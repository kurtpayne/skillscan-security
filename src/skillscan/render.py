from __future__ import annotations

from collections import Counter

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from skillscan.models import Finding, ScanReport, Verdict, confidence_label

VERDICT_STYLE = {
    Verdict.ALLOW: "bold green",
    Verdict.WARN: "bold yellow",
    Verdict.BLOCK: "bold red",
}


def _finding_narrative(finding: Finding) -> tuple[str, str, str]:
    clabel = confidence_label(finding.confidence)
    why = f"Matched {finding.id} ({finding.category}) [{clabel.value} confidence]"
    impact = f"Potential {finding.severity.value}-severity security risk"
    next_action = finding.mitigation or "Review the flagged snippet and remove/contain risky behavior"
    return why, impact, next_action




def _recommended_actions(report: ScanReport, limit: int = 3) -> list[str]:
    actions: list[str] = []
    for finding in report.findings:
        _, _, next_action = _finding_narrative(finding)
        next_action = next_action.strip()
        if next_action and next_action not in actions:
            actions.append(next_action)
        if len(actions) >= limit:
            break
    return actions


def _category_counts(report: ScanReport) -> list[tuple[str, int]]:
    counts = Counter(f.category for f in report.findings)
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))

def render_report(report: ScanReport, console: Console | None = None) -> None:
    console = console or Console()

    summary = (
        f"[bold]Target:[/bold] {report.metadata.target}\n"
        f"[bold]Policy:[/bold] {report.metadata.policy_profile}\n"
        f"[bold]Ecosystems:[/bold] {', '.join(report.metadata.ecosystem_hints)}\n"
        f"[bold]Score:[/bold] {report.score}\n"
        f"[bold]Findings:[/bold] {len(report.findings)}"
    )
    console.print(
        Panel(
            summary,
            title=f"Verdict: [{VERDICT_STYLE[report.verdict]}]{report.verdict.value.upper()}[/]",
            border_style=VERDICT_STYLE[report.verdict],
        )
    )

    findings = Table(title="Top Findings", show_lines=True)
    findings.add_column("ID", style="cyan")
    findings.add_column("Severity")
    findings.add_column("Category")
    findings.add_column("Evidence")
    findings.add_column("Confidence", style="dim")
    findings.add_column("Snippet")
    findings.add_column("Why")
    findings.add_column("Impact")
    findings.add_column("Next Action")
    for finding in report.findings[:20]:
        why, impact, next_action = _finding_narrative(finding)
        findings.add_row(
            finding.id,
            finding.severity.value,
            finding.category,
            f"{finding.evidence_path}:{finding.line or '-'}",
            confidence_label(finding.confidence).value,
            finding.snippet[:90],
            why[:80],
            impact[:80],
            next_action[:110],
        )
    if report.findings:
        console.print(findings)

    categories = _category_counts(report)
    if categories:
        cat = Table(title="Finding Categories")
        cat.add_column("Category", style="magenta")
        cat.add_column("Count", justify="right")
        for name, count in categories:
            cat.add_row(name, str(count))
        console.print(cat)

    actions = _recommended_actions(report)
    if actions:
        action_lines = "\n".join(f"{idx+1}. {line}" for idx, line in enumerate(actions))
        console.print(Panel(action_lines, title="Recommended Actions"))

    if report.ai_assessment is not None:
        ai_summary = (
            f"[bold]Provider:[/bold] {report.ai_assessment.provider}\n"
            f"[bold]Model:[/bold] {report.ai_assessment.model}\n"
            f"[bold]Prompt Version:[/bold] {report.ai_assessment.prompt_version}\n"
            f"[bold]AI Findings Added:[/bold] {report.ai_assessment.findings_added}\n"
            f"[bold]Summary:[/bold] {report.ai_assessment.summary}"
        )
        console.print(Panel(ai_summary, title="AI Assist"))

    caps = Table(title="Capabilities")
    caps.add_column("Capability", style="magenta")
    caps.add_column("Evidence")
    for cap in report.capabilities[:20]:
        caps.add_row(cap.name, cap.evidence_path)
    if report.capabilities:
        console.print(caps)

    ioc = Table(title="Network Indicators")
    ioc.add_column("Type")
    ioc.add_column("Value")
    ioc.add_column("Listed")
    ioc.add_column("Source")
    for entry in report.iocs[:30]:
        ioc.add_row(entry.kind, entry.value, "yes" if entry.listed else "no", entry.source_path)
    if report.iocs:
        console.print(ioc)

    dep = Table(title="Dependency Vulnerabilities")
    dep.add_column("Ecosystem")
    dep.add_column("Package")
    dep.add_column("Version")
    dep.add_column("Vuln")
    dep.add_column("Severity")
    dep.add_column("Fixed")
    for d in report.dependency_findings:
        dep.add_row(
            d.ecosystem,
            d.name,
            d.version,
            d.vulnerability_id,
            d.severity.value,
            d.fixed_version or "-",
        )
    if report.dependency_findings:
        console.print(dep)
