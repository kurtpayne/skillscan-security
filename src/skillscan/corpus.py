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

3. **CLI integration**: ``skillscan corpus sync`` and ``skillscan corpus status``
   subcommands are wired in via ``cli.py``.

Environment variables
---------------------
``SKILLSCAN_CORPUS_DIR``      — override the default ``corpus/`` path.
``SKILLSCAN_MIN_NEW_EXAMPLES`` — override the absolute delta threshold.
``SKILLSCAN_MIN_DELTA_PCT``   — override the relative delta threshold (0–1 float).
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
MANIFEST_VERSION = 1

# Subdirectory → label mapping
LABEL_MAP: dict[str, str] = {
    "benign": "benign",
    "malicious": "injection",
    "prompt_injection": "injection",
}

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
    """Manages the training corpus and decides when to trigger fine-tuning."""

    def __init__(
        self,
        corpus_dir: Path | None = None,
        min_new_examples: int = DEFAULT_MIN_NEW_EXAMPLES,
        min_delta_pct: float = DEFAULT_MIN_DELTA_PCT,
    ) -> None:
        env_dir = os.getenv("SKILLSCAN_CORPUS_DIR")
        if corpus_dir is None and env_dir:
            corpus_dir = Path(env_dir)
        if corpus_dir is None:
            # Default: corpus/ sibling of the package root
            corpus_dir = Path(__file__).parent.parent.parent / "corpus"
        self.corpus_dir = corpus_dir.resolve()
        self.manifest_path = self.corpus_dir / MANIFEST_FILENAME
        self.min_new_examples = min_new_examples
        self.min_delta_pct = min_delta_pct

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def sync(self) -> UpdateDecision:
        """Scan corpus, update manifest, and return an UpdateDecision."""
        old_manifest = self._load_manifest()
        new_index = self._build_index()
        new_manifest = self._build_manifest(new_index, old_manifest)
        decision = self._evaluate(old_manifest, new_manifest)
        self._save_manifest(new_manifest)
        logger.info(decision.summary())
        return decision

    def status(self) -> dict[str, Any]:
        """Return a human-readable status dict without modifying the manifest."""
        manifest = self._load_manifest()
        current_index = self._build_index()
        current_size = len(current_index)
        return {
            "corpus_dir": str(self.corpus_dir),
            "manifest_exists": self.manifest_path.exists(),
            "current_examples": current_size,
            "manifest_examples": manifest.total_examples,
            "label_counts": manifest.label_counts,
            "last_updated": manifest.last_updated,
            "last_finetune": asdict(manifest.last_finetune),
            "thresholds": {
                "min_new_examples": self.min_new_examples,
                "min_delta_pct": self.min_delta_pct,
            },
        }

    def record_finetune(self, checkpoint: str) -> None:
        """Update the manifest to record a completed fine-tune run."""
        manifest = self._load_manifest()
        manifest.last_finetune = FineTuneRecord(
            timestamp=_now_iso(),
            corpus_size_at_finetune=manifest.total_examples,
            model_checkpoint=checkpoint,
        )
        self._save_manifest(manifest)
        logger.info("Recorded fine-tune: checkpoint=%s size=%d", checkpoint, manifest.total_examples)

    def iter_examples(self) -> list[tuple[Path, str]]:
        """Yield (path, label) tuples for all corpus examples."""
        examples = []
        for subdir, label in LABEL_MAP.items():
            d = self.corpus_dir / subdir
            if not d.is_dir():
                continue
            for p in sorted(d.rglob("*")):
                if p.is_file() and p.suffix in SUPPORTED_EXTENSIONS:
                    examples.append((p, label))
        return examples

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_index(self) -> dict[str, str]:
        """Return {relative_path: sha256} for every corpus file."""
        index: dict[str, str] = {}
        for path, _label in self.iter_examples():
            rel = str(path.relative_to(self.corpus_dir))
            index[rel] = _sha256(path)
        return index

    def _load_manifest(self) -> CorpusManifest:
        if not self.manifest_path.exists():
            return CorpusManifest()
        try:
            raw = json.loads(self.manifest_path.read_text(encoding="utf-8"))
            return CorpusManifest.from_dict(raw)
        except Exception as exc:
            logger.warning("Failed to load manifest: %s — starting fresh", exc)
            return CorpusManifest()

    def _build_manifest(
        self, new_index: dict[str, str], old: CorpusManifest
    ) -> CorpusManifest:
        label_counts: dict[str, int] = {}
        for rel_path in new_index:
            subdir = rel_path.split("/")[0]
            label = LABEL_MAP.get(subdir, "unknown")
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

    def _save_manifest(self, manifest: CorpusManifest) -> None:
        self.manifest_path.write_text(
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
