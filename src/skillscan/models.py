from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, Field


class Verdict(StrEnum):
    ALLOW = "allow"
    WARN = "warn"
    BLOCK = "block"


class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Finding(BaseModel):
    id: str
    category: str
    severity: Severity
    confidence: float = Field(ge=0.0, le=1.0)
    title: str
    evidence_path: str
    line: int | None = None
    snippet: str = ""
    mitigation: str | None = None
    chain_actions: list[str] = Field(default_factory=list)




class ConfidenceLabel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


def confidence_label(confidence: float) -> ConfidenceLabel:
    """Map a 0.0-1.0 confidence score to a human-readable label."""
    if confidence < 0.5:
        return ConfidenceLabel.LOW
    if confidence < 0.7:
        return ConfidenceLabel.MEDIUM
    if confidence < 0.9:
        return ConfidenceLabel.HIGH
    return ConfidenceLabel.CRITICAL


class IOC(BaseModel):
    value: str
    kind: str
    source_path: str
    listed: bool = False


class DependencyFinding(BaseModel):
    ecosystem: str
    name: str
    version: str
    vulnerability_id: str
    severity: Severity
    fixed_version: str | None = None


class Capability(BaseModel):
    name: str
    evidence_path: str
    detail: str



class ScanMetadata(BaseModel):
    scanner_version: str
    scanned_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    target: str
    target_type: str
    ecosystem_hints: list[str] = Field(default_factory=list)
    rulepack_version: str = "builtin-unknown"
    policy_profile: str
    policy_source: str
    intel_sources: list[str]


class ScanReport(BaseModel):
    metadata: ScanMetadata
    verdict: Verdict
    score: int
    findings: list[Finding]
    iocs: list[IOC]
    dependency_findings: list[DependencyFinding]
    capabilities: list[Capability]

    def to_json(self) -> str:
        return self.model_dump_json(indent=2)


class Policy(BaseModel):
    name: str
    description: str
    thresholds: dict[str, int]
    weights: dict[str, int]
    hard_block_rules: list[str]
    allow_domains: list[str] = Field(default_factory=list)
    block_domains: list[str] = Field(default_factory=list)
    block_min_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    limits: dict[str, int] = Field(
        default_factory=lambda: {
            "max_files": 4000,
            "max_depth": 8,
            "max_bytes": 200_000_000,
            "timeout_seconds": 60,
            "max_binary_artifacts": 500,
            "max_binary_bytes": 100_000_000,
        }
    )


# Magic-byte signatures for archive formats
_ARCHIVE_MAGIC: list[tuple[bytes, str]] = [
    (b"PK\x03\x04", "zip"),        # ZIP / JAR / WHL / NUPKG / APK / WAR
    (b"PK\x05\x06", "zip"),        # empty ZIP
    (b"PK\x07\x08", "zip"),        # spanned ZIP
    (b"\x1f\x8b", "gz"),           # gzip / .tar.gz / .tgz
    (b"BZh", "bz2"),               # bzip2 / .tar.bz2
    (b"\xfd7zXZ\x00", "xz"),      # XZ / .tar.xz
    (b"7z\xbc\xaf'\x1c", "7z"),   # 7-Zip
    (b"Rar!\x1a\x07\x00", "rar"), # RAR v4
    (b"Rar!\x1a\x07\x01\x00", "rar"),  # RAR v5
    (b"\x28\xb5\x2f\xfd", "zst"), # Zstandard
    (b"ustar", "tar"),             # POSIX tar (offset 257, checked separately)
]

_ARCHIVE_EXTENSIONS: frozenset[str] = frozenset({
    ".zip", ".tar", ".gz", ".tgz", ".bz2", ".tbz2", ".xz", ".txz",
    ".7z", ".rar", ".zst", ".tzst",
    ".jar", ".war", ".apk", ".whl", ".nupkg",
})


def _read_magic(path: Path, n: int = 8) -> bytes:
    try:
        with path.open("rb") as fh:
            return fh.read(n)
    except OSError:
        return b""


def detect_archive_format(path: Path) -> str | None:
    """Return a short format string (e.g. 'zip', '7z') or None if not an archive."""
    magic = _read_magic(path, 16)
    for sig, fmt in _ARCHIVE_MAGIC:
        if magic.startswith(sig):
            return fmt
    # POSIX tar has 'ustar' at byte offset 257
    try:
        with path.open("rb") as fh:
            fh.seek(257)
            if fh.read(5) == b"ustar":
                return "tar"
    except OSError:
        pass
    # Fall back to extension for formats with variable magic
    ext = path.suffix.lower()
    if ext in _ARCHIVE_EXTENSIONS:
        return ext.lstrip(".")
    return None


def is_archive(path: Path) -> bool:
    return detect_archive_format(path) is not None
