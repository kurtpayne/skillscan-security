from __future__ import annotations

from skillscan.models import Finding, ScanMetadata, ScanReport, Severity, Verdict
from skillscan.sarif import report_to_sarif


def _base_report(findings: list[Finding]) -> ScanReport:
    return ScanReport(
        metadata=ScanMetadata(
            scanner_version="0.1.0",
            target="examples/showcase/01_download_execute",
            target_type="directory",
            ecosystem_hints=["generic"],
            rulepack_version="test-rulepack",
            policy_profile="strict",
            policy_source="builtin:strict",
            intel_sources=["builtin:ioc_db"],
        ),
        verdict=Verdict.BLOCK,
        score=80,
        findings=findings,
        iocs=[],
        dependency_findings=[],
        capabilities=[],
    )


def test_report_to_sarif_basic() -> None:
    report = _base_report(
        [
            Finding(
                id="MAL-001",
                category="malware_pattern",
                severity=Severity.HIGH,
                confidence=0.9,
                title="Download and execute pattern",
                evidence_path="examples/showcase/01_download_execute/SKILL.md",
                line=3,
                snippet="curl ... | bash",
                mitigation="Do not execute remote scripts directly",
            )
        ]
    )

    sarif = report_to_sarif(report)
    assert sarif["version"] == "2.1.0"
    assert sarif["runs"][0]["tool"]["driver"]["name"] == "skillscan"
    assert sarif["runs"][0]["tool"]["driver"]["rules"][0]["id"] == "MAL-001"

    result = sarif["runs"][0]["results"][0]
    assert result["ruleId"] == "MAL-001"
    assert result["level"] == "error"
    assert result["properties"]["confidenceLabel"] == "critical"
    assert "confidence=critical" in result["message"]["text"]
    assert result["locations"][0]["physicalLocation"]["artifactLocation"]["uri"] == (
        "examples/showcase/01_download_execute/SKILL.md"
    )
    assert result["locations"][0]["physicalLocation"]["region"]["startLine"] == 3


def test_report_to_sarif_level_mapping() -> None:
    report = _base_report(
        [
            Finding(
                id="LOW-001",
                category="misc",
                severity=Severity.LOW,
                confidence=0.7,
                title="Low severity marker",
                evidence_path="a.txt",
                snippet="low",
            ),
            Finding(
                id="MED-001",
                category="misc",
                severity=Severity.MEDIUM,
                confidence=0.7,
                title="Medium severity marker",
                evidence_path="b.txt",
                snippet="medium",
            ),
        ]
    )

    sarif = report_to_sarif(report)
    levels = [r["level"] for r in sarif["runs"][0]["results"]]
    assert levels == ["note", "warning"]
