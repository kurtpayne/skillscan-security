from __future__ import annotations

from rich.console import Console

from skillscan.models import (
    IOC,
    AIAssessment,
    Capability,
    DependencyFinding,
    Finding,
    ScanMetadata,
    ScanReport,
    Severity,
    Verdict,
)
from skillscan.render import _finding_narrative, render_report


def _base_metadata() -> ScanMetadata:
    return ScanMetadata(
        scanner_version="0.1.0",
        target="x",
        target_type="directory",
        ecosystem_hints=["generic"],
        policy_profile="strict",
        policy_source="builtin:strict",
        intel_sources=["builtin:ioc_db"],
    )


def test_render_report_minimal() -> None:
    report = ScanReport(
        metadata=_base_metadata(),
        verdict=Verdict.ALLOW,
        score=0,
        findings=[],
        iocs=[],
        dependency_findings=[],
        capabilities=[],
    )
    console = Console(record=True)
    render_report(report, console=console)
    output = console.export_text()
    assert "Verdict" in output


def test_finding_narrative() -> None:
    finding = Finding(
        id="ABU-001",
        category="instruction_abuse",
        severity=Severity.MEDIUM,
        confidence=0.7,
        title="test",
        evidence_path="a",
        snippet="bad",
        mitigation="explicit fix",
    )
    why, impact, next_action = _finding_narrative(finding)
    assert "ABU-001" in why
    assert "medium" in impact
    assert next_action == "explicit fix"


def test_render_report_full_sections() -> None:
    report = ScanReport(
        metadata=_base_metadata(),
        verdict=Verdict.BLOCK,
        score=100,
        findings=[
            Finding(
                id="IOC-001",
                category="threat_intel",
                severity=Severity.HIGH,
                confidence=0.9,
                title="test",
                evidence_path="a",
                snippet="bad",
                mitigation="remove",
            )
        ],
        iocs=[IOC(value="bad.example", kind="domain", source_path="a", listed=True)],
        dependency_findings=[
            DependencyFinding(
                ecosystem="python",
                name="x",
                version="1",
                vulnerability_id="CVE-1",
                severity=Severity.HIGH,
                fixed_version="2",
            )
        ],
        capabilities=[Capability(name="network_access", evidence_path="a", detail="x")],
        ai_assessment=AIAssessment(
            provider="openai",
            model="gpt-4o-mini",
            summary="extra context",
            findings_added=1,
        ),
    )
    console = Console(record=True)
    render_report(report, console=console)
    output = console.export_text()
    assert "Top Findings" in output
    assert "Action" in output
    assert "Network Indicators" in output
    assert "Dependency Vulnerabilities" in output
    assert "AI Assist" in output
