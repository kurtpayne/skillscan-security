#!/usr/bin/env python3
"""scripts/reserve_eval_set.py — Reserve a stratified 20% held-out evaluation set.

Reads the combined public + private corpus, stratifies by label (benign /
injection), and copies 20% of each label class into the private corpus's
``held_out_eval/`` directory.  The selected files are NOT removed from the
training corpus — the training pipeline already excludes ``held_out_eval/``
via ``CorpusManager.iter_examples()``.

The held-out set lives in the private ``skillscan-corpus`` repo so that it
is never visible in the public repo.  The naming convention is:

    held_out_eval/benign_<slug>.md     → label: benign
    held_out_eval/injection_<slug>.md  → label: injection

Usage
-----
    python scripts/reserve_eval_set.py [--dry-run] [--ratio 0.2] [--seed 42]
    python scripts/reserve_eval_set.py \\
        --corpus-dir corpus/ \\
        --private-dir /path/to/skillscan-corpus \\
        --ratio 0.2

Options
-------
    --corpus-dir PATH    Public corpus root (default: corpus/)
    --private-dir PATH   Private corpus root (default: ../skillscan-corpus)
    --ratio FLOAT        Fraction to reserve (default: 0.20)
    --seed INT           Random seed (default: 42)
    --dry-run            Print what would be written without writing
    --force              Overwrite existing held-out files (default: skip)
"""
from __future__ import annotations

import argparse
import random
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DEFAULT_PRIVATE_DIR = REPO_ROOT.parent / "skillscan-corpus"


def _label_for_path(rel: str, filename: str = "") -> str | None:
    """Infer label from the relative path within the corpus directory.

    For social_engineering/, the filename prefix determines the label:
    files starting with 'benign' are benign; all others are injection.
    This mirrors the logic in CorpusManager.iter_examples().
    """
    parts = rel.replace("\\", "/").split("/")
    if not parts:
        return None
    top = parts[0]
    if top == "benign":
        return "benign"
    if top in ("prompt_injection", "malicious", "adversarial",
               "jailbreak_distillations"):
        return "injection"
    if top == "social_engineering":
        # Benign counterparts are prefixed with 'benign_'
        fname = filename or (parts[-1] if len(parts) > 1 else "")
        return "benign" if fname.startswith("benign") else "injection"
    if top == "graph_injection":
        # graph_injection/RULE/polarity/file.md
        # polarity can be 'malicious', 'malicious_2', 'benign', 'benign_2'
        polarity = parts[2] if len(parts) >= 3 else "malicious"
        return "injection" if polarity.startswith("malicious") else "benign"
    if top == "held_out_eval":
        return None  # already in eval set
    return None


def collect_corpus_examples(corpus_dir: Path) -> list[tuple[Path, str]]:
    """Return (absolute_path, label) for all training-eligible examples."""
    examples: list[tuple[Path, str]] = []
    for p in sorted(corpus_dir.rglob("*.md")):
        rel = str(p.relative_to(corpus_dir)).replace("\\", "/")
        # Skip manifest, README, held_out_eval
        if rel.startswith("held_out_eval/"):
            continue
        label = _label_for_path(rel, filename=p.name)
        if label is None:
            continue
        examples.append((p, label))
    return examples


def stratified_sample(
    examples: list[tuple[Path, str]],
    ratio: float,
    seed: int,
) -> list[tuple[Path, str]]:
    """Return a stratified sample of `ratio` fraction from each label class."""
    rng = random.Random(seed)
    by_label: dict[str, list[tuple[Path, str]]] = {}
    for path, label in examples:
        by_label.setdefault(label, []).append((path, label))

    selected: list[tuple[Path, str]] = []
    for label, group in sorted(by_label.items()):
        shuffled = list(group)
        rng.shuffle(shuffled)
        n = max(1, round(len(shuffled) * ratio))
        selected.extend(shuffled[:n])

    return selected


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--corpus-dir",
        type=Path,
        default=REPO_ROOT / "corpus",
        help="Public corpus root (default: corpus/)",
    )
    parser.add_argument(
        "--private-dir",
        type=Path,
        default=DEFAULT_PRIVATE_DIR,
        help="Private corpus root (default: ../skillscan-corpus)",
    )
    parser.add_argument(
        "--ratio",
        type=float,
        default=0.20,
        help="Fraction to reserve as held-out eval (default: 0.20)",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing held-out files",
    )
    args = parser.parse_args()

    corpus_dir: Path = args.corpus_dir.resolve()
    private_dir: Path = args.private_dir.resolve()
    eval_dir: Path = private_dir / "held_out_eval"

    if not corpus_dir.is_dir():
        print(f"ERROR: corpus directory not found: {corpus_dir}", file=sys.stderr)
        sys.exit(1)

    if not private_dir.is_dir():
        print(
            f"ERROR: private corpus directory not found: {private_dir}\n"
            "Clone skillscan-corpus first: gh repo clone kurtpayne/skillscan-corpus",
            file=sys.stderr,
        )
        sys.exit(1)

    # Also collect private corpus examples (adversarial/, jailbreak_distillations/)
    all_examples: list[tuple[Path, str]] = collect_corpus_examples(corpus_dir)
    all_examples += collect_corpus_examples(private_dir)

    # Deduplicate by filename stem (in case public + private overlap)
    seen_stems: set[str] = set()
    deduped: list[tuple[Path, str]] = []
    for path, label in all_examples:
        if path.stem not in seen_stems:
            seen_stems.add(path.stem)
            deduped.append((path, label))

    label_counts = {}
    for _, label in deduped:
        label_counts[label] = label_counts.get(label, 0) + 1

    print(f"Total training examples: {len(deduped)}")
    for label, count in sorted(label_counts.items()):
        print(f"  {label}: {count}")

    selected = stratified_sample(deduped, args.ratio, args.seed)

    sel_counts = {}
    for _, label in selected:
        sel_counts[label] = sel_counts.get(label, 0) + 1

    print(f"\nReserving {len(selected)} examples ({args.ratio*100:.0f}% stratified):")
    for label, count in sorted(sel_counts.items()):
        print(f"  {label}: {count}")

    if args.dry_run:
        print("\n[DRY RUN] Would write to:", eval_dir)
        for path, label in sorted(selected, key=lambda x: (x[1], x[0].name)):
            dest_name = f"{label}_{path.stem}.md"
            print(f"  {dest_name}  ← {path.relative_to(path.parent.parent)}")
        return

    eval_dir.mkdir(parents=True, exist_ok=True)
    written = 0
    skipped = 0

    for path, label in selected:
        dest_name = f"{label}_{path.stem}.md"
        dest = eval_dir / dest_name
        if dest.exists() and not args.force:
            skipped += 1
            continue
        shutil.copy2(path, dest)
        written += 1

    print(f"\nDone. Written: {written}, Skipped (already exist): {skipped}")
    print(f"Held-out eval set: {eval_dir}")
    print(
        "\nNext steps:\n"
        "  1. cd ../skillscan-corpus && git add held_out_eval/ && git commit -m 'feat(eval): reserve 20% held-out eval set'\n"
        "  2. git push origin main\n"
        "  3. Run: modal run scripts/finetune_modal.py --dry-run  (to verify eval step)"
    )


if __name__ == "__main__":
    main()
