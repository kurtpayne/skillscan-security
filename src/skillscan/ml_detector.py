"""ml_detector.py — Offline HuggingFace-based prompt-injection detector.

Uses protectai/deberta-v3-base-prompt-injection-v2 (Apache 2.0) for high-accuracy
ML-based detection as an optional complement to the deterministic rule engine.

The model is loaded lazily on first call and cached in-process.  Two backends
are supported, selected automatically based on what is installed:

  1. ONNX Runtime (preferred, CPU-only, ~200 MB)
       pip install skillscan-security[ml-onnx]
       requires: optimum[onnxruntime], transformers

  2. PyTorch / Transformers (fallback, ~500 MB)
       pip install skillscan-security[ml]
       requires: transformers, torch

If neither backend is available the detector is silently skipped and an
informational Finding is emitted so the user knows to install the extras.

Model: protectai/deberta-v3-base-prompt-injection-v2
  - Fine-tuned DeBERTa-v3-base for binary prompt-injection classification
  - Labels: 0 = SAFE, 1 = INJECTION
  - Post-training accuracy: 95.25 % (20 k held-out prompts)
  - License: Apache 2.0
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any

from skillscan.models import Finding, Severity

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

_MODEL_ID = "ProtectAI/deberta-v3-base-prompt-injection-v2"
_MAX_LENGTH = 512
_INJECTION_THRESHOLD = 0.70  # minimum score for INJECTION label to fire
_HIGH_THRESHOLD = 0.88       # score above this → HIGH severity, else MEDIUM

# ---------------------------------------------------------------------------
# Lazy singleton cache
# ---------------------------------------------------------------------------
_pipeline_cache: Any = None
_backend_cache: str | None = None   # "onnx" | "transformers" | "unavailable"


def _try_load_onnx() -> Any | None:
    """Attempt to load the ONNX Runtime backend via 🤗 Optimum."""
    try:
        from optimum.onnxruntime import ORTModelForSequenceClassification  # type: ignore[import]
        from transformers import AutoTokenizer, pipeline  # type: ignore[import]

        tokenizer = AutoTokenizer.from_pretrained(_MODEL_ID, subfolder="onnx")
        tokenizer.model_input_names = ["input_ids", "attention_mask"]
        model = ORTModelForSequenceClassification.from_pretrained(
            _MODEL_ID, export=False, subfolder="onnx"
        )
        return pipeline(
            task="text-classification",
            model=model,
            tokenizer=tokenizer,
            truncation=True,
            max_length=_MAX_LENGTH,
        )
    except Exception as exc:
        logger.debug("ONNX backend unavailable: %s", exc)
        return None


def _try_load_transformers() -> Any | None:
    """Attempt to load the PyTorch / Transformers backend."""
    try:
        import torch  # type: ignore[import]
        from transformers import (  # type: ignore[import]
            AutoModelForSequenceClassification,
            AutoTokenizer,
            pipeline,
        )

        tokenizer = AutoTokenizer.from_pretrained(_MODEL_ID)
        model = AutoModelForSequenceClassification.from_pretrained(_MODEL_ID)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        return pipeline(
            "text-classification",
            model=model,
            tokenizer=tokenizer,
            truncation=True,
            max_length=_MAX_LENGTH,
            device=device,
        )
    except Exception as exc:
        logger.debug("Transformers backend unavailable: %s", exc)
        return None


def _get_pipeline() -> tuple[Any | None, str]:
    """Return (pipeline, backend_name).  Results are cached after first call."""
    global _pipeline_cache, _backend_cache
    if _backend_cache is not None:
        return _pipeline_cache, _backend_cache

    pipe = _try_load_onnx()
    if pipe is not None:
        _pipeline_cache, _backend_cache = pipe, "onnx"
        logger.info("ML detector: loaded ONNX backend (%s)", _MODEL_ID)
        return pipe, "onnx"

    pipe = _try_load_transformers()
    if pipe is not None:
        _pipeline_cache, _backend_cache = pipe, "transformers"
        logger.info("ML detector: loaded Transformers backend (%s)", _MODEL_ID)
        return pipe, "transformers"

    _pipeline_cache, _backend_cache = None, "unavailable"
    logger.warning(
        "ML detector: neither optimum[onnxruntime] nor transformers+torch is installed. "
        "Install skillscan-security[ml-onnx] or skillscan-security[ml] to enable."
    )
    return None, "unavailable"


# ---------------------------------------------------------------------------
# Text chunking helpers
# ---------------------------------------------------------------------------

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def _chunk_text(text: str, max_chars: int = 1800) -> list[str]:
    """Split *text* into chunks of at most *max_chars* characters.

    Splitting on sentence boundaries where possible keeps semantic context
    intact and avoids truncating mid-sentence.
    """
    if len(text) <= max_chars:
        return [text]

    sentences = _SENTENCE_SPLIT_RE.split(text)
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for sent in sentences:
        if current_len + len(sent) > max_chars and current:
            chunks.append(" ".join(current))
            current, current_len = [], 0
        current.append(sent)
        current_len += len(sent) + 1

    if current:
        chunks.append(" ".join(current))

    return chunks or [text[:max_chars]]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def ml_prompt_injection_findings(path: Path, text: str) -> list[Finding]:
    """Run the ML classifier on *text* and return zero or one Finding.

    Returns an empty list if:
    - The ML backend is not installed (silently skipped).
    - No chunk scores above the injection threshold.

    Returns a single Finding with id PINJ-ML-001 if injection is detected.
    """
    if not text.strip():
        return []

    pipe, backend = _get_pipeline()

    if backend == "unavailable":
        # Emit a low-severity informational finding so users know ML is off.
        return [
            Finding(
                id="PINJ-ML-UNAVAIL",
                category="prompt_injection_ml",
                severity=Severity.LOW,
                confidence=1.0,
                title="ML prompt-injection detector not available (missing extras)",
                evidence_path=str(path),
                snippet="Install skillscan-security[ml-onnx] or skillscan-security[ml] to enable.",
                mitigation=(
                    "Run: pip install 'skillscan-security[ml-onnx]' "
                    "for the lightweight ONNX backend (recommended), or "
                    "'skillscan-security[ml]' for the PyTorch backend."
                ),
            )
        ]

    assert pipe is not None, "pipe should be set when backend != 'unavailable'"
    chunks = _chunk_text(text)
    best_score = 0.0
    best_snippet = ""

    for chunk in chunks:
        try:
            result = pipe(chunk)
            # result is a list of dicts: [{"label": "INJECTION", "score": 0.97}]
            if not result:
                continue
            item = result[0] if isinstance(result, list) else result
            label: str = item.get("label", "").upper()
            score: float = float(item.get("score", 0.0))

            # Normalise: some model versions use "1" / "INJECTION" for positive class
            is_injection = label in {"INJECTION", "1", "LABEL_1"}
            if not is_injection:
                # score is for the SAFE class — flip it
                score = 1.0 - score

            if score > best_score:
                best_score = score
                # Extract a representative snippet from this chunk
                lines = [ln.strip() for ln in chunk.splitlines() if ln.strip()]
                best_snippet = " | ".join(lines[:2])[:240]
        except Exception as exc:
            logger.debug("ML classifier error on chunk: %s", exc)
            continue

    if best_score < _INJECTION_THRESHOLD:
        return []

    severity = Severity.HIGH if best_score >= _HIGH_THRESHOLD else Severity.MEDIUM
    confidence = round(min(best_score, 0.99), 3)

    return [
        Finding(
            id="PINJ-ML-001",
            category="prompt_injection_ml",
            severity=severity,
            confidence=confidence,
            title="ML-detected prompt-injection intent (DeBERTa classifier)",
            evidence_path=str(path),
            snippet=best_snippet,
            mitigation=(
                "The ML classifier detected language consistent with a prompt-injection attack. "
                "Review the flagged text for override/coercion instructions, hidden directives, "
                "or attempts to exfiltrate secrets. "
                f"Model: {_MODEL_ID} | Backend: {backend} | Score: {confidence:.3f}"
            ),
        )
    ]
