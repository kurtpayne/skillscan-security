#!/usr/bin/env python3
"""scripts/finetune.py — Fine-tune DeBERTa-v3 on the SkillScan corpus.

Usage
-----
    python scripts/finetune.py [OPTIONS]

Options
-------
    --corpus-dir PATH       Path to corpus/ directory (default: auto-discover)
    --output-dir PATH       Where to save the fine-tuned model (default: checkpoints/)
    --base-model NAME       HuggingFace model ID to start from
                            (default: protectai/deberta-v3-base-prompt-injection-v2)
    --epochs INT            Number of training epochs (default: 3)
    --batch-size INT        Per-device training batch size (default: 8)
    --max-length INT        Max token length (default: 256)
    --learning-rate FLOAT   Learning rate (default: 2e-5)
    --dry-run               Print dataset stats and exit without training
    --force                 Run even if corpus delta is below threshold

Exit codes
----------
    0  — training completed (or dry-run / skipped)
    1  — error
    2  — skipped (delta below threshold, use --force to override)

Environment variables
---------------------
    SKILLSCAN_CORPUS_DIR         Override corpus directory
    SKILLSCAN_MIN_NEW_EXAMPLES   Absolute delta threshold (default 50)
    SKILLSCAN_MIN_DELTA_PCT      Relative delta threshold (default 0.10)
    SKILLSCAN_BASE_MODEL         Override base model ID
    HF_TOKEN                     HuggingFace token for private model access
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import UTC, datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Resolve paths relative to the repo root regardless of cwd
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from skillscan.corpus import CorpusManager  # noqa: E402

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Fine-tune DeBERTa on SkillScan corpus")
    p.add_argument("--corpus-dir", type=Path, default=None)
    p.add_argument("--output-dir", type=Path, default=REPO_ROOT / "checkpoints")
    p.add_argument(
        "--base-model",
        default="protectai/deberta-v3-base-prompt-injection-v2",
    )
    p.add_argument("--epochs", type=int, default=3)
    p.add_argument("--batch-size", type=int, default=8)
    p.add_argument("--max-length", type=int, default=256)
    p.add_argument("--learning-rate", type=float, default=2e-5)
    p.add_argument("--dry-run", action="store_true", help="Print stats and exit")
    p.add_argument("--force", action="store_true", help="Ignore delta threshold")
    return p.parse_args()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    args = parse_args()

    mgr = CorpusManager(corpus_dir=args.corpus_dir)

    # Sync corpus and evaluate delta
    decision = mgr.sync()
    logger.info(decision.summary())

    if args.dry_run:
        status = mgr.status()
        print(json.dumps(status, indent=2))
        return 0

    if not decision.should_retrain and not args.force:
        logger.info("Delta below threshold — skipping fine-tune (use --force to override).")
        return 2

    if decision.should_retrain:
        logger.info("Delta threshold crossed — proceeding with fine-tune.")
    else:
        logger.info("--force flag set — proceeding despite sub-threshold delta.")

    # Build dataset
    examples = mgr.iter_examples()
    if not examples:
        logger.error("Corpus is empty — nothing to train on.")
        return 1

    label_dist = {}
    for _, label in examples:
        label_dist[label] = label_dist.get(label, 0) + 1
    logger.info("Dataset: %d examples — %s", len(examples), label_dist)

    # Check ML dependencies
    try:
        import torch  # type: ignore[import-untyped]
        from transformers import (  # type: ignore[import-untyped]
            AutoModelForSequenceClassification,
            AutoTokenizer,
            Trainer,
            TrainingArguments,
        )
    except ImportError:
        logger.error(
            "ML dependencies not installed. Run: pip install 'skillscan-security[ml]'"
        )
        return 1

    # Tokenise
    tokenizer = AutoTokenizer.from_pretrained(args.base_model)
    label2id = {"benign": 0, "injection": 1}

    texts = [p.read_text(encoding="utf-8", errors="replace") for p, _ in examples]
    labels = [label2id[lbl] for _, lbl in examples]

    encodings = tokenizer(
        texts,
        truncation=True,
        padding=True,
        max_length=args.max_length,
        return_tensors="pt",
    )

    class SkillDataset(torch.utils.data.Dataset):  # type: ignore[misc]
        def __init__(self, enc: dict, lbls: list[int]) -> None:
            self.enc = enc
            self.lbls = lbls

        def __len__(self) -> int:
            return len(self.lbls)

        def __getitem__(self, idx: int) -> dict:
            return {k: v[idx] for k, v in self.enc.items()} | {"labels": torch.tensor(self.lbls[idx])}

    dataset = SkillDataset(encodings, labels)

    # Model
    model = AutoModelForSequenceClassification.from_pretrained(
        args.base_model,
        num_labels=2,
        id2label={0: "BENIGN", 1: "INJECTION"},
        label2id=label2id,
        ignore_mismatched_sizes=True,
    )

    # Checkpoint path
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    checkpoint_dir = args.output_dir / f"deberta-v3-ft-{timestamp}"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    training_args = TrainingArguments(
        output_dir=str(checkpoint_dir),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        weight_decay=0.01,
        logging_steps=10,
        save_strategy="epoch",
        evaluation_strategy="no",
        load_best_model_at_end=False,
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
    )

    logger.info("Starting fine-tune → %s", checkpoint_dir)
    trainer.train()
    trainer.save_model(str(checkpoint_dir))
    tokenizer.save_pretrained(str(checkpoint_dir))
    logger.info("Fine-tune complete → %s", checkpoint_dir)

    # Record in manifest
    mgr.record_finetune(str(checkpoint_dir))

    # Write a summary JSON for CI to consume
    summary = {
        "checkpoint": str(checkpoint_dir),
        "timestamp": timestamp,
        "corpus_size": decision.corpus_size_after,
        "new_examples": decision.new_examples,
        "changed_examples": decision.changed_examples,
        "base_model": args.base_model,
        "epochs": args.epochs,
    }
    summary_path = checkpoint_dir / "finetune_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    logger.info("Summary written to %s", summary_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
