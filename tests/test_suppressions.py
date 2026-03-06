from __future__ import annotations

from pathlib import Path

from skillscan.models import Finding, Severity
from skillscan.suppressions import apply_suppressions


def test_apply_suppressions_active_and_expired(tmp_path: Path) -> None:
    sup = tmp_path / "suppressions.yaml"
    sup.write_text(
        """
- id: ABU-001
  reason: false positive
  expires: 2099-01-01
  evidence_path: a.md
  line: 1
- id: ABU-002
  reason: old suppression
  expires: 2020-01-01
""".strip(),
        encoding="utf-8",
    )

    findings = [
        Finding(
            id="ABU-001",
            category="instruction_abuse",
            severity=Severity.HIGH,
            confidence=0.8,
            title="a",
            evidence_path="a.md",
            line=1,
            snippet="x",
        ),
        Finding(
            id="ABU-002",
            category="instruction_abuse",
            severity=Severity.MEDIUM,
            confidence=0.8,
            title="b",
            evidence_path="b.md",
            line=1,
            snippet="y",
        ),
    ]

    result = apply_suppressions(findings, sup)
    assert result.suppressed_count == 1
    assert result.expired_count == 1
    assert len(result.findings) == 1
    assert result.findings[0].id == "ABU-002"


def test_apply_suppressions_empty_file(tmp_path: Path) -> None:
    sup = tmp_path / "suppressions.yaml"
    sup.write_text("", encoding="utf-8")

    findings = [
        Finding(
            id="ABU-001",
            category="instruction_abuse",
            severity=Severity.HIGH,
            confidence=0.8,
            title="a",
            evidence_path="a.md",
            line=1,
            snippet="x",
        ),
    ]

    result = apply_suppressions(findings, sup)
    assert result.suppressed_count == 0
    assert result.expired_count == 0
    assert len(result.findings) == 1


def test_apply_suppressions_evidence_path_mismatch(tmp_path: Path) -> None:
    sup = tmp_path / "suppressions.yaml"
    sup.write_text(
        """
- id: ABU-001
  reason: scoped suppression
  expires: 2099-01-01
  evidence_path: other.md
""".strip(),
        encoding="utf-8",
    )

    findings = [
        Finding(
            id="ABU-001",
            category="instruction_abuse",
            severity=Severity.HIGH,
            confidence=0.8,
            title="a",
            evidence_path="a.md",
            line=1,
            snippet="x",
        ),
    ]

    result = apply_suppressions(findings, sup)
    assert result.suppressed_count == 0
    assert len(result.findings) == 1


def test_apply_suppressions_line_mismatch(tmp_path: Path) -> None:
    sup = tmp_path / "suppressions.yaml"
    sup.write_text(
        """
- id: ABU-001
  reason: line-scoped suppression
  expires: 2099-01-01
  evidence_path: a.md
  line: 99
""".strip(),
        encoding="utf-8",
    )

    findings = [
        Finding(
            id="ABU-001",
            category="instruction_abuse",
            severity=Severity.HIGH,
            confidence=0.8,
            title="a",
            evidence_path="a.md",
            line=1,
            snippet="x",
        ),
    ]

    result = apply_suppressions(findings, sup)
    assert result.suppressed_count == 0
    assert len(result.findings) == 1
