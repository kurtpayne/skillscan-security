"""corpus.py — Corpus management and model update trigger for skillscan-security.

Responsibilities
----------------
1. **CorpusManager**: Scans the ``corpus/`` directory, computes SHA-256 fingerprints
   for every example, and maintains a ``manifest.json`` that tracks corpus state
   across runs.

2. **UpdateDecision**: Evaluates whether the corpus delta since the last fine-tune
   warrants a new training run.  Two configurable thresholds govern the decision:

   * ``min_new_examples`` (default 50) — absolute count of new/changed examples.
   * ``min_delta_pct``    (default 0.10) — relative growth of the corpus (10 %).

   A fine-tune is triggered when **either** threshold is crossed.  This keeps
   retraining cheap for small corpora (absolute threshold dominates early on) and
   proportional for large ones (relative threshold dominates later).

3. **Dual-manifest support**: When private corpus fixtures are merged in CI via the
   corpus-sync deploy key workflow, the manager operates in two modes:

   - **Public manifest** (``manifest.json``): reflects only the public corpus
     subdirectories.  This is the file committed back to the public repo.  It
     never contains SHA-256 hashes or counts for private fixtures.

   - **Combined manifest** (``manifest_combined.json``): reflects the full merged
     corpus including private fixtures.  This file is written in CI only and is
     never committed.  The retrain decision is made from the combined manifest.

   The ``sync()`` method always writes the public manifest.  Pass
   ``combined_manifest_path`` to also write the combined manifest and base the
   retrain decision on the full corpus.

4. **CLI integration**: ``skillscan corpus sync`` and ``skillscan corpus status``
   subcommands are wired in via ``cli.py``.

Corpus directory layout
-----------------------
Public subdirectories (committed to public repo, included in public manifest):
  benign/               Benign skill examples — label: benign
  malicious/            Known malicious patterns — label: injection
  prompt_injection/     Prompt injection variants — label: injection
  social_engineering/   SE credential-harvest patterns — label: injection
  graph_injection/      Skill-graph injection patterns — label: injection
                        (nested structure: RULE-ID/malicious/ and RULE-ID/benign/)

Private subdirectories (merged in CI from skillscan-corpus, NOT in public manifest):
  adversarial/          Evasion-crafted adversarial variants — label: injection
  jailbreak_distillations/  Jailbreak patterns in skill contexts — label: injection

Eval-only subdirectories (never used for training):
  held_out_eval/        Reserved 20% held-out evaluation set — excluded from training

Environment variables
---------------------
``SKILLSCAN_CORPUS_DIR``       — override the default ``corpus/`` path.
``SKILLSCAN_MIN_NEW_EXAMPLES`` — override the absolute delta threshold.
``SKILLSCAN_MIN_DELTA_PCT``    — override the relative delta threshold (0–1 float).
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MANIFEST_FILENAME = "manifest.json"
MANIFEST_COMBINED_FILENAME = "manifest_combined.json"
MANIFEST_VERSION = 1

# Public subdirectory → label mapping.
# These directories are committed to the public repo and included in the
# public manifest.  The updater agent adds to malicious/ and prompt_injection/.
PUBLIC_LABEL_MAP: dict[str, str] = {
    "benign": "benign",
    "malicious": "injection",
    "prompt_injection": "injection",
    "social_engineering": "injection",
    # graph_injection/ uses a nested structure (RULE-ID/{malicious,benign}/)
    # handled separately in iter_examples().
}

# Private subdirectory → label mapping.
# These directories are merged from skillscan-corpus in CI via deploy key.
# They are included in training but NOT in the committed public manifest.
PRIVATE_LABEL_MAP: dict[str, str] = {
    "adversarial": "injection",
    "jailbreak_distillations": "injection",
}

# Subdirectories that are never used for training (eval only).
EVAL_ONLY_DIRS: frozenset[str] = frozenset({"held_out_eval"})

SUPPORTED_EXTENSIONS = {".md", ".txt", ".yaml", ".yml"}

# Default delta thresholds
DEFAULT_MIN_NEW_EXAMPLES = int(os.getenv("SKILLSCAN_MIN_NEW_EXAMPLES", "50"))
DEFAULT_MIN_DELTA_PCT = float(os.getenv("SKILLSCAN_MIN_DELTA_PCT", "0.10"))


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class FineTuneRecord:
    """Metadata about the last completed fine-tune run."""

    timestamp: str = ""
    corpus_size_at_finetune: int = 0
    model_checkpoint: str = ""

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> FineTuneRecord:
        return cls(
            timestamp=d.get("timestamp", ""),
            corpus_size_at_finetune=int(d.get("corpus_size_at_finetune", 0)),
            model_checkpoint=d.get("model_checkpoint", ""),
        )


@dataclass
class CorpusManifest:
    """Serialisable snapshot of corpus state."""

    version: int = MANIFEST_VERSION
    last_updated: str = ""
    total_examples: int = 0
    label_counts: dict[str, int] = field(default_factory=dict)
    sha256_index: dict[str, str] = field(default_factory=dict)
    last_finetune: FineTuneRecord = field(default_factory=FineTuneRecord)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["last_finetune"] = asdict(self.last_finetune)
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> CorpusManifest:
        m = cls(
            version=int(d.get("version", MANIFEST_VERSION)),
            last_updated=d.get("last_updated", ""),
            total_examples=int(d.get("total_examples", 0)),
            label_counts=dict(d.get("label_counts", {})),
            sha256_index=dict(d.get("sha256_index", {})),
        )
        ft = d.get("last_finetune", {})
        m.last_finetune = FineTuneRecord.from_dict(ft) if ft else FineTuneRecord()
        return m


@dataclass
class UpdateDecision:
    """Result of evaluating whether a fine-tune run should be triggered."""

    should_retrain: bool
    new_examples: int
    changed_examples: int
    removed_examples: int
    corpus_size_before: int
    corpus_size_after: int
    delta_pct: float
    reason: str

    @property
    def delta_total(self) -> int:
        return self.new_examples + self.changed_examples

    def summary(self) -> str:
        status = "RETRAIN" if self.should_retrain else "SKIP"
        return (
            f"[{status}] corpus: {self.corpus_size_before} → {self.corpus_size_after} examples "
            f"(+{self.new_examples} new, {self.changed_examples} changed, "
            f"{self.removed_examples} removed, {self.delta_pct:.1%} delta). {self.reason}"
        )


# ---------------------------------------------------------------------------
# CorpusManager
# ---------------------------------------------------------------------------


class CorpusManager:
    """Manages the training corpus and decides when to trigger fine-tuning.

    Parameters
    ----------
    corpus_dir:
        Root of the corpus directory.  Defaults to ``corpus/`` relative to the
        repo root (detected from this file's location).
    min_new_examples:
        Absolute count of new/changed examples that triggers a retrain.
    min_delta_pct:
        Relative corpus growth fraction (0–1) that triggers a retrain.
    include_private:
        If True, include private subdirectories (adversarial/,
        jailbreak_distillations/) in the training index.  The public manifest
        is still written without these entries; the combined manifest is written
        to ``manifest_combined.json`` alongside the public manifest.
        Default: auto-detected from whether the private directories exist.
    """

    def __init__(
        self,
        corpus_dir: Path | None = None,
        min_new_examples: int = DEFAULT_MIN_NEW_EXAMPLES,
        min_delta_pct: float = DEFAULT_MIN_DELTA_PCT,
        include_private: bool | None = None,
    ) -> None:
        env_dir = os.getenv("SKILLSCAN_CORPUS_DIR")
        if corpus_dir is None and env_dir:
            corpus_dir = Path(env_dir)
        if corpus_dir is None:
            # Default: corpus/ sibling of the package root
            corpus_dir = Path(__file__).parent.parent.parent / "corpus"
        self.corpus_dir = corpus_dir.resolve()
        self.manifest_path = self.corpus_dir / MANIFEST_FILENAME
        self.combined_manifest_path = self.corpus_dir / MANIFEST_COMBINED_FILENAME
        self.min_new_examples = min_new_examples
        self.min_delta_pct = min_delta_pct

        # Auto-detect whether private directories are present
        if include_private is None:
            include_private = any(
                (self.corpus_dir / d).is_dir() for d in PRIVATE_LABEL_MAP
            )
        self.include_private = include_private

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def sync(self) -> UpdateDecision:
        """Scan corpus, update manifest(s), and return an UpdateDecision.

        Always writes the public manifest (manifest.json) which covers only
        public subdirectories.  If private directories are present, also writes
        manifest_combined.json and bases the retrain decision on the combined
        corpus size.
        """
        old_public_manifest = self._load_manifest(self.manifest_path)

        # Build public index (for the committed manifest)
        public_index = self._build_index(include_private=False)
        new_public_manifest = self._build_manifest(public_index, old_public_manifest)
        self._save_manifest(new_public_manifest, self.manifest_path)

        if self.include_private:
            # Build combined index (for the retrain decision)
            combined_index = self._build_index(include_private=True)
            old_combined = self._load_manifest(self.combined_manifest_path)
            new_combined_manifest = self._build_manifest(combined_index, old_combined)
            # Carry last_finetune from the public manifest into the combined one
            new_combined_manifest.last_finetune = new_public_manifest.last_finetune
            self._save_manifest(new_combined_manifest, self.combined_manifest_path)
            decision = self._evaluate(old_combined, new_combined_manifest)
            logger.info(
                "Combined corpus: %d public + %d private = %d total",
                len(public_index),
                len(combined_index) - len(public_index),
                len(combined_index),
            )
        else:
            decision = self._evaluate(old_public_manifest, new_public_manifest)

        logger.info(decision.summary())
        return decision

    def status(self) -> dict[str, Any]:
        """Return a human-readable status dict without modifying the manifest."""
        public_manifest = self._load_manifest(self.manifest_path)
        public_index = self._build_index(include_private=False)
        combined_index = self._build_index(include_private=True)

        result: dict[str, Any] = {
            "corpus_dir": str(self.corpus_dir),
            "manifest_exists": self.manifest_path.exists(),
            "public_examples": len(public_index),
            "private_examples": len(combined_index) - len(public_index),
            "combined_examples": len(combined_index),
            # Backward-compatible alias: current_examples == combined_examples
            "current_examples": len(combined_index),
            "manifest_examples": public_manifest.total_examples,
            "label_counts": public_manifest.label_counts,
            "last_updated": public_manifest.last_updated,
            "last_finetune": asdict(public_manifest.last_finetune),
            "thresholds": {
                "min_new_examples": self.min_new_examples,
                "min_delta_pct": self.min_delta_pct,
            },
        }

        # Per-directory breakdown
        breakdown: dict[str, int] = {}
        for d in sorted(self.corpus_dir.iterdir()):
            if not d.is_dir():
                continue
            name = d.name
            if name in EVAL_ONLY_DIRS:
                count = sum(
                    1 for p in d.rglob("*")
                    if p.is_file() and p.suffix in SUPPORTED_EXTENSIONS
                )
                breakdown[f"{name} (eval-only)"] = count
            elif name in PUBLIC_LABEL_MAP or name == "graph_injection":
                count = sum(
                    1 for p in d.rglob("*")
                    if p.is_file() and p.suffix in SUPPORTED_EXTENSIONS
                )
                breakdown[f"{name} (public)"] = count
            elif name in PRIVATE_LABEL_MAP:
                count = sum(
                    1 for p in d.rglob("*")
                    if p.is_file() and p.suffix in SUPPORTED_EXTENSIONS
                )
                breakdown[f"{name} (private)"] = count
        result["directory_breakdown"] = breakdown

        return result

    def record_finetune(self, checkpoint: str) -> None:
        """Update the manifest to record a completed fine-tune run."""
        manifest = self._load_manifest(self.manifest_path)
        # Use combined size if available, else public size
        combined_manifest = self._load_manifest(self.combined_manifest_path)
        size = combined_manifest.total_examples or manifest.total_examples
        record = FineTuneRecord(
            timestamp=_now_iso(),
            corpus_size_at_finetune=size,
            model_checkpoint=checkpoint,
        )
        manifest.last_finetune = record
        self._save_manifest(manifest, self.manifest_path)
        if self.combined_manifest_path.exists():
            combined_manifest.last_finetune = record
            self._save_manifest(combined_manifest, self.combined_manifest_path)
        logger.info(
            "Recorded fine-tune: checkpoint=%s size=%d", checkpoint, size
        )

    def iter_examples(self, include_private: bool | None = None) -> list[tuple[Path, str]]:
        """Return (path, label) tuples for all training corpus examples.

        Parameters
        ----------
        include_private:
            If None, uses ``self.include_private``.  Pass True/False to override.
        """
        if include_private is None:
            include_private = self.include_private
        examples = []

        # Public flat subdirectories
        for subdir, label in PUBLIC_LABEL_MAP.items():
            d = self.corpus_dir / subdir
            if not d.is_dir():
                continue
            for p in sorted(d.rglob("*")):
                if p.is_file() and p.suffix in SUPPORTED_EXTENSIONS:
                    examples.append((p, label))

        # graph_injection/ — nested structure: RULE-ID/{malicious,benign}/
        graph_dir = self.corpus_dir / "graph_injection"
        if graph_dir.is_dir():
            for rule_dir in sorted(graph_dir.iterdir()):
                if not rule_dir.is_dir():
                    continue
                for polarity in ("malicious", "benign"):
                    sub = rule_dir / polarity
                    if not sub.is_dir():
                        continue
                    label = "injection" if polarity == "malicious" else "benign"
                    for p in sorted(sub.rglob("*")):
                        if p.is_file() and p.suffix in SUPPORTED_EXTENSIONS:
                            examples.append((p, label))

        # Private subdirectories (only when include_private is True)
        if include_private:
            for subdir, label in PRIVATE_LABEL_MAP.items():
                d = self.corpus_dir / subdir
                if not d.is_dir():
                    continue
                for p in sorted(d.rglob("*")):
                    if p.is_file() and p.suffix in SUPPORTED_EXTENSIONS:
                        # Skip manifest files that were rsync'd in
                        if p.name in ("MANIFEST.json", "manifest.json"):
                            continue
                        examples.append((p, label))

        # held_out_eval/ is intentionally excluded from iter_examples()
        # It is only used by the evaluation step in finetune_modal.py

        return examples

    def iter_eval_examples(self) -> list[tuple[Path, str]]:
        """Return (path, label) tuples for the held-out evaluation set only.

        The label is inferred from the filename prefix: files starting with
        'benign' are labeled 'benign'; all others are labeled 'injection'.
        """
        eval_dir = self.corpus_dir / "held_out_eval"
        if not eval_dir.is_dir():
            return []
        examples = []
        for p in sorted(eval_dir.rglob("*")):
            if not p.is_file() or p.suffix not in SUPPORTED_EXTENSIONS:
                continue
            label = "benign" if p.name.startswith("benign") else "injection"
            examples.append((p, label))
        return examples

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_index(self, include_private: bool = False) -> dict[str, str]:
        """Return {relative_path: sha256} for every training corpus file."""
        index: dict[str, str] = {}
        for path, _label in self.iter_examples(include_private=include_private):
            rel = str(path.relative_to(self.corpus_dir))
            index[rel] = _sha256(path)
        return index

    def _load_manifest(self, path: Path) -> CorpusManifest:
        if not path.exists():
            return CorpusManifest()
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            return CorpusManifest.from_dict(raw)
        except Exception as exc:
            logger.warning("Failed to load manifest %s: %s — starting fresh", path, exc)
            return CorpusManifest()

    def _build_manifest(
        self, new_index: dict[str, str], old: CorpusManifest
    ) -> CorpusManifest:
        label_counts: dict[str, int] = {}
        for rel_path in new_index:
            top = rel_path.split("/")[0]
            # graph_injection nested: rel_path is graph_injection/RULE/polarity/file
            if top == "graph_injection":
                parts = rel_path.split("/")
                polarity = parts[2] if len(parts) >= 3 else "malicious"
                label = "injection" if polarity == "malicious" else "benign"
            else:
                label = PUBLIC_LABEL_MAP.get(top) or PRIVATE_LABEL_MAP.get(top, "unknown")
            label_counts[label] = label_counts.get(label, 0) + 1

        return CorpusManifest(
            version=MANIFEST_VERSION,
            last_updated=_now_iso(),
            total_examples=len(new_index),
            label_counts=label_counts,
            sha256_index=new_index,
            last_finetune=old.last_finetune,
        )

    def _evaluate(self, old: CorpusManifest, new: CorpusManifest) -> UpdateDecision:
        old_index = old.sha256_index
        new_index = new.sha256_index

        old_keys = set(old_index.keys())
        new_keys = set(new_index.keys())

        added = new_keys - old_keys
        removed = old_keys - new_keys
        changed = {
            k for k in old_keys & new_keys if old_index[k] != new_index[k]
        }

        corpus_before = old.last_finetune.corpus_size_at_finetune or old.total_examples
        corpus_after = new.total_examples
        delta_total = len(added) + len(changed)

        delta_pct = (delta_total / corpus_before) if corpus_before > 0 else 1.0

        absolute_trigger = delta_total >= self.min_new_examples
        relative_trigger = delta_pct >= self.min_delta_pct

        should_retrain = absolute_trigger or relative_trigger

        if should_retrain:
            if absolute_trigger and relative_trigger:
                reason = (
                    f"Both thresholds crossed: {delta_total} new/changed examples "
                    f"(≥{self.min_new_examples}) and {delta_pct:.1%} growth "
                    f"(≥{self.min_delta_pct:.0%})."
                )
            elif absolute_trigger:
                reason = (
                    f"Absolute threshold crossed: {delta_total} new/changed examples "
                    f"(≥{self.min_new_examples})."
                )
            else:
                reason = (
                    f"Relative threshold crossed: {delta_pct:.1%} corpus growth "
                    f"(≥{self.min_delta_pct:.0%})."
                )
        else:
            reason = (
                f"Below both thresholds: {delta_total} new/changed examples "
                f"(need {self.min_new_examples}) and {delta_pct:.1%} growth "
                f"(need {self.min_delta_pct:.0%})."
            )

        return UpdateDecision(
            should_retrain=should_retrain,
            new_examples=len(added),
            changed_examples=len(changed),
            removed_examples=len(removed),
            corpus_size_before=corpus_before,
            corpus_size_after=corpus_after,
            delta_pct=delta_pct,
            reason=reason,
        )

    def _save_manifest(self, manifest: CorpusManifest, path: Path) -> None:
        path.write_text(
            json.dumps(manifest.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")
