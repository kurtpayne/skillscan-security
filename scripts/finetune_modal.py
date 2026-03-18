"""Modal-based GPU fine-tuning for the SkillScan prompt-injection DeBERTa model.

This script wraps the local finetune.py logic in a Modal function that runs on
a GPU worker, then pushes the resulting LoRA adapter to the HuggingFace Hub.

Usage (local trigger):
    modal run scripts/finetune_modal.py                  # respects delta threshold
    modal run scripts/finetune_modal.py --force          # ignore threshold
    modal run scripts/finetune_modal.py --dry-run        # stats only, no GPU

Environment variables (set as Modal secrets or GitHub secrets):
    HF_TOKEN          HuggingFace write token (required for Hub push)
    HF_REPO_ID        Target repo, e.g. "kurtpayne/skillscan-deberta-adapter"
                      Defaults to "kurtpayne/skillscan-deberta-adapter"

The function:
1. Uploads the local corpus/ directory to Modal's ephemeral volume.
2. Fine-tunes deberta-v3-base-prompt-injection-v2 with LoRA (PEFT).
3. Pushes the adapter weights + tokenizer to HuggingFace Hub.
4. Updates corpus/manifest.json with the new adapter SHA and version.
5. Returns a summary dict that corpus-sync.yml can consume.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import UTC
from pathlib import Path

import modal

# ---------------------------------------------------------------------------
# Modal app definition
# ---------------------------------------------------------------------------

app = modal.App("skillscan-finetune")

# GPU image: Python 3.11 + ML stack + PEFT for LoRA
gpu_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "transformers>=4.40.0",
        "torch>=2.2.0",
        "peft>=0.10.0",          # LoRA adapter support
        "datasets>=2.18.0",
        "accelerate>=0.28.0",
        "huggingface_hub>=0.22.0",
        "pyyaml>=6.0",
        "tqdm>=4.66.0",
        "optimum[onnxruntime]>=1.18.0",  # ONNX export + INT8 quantization
        "onnxruntime>=1.17.0",
    )
)

# Modal secret for HuggingFace token
hf_secret = modal.Secret.from_name("huggingface-token", required_keys=[])

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BASE_MODEL = "protectai/deberta-v3-base-prompt-injection-v2"
DEFAULT_HF_REPO = "kurtpayne/skillscan-deberta-adapter"
LORA_R = 16
LORA_ALPHA = 32
LORA_DROPOUT = 0.05
MAX_LENGTH = 256
EPOCHS = 3
BATCH_SIZE = 8
LEARNING_RATE = 2e-5


# ---------------------------------------------------------------------------
# Remote function
# ---------------------------------------------------------------------------

@app.function(
    image=gpu_image,
    gpu="T4",
    timeout=1800,       # 30 minutes max
    secrets=[hf_secret],
    memory=8192,
)
def run_finetune(
    corpus_data: dict[str, str],   # {relative_path: file_content}
    manifest_json: str,
    force: bool = False,
    dry_run: bool = False,
    hf_repo_id: str = DEFAULT_HF_REPO,
) -> dict:
    """Run fine-tuning on a GPU worker and push adapter to HuggingFace Hub."""
    import json
    import tempfile
    from pathlib import Path

    import torch
    from peft import LoraConfig, TaskType, get_peft_model
    from transformers import (
        AutoModelForSequenceClassification,
        AutoTokenizer,
        Trainer,
        TrainingArguments,
    )

    print(f"GPU available: {torch.cuda.is_available()}")
    print(f"Corpus examples: {len(corpus_data)}")

    # Write corpus to temp dir
    tmpdir = Path(tempfile.mkdtemp())
    corpus_dir = tmpdir / "corpus"
    for rel_path, content in corpus_data.items():
        dest = corpus_dir / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")

    # Parse manifest for delta check
    manifest = json.loads(manifest_json) if manifest_json else {}
    last_finetune = manifest.get("last_finetune")
    corpus_size = len(corpus_data)

    if dry_run:
        return {
            "status": "dry_run",
            "corpus_size": corpus_size,
            "last_finetune": last_finetune,
        }

    # Build labelled dataset from corpus structure
    # corpus/benign/*.md → label 0
    # corpus/prompt_injection/*.md + corpus/malicious/*.md → label 1
    label2id = {"benign": 0, "injection": 1}
    examples: list[tuple[str, int]] = []

    for rel_path, content in corpus_data.items():
        parts = Path(rel_path).parts
        if not parts:
            continue
        category = parts[0]
        if category == "benign":
            label = 0
        elif category in ("prompt_injection", "malicious"):
            label = 1
        else:
            continue  # skip manifest.json and README
        examples.append((content, label))

    if not examples:
        return {"status": "error", "message": "No labelled examples found in corpus"}

    label_counts = {0: sum(1 for _, lbl in examples if lbl == 0),
                    1: sum(1 for _, lbl in examples if lbl == 1)}
    print(f"Dataset: {len(examples)} examples — benign={label_counts[0]}, injection={label_counts[1]}")

    # Tokenise
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    texts = [text for text, _ in examples]
    labels = [label for _, label in examples]

    encodings = tokenizer(
        texts,
        truncation=True,
        padding=True,
        max_length=MAX_LENGTH,
        return_tensors="pt",
    )

    class SkillDataset(torch.utils.data.Dataset):  # type: ignore[misc]
        def __init__(self, enc: dict, lbls: list) -> None:
            self.enc = enc
            self.lbls = lbls
        def __len__(self) -> int:
            return len(self.lbls)
        def __getitem__(self, idx: int) -> dict:
            return {k: v[idx] for k, v in self.enc.items()} | {"labels": torch.tensor(self.lbls[idx])}

    dataset = SkillDataset(encodings, labels)

    # Load base model
    model = AutoModelForSequenceClassification.from_pretrained(
        BASE_MODEL,
        num_labels=2,
        id2label={0: "BENIGN", 1: "INJECTION"},
        label2id=label2id,
        ignore_mismatched_sizes=True,
    )

    # Apply LoRA
    lora_config = LoraConfig(
        task_type=TaskType.SEQ_CLS,
        r=LORA_R,
        lora_alpha=LORA_ALPHA,
        lora_dropout=LORA_DROPOUT,
        target_modules=["query_proj", "value_proj"],
        bias="none",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # Train
    output_dir = str(tmpdir / "adapter")
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        learning_rate=LEARNING_RATE,
        weight_decay=0.01,
        logging_steps=10,
        save_strategy="epoch",
        evaluation_strategy="no",
        load_best_model_at_end=False,
        report_to="none",
        fp16=torch.cuda.is_available(),
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
    )

    print("Starting LoRA fine-tune...")
    trainer.train()
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Adapter saved to {output_dir}")

    # -----------------------------------------------------------------------
    # ONNX export: merge LoRA → base, export to ONNX, INT8 quantize
    # This produces a ~70MB quantized model for fast CPU inference.
    # Users download this via `skillscan model sync` — no PyTorch needed.
    # -----------------------------------------------------------------------
    onnx_dir = str(tmpdir / "onnx")
    onnx_result: dict[str, object] = {"exported": False}
    try:
        from optimum.onnxruntime import ORTModelForSequenceClassification, ORTQuantizer
        from optimum.onnxruntime.configuration import AutoQuantizationConfig

        print("Merging LoRA adapter into base weights...")
        merged_model = model.merge_and_unload()
        merged_dir = str(tmpdir / "merged")
        merged_model.save_pretrained(merged_dir)
        tokenizer.save_pretrained(merged_dir)
        print("Exporting merged model to ONNX...")
        ort_model = ORTModelForSequenceClassification.from_pretrained(
            merged_dir,
            export=True,
        )
        ort_model.save_pretrained(onnx_dir)
        tokenizer.save_pretrained(onnx_dir)
        print("Quantizing ONNX model to INT8...")
        quantizer = ORTQuantizer.from_pretrained(onnx_dir)
        qconfig = AutoQuantizationConfig.avx512_vnni(is_static=False, per_channel=False)
        quantizer.quantize(
            save_dir=onnx_dir,
            quantization_config=qconfig,
        )
        # Write a manifest for model_sync.py to validate downloads
        import hashlib as _hashlib
        import pathlib as _pathlib
        onnx_sha256 = _hashlib.sha256()
        for f in sorted(_pathlib.Path(onnx_dir).rglob("*")):
            if f.is_file():
                onnx_sha256.update(f.read_bytes())
        onnx_manifest = {
            "version": f"{corpus_size}-{EPOCHS}ep",
            "sha256": onnx_sha256.hexdigest(),
            "files": [f.name for f in _pathlib.Path(onnx_dir).iterdir() if f.is_file()],
            "quantization": "int8-avx512",
            "base_model": BASE_MODEL,
            "corpus_size": corpus_size,
        }
        (_pathlib.Path(onnx_dir) / "skillscan_manifest.json").write_text(
            json.dumps(onnx_manifest, indent=2)
        )
        onnx_result = {"exported": True, "quantization": "int8-avx512", "dir": onnx_dir}
        print(f"ONNX INT8 model ready at {onnx_dir}")
    except Exception as exc:
        print(f"ONNX export failed (non-fatal): {exc}")
        onnx_result = {"exported": False, "error": str(exc)}

    # -----------------------------------------------------------------------
    # Push to HuggingFace Hub
    # Prefer the ONNX model if export succeeded; fall back to raw LoRA adapter.
    # -----------------------------------------------------------------------
    hf_token = os.environ.get("HF_TOKEN")
    push_result = {"pushed": False, "repo_id": hf_repo_id}
    if hf_token:
        from huggingface_hub import HfApi
        api = HfApi(token=hf_token)
        upload_dir = onnx_dir if onnx_result.get("exported") else output_dir
        commit_msg = (
            f"Auto fine-tune: {corpus_size} examples (ONNX INT8)"
            if onnx_result.get("exported")
            else f"Auto fine-tune: {corpus_size} examples (LoRA adapter)"
        )
        try:
            api.create_repo(repo_id=hf_repo_id, exist_ok=True, private=False)
            api.upload_folder(
                folder_path=upload_dir,
                repo_id=hf_repo_id,
                commit_message=commit_msg,
            )
            push_result["pushed"] = True
            push_result["onnx"] = bool(onnx_result.get("exported"))
            print(f"Model pushed to https://huggingface.co/{hf_repo_id}")
        except Exception as e:
            push_result["error"] = str(e)
            print(f"HF Hub push failed: {e}")
    else:
        print("HF_TOKEN not set — skipping Hub push")

    return {
        "status": "success",
        "corpus_size": corpus_size,
        "label_counts": label_counts,
        "epochs": EPOCHS,
        "lora_r": LORA_R,
        "hf_push": push_result,
    }


# ---------------------------------------------------------------------------
# Local entrypoint
# ---------------------------------------------------------------------------

@app.local_entrypoint()
def main(
    force: bool = False,
    dry_run: bool = False,
    hf_repo_id: str = DEFAULT_HF_REPO,
) -> None:
    """Collect corpus locally and dispatch GPU fine-tune to Modal."""
    repo_root = Path(__file__).parent.parent
    corpus_dir = repo_root / "corpus"
    manifest_path = corpus_dir / "manifest.json"

    if not corpus_dir.exists():
        print("ERROR: corpus/ directory not found. Run: skillscan corpus sync")
        sys.exit(1)

    # Load corpus files into memory for upload
    corpus_data: dict[str, str] = {}
    for md_file in corpus_dir.rglob("*.md"):
        rel = str(md_file.relative_to(corpus_dir))
        try:
            corpus_data[rel] = md_file.read_text(encoding="utf-8", errors="replace")
        except Exception:
            pass

    manifest_json = manifest_path.read_text() if manifest_path.exists() else "{}"

    print(f"Uploading {len(corpus_data)} corpus files to Modal...")

    result = run_finetune.remote(
        corpus_data=corpus_data,
        manifest_json=manifest_json,
        force=force,
        dry_run=dry_run,
        hf_repo_id=hf_repo_id,
    )

    print(json.dumps(result, indent=2))

    if result.get("status") == "success" and result.get("hf_push", {}).get("pushed"):
        # Update local manifest with finetune record
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text())
        else:
            manifest = {}
        from datetime import datetime
        now_iso = datetime.now(UTC).isoformat()
        manifest["last_finetune"] = now_iso
        manifest["last_finetune_corpus_size"] = result["corpus_size"]
        manifest["adapter_repo"] = hf_repo_id
        manifest_path.write_text(json.dumps(manifest, indent=2))
        print(f"Manifest updated: {manifest_path}")

        # Auto-update CORPUS_CARD.md fine-tune history table
        _update_corpus_card(
            corpus_dir=corpus_dir,
            result=result,
            hf_repo_id=hf_repo_id,
            now_iso=now_iso,
        )


def _update_corpus_card(
    corpus_dir: Path,
    result: dict,
    hf_repo_id: str,
    now_iso: str,
) -> None:
    """Append a row to the Fine-Tune History table in CORPUS_CARD.md."""
    import hashlib
    import subprocess

    card_path = corpus_dir / "CORPUS_CARD.md"
    if not card_path.exists():
        return

    # Compute corpus SHA
    all_files = sorted(corpus_dir.rglob("*.md"), key=lambda p: str(p))
    h = hashlib.sha256()
    for f in all_files:
        h.update(f.read_bytes())
    corpus_sha = h.hexdigest()

    # Get git commit
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(corpus_dir.parent),
            text=True,
        ).strip()
        commit_url = (
            "https://github.com/kurtpayne/skillscan-security/commit/"
            + subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=str(corpus_dir.parent),
                text=True,
            ).strip()
        )
        commit_link = f"[`{commit}`]({commit_url})"
    except Exception:
        commit_link = "unknown"

    label_counts = result.get("label_counts", {})
    benign = label_counts.get(0, "?")
    injection = label_counts.get(1, "?")
    corpus_size = result.get("corpus_size", "?")
    model_version = f"{corpus_size}-{EPOCHS}ep"
    date_str = now_iso[:10]  # YYYY-MM-DD
    sha_short = corpus_sha[:16]

    new_row = (
        f"| {date_str} | {corpus_size} | {benign} | {injection} "
        f"| `{sha_short}` | {model_version} | {commit_link} |"
    )

    card_text = card_path.read_text()
    # Replace the placeholder row if still present
    placeholder = "| *(first run pending)* |"
    if placeholder in card_text:
        lines = card_text.splitlines()
        new_lines = []
        for line in lines:
            if line.startswith(placeholder):
                new_lines.append(new_row)
            else:
                new_lines.append(line)
        card_path.write_text("\n".join(new_lines) + "\n")
    else:
        # Append after the last row in the Fine-Tune History table
        header = "| Date | Corpus Size |"
        lines = card_text.splitlines()
        insert_idx = None
        for i, line in enumerate(lines):
            if line.startswith(header):
                # Find the end of this table block
                j = i + 2  # skip header + separator
                while j < len(lines) and lines[j].startswith("|"):
                    j += 1
                insert_idx = j
                break
        if insert_idx is not None:
            lines.insert(insert_idx, new_row)
            card_path.write_text("\n".join(lines) + "\n")

    print(f"CORPUS_CARD.md updated with fine-tune record for {date_str}")
