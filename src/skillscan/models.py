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




class ConfidenceLabel(StrEnum):
    EXPERIMENTAL = "experimental"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


def confidence_label(confidence: float) -> ConfidenceLabel:
    """Map a 0.0-1.0 confidence score to a human-readable label."""
    if confidence < 0.5:
        return ConfidenceLabel.EXPERIMENTAL
    if confidence < 0.7:
        return ConfidenceLabel.LOW
    if confidence < 0.85:
        return ConfidenceLabel.MEDIUM
    return ConfidenceLabel.HIGH


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


class AIAssessment(BaseModel):
    provider: str
    model: str
    summary: str
    findings_added: int
    prompt_version: str = "v1"


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
    ai_assessment: AIAssessment | None = None

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
    ai_block_on_critical: bool = True
    ai_block_min_confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    block_min_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    limits: dict[str, int] = Field(
        default_factory=lambda: {
            "max_files": 4000,
            "max_depth": 8,
            "max_bytes": 200_000_000,
            "timeout_seconds": 60,
        }
    )


def is_archive(path: Path) -> bool:
    return path.suffix.lower() in {".zip", ".tar", ".gz", ".tgz"}
