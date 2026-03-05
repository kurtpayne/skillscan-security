from __future__ import annotations

from skillscan.compact import report_to_compact_text
from skillscan.models import Finding, ScanMetadata, ScanReport, Severity, Verdict


def test_compact_render() -> None:
    report = ScanReport(
        metadata=ScanMetadata(
            scanner_version="0.1.0",
            target="x",
            target_type="directory",
            ecosystem_hints=["generic"],
            rulepack_version="x",
            policy_profile="strict",
            policy_source="builtin:strict",
            intel_sources=[],
        ),
        verdict=Verdict.BLOCK,
        score=50,
        findings=[
            Finding(
                id="ABU-001",
                category="instruction_abuse",
                severity=Severity.HIGH,
                confidence=0.8,
                title="abuse",
                evidence_path="SKILL.md",
                line=2,
                snippet="ignore previous",
            )
        ],
        iocs=[],
        dependency_findings=[],
        capabilities=[],
    )

    text = report_to_compact_text(report)
    assert "verdict=block" in text
    assert "ABU-001" in text
    assert "SKILL.md:2" in text
