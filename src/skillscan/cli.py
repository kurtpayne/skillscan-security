from __future__ import annotations

import json
import shutil
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from skillscan import __version__
from skillscan.ai import load_dotenv
from skillscan.analysis import ScanError, scan
from skillscan.compact import report_to_compact_text
from skillscan.intel import (
    add_source,
    clear_runtime,
    data_dir,
    intel_dir,
    load_store,
    remove_source,
    set_enabled,
)
from skillscan.intel_update import sync_managed
from skillscan.junit import report_to_junit_xml
from skillscan.policies import BUILTIN_PROFILES, load_builtin_policy, load_policy_file, policy_summary
from skillscan.render import render_report
from skillscan.sarif import report_to_sarif

app = typer.Typer(help="SkillScan: standalone AI skill security analyzer")
policy_app = typer.Typer(help="Policy operations")
intel_app = typer.Typer(help="Local intel operations")
app.add_typer(policy_app, name="policy")
app.add_typer(intel_app, name="intel")
console = Console()


def _finding_key(finding: dict) -> tuple[str, str, int | None]:
    return (
        finding.get("id", ""),
        finding.get("evidence_path", ""),
        finding.get("line"),
    )


@app.command("version")
def version() -> None:
    console.print(f"skillscan {__version__}")


@app.command("scan")
def scan_cmd(
    target: str = typer.Argument(..., help="Local path or URL to scan"),
    policy_profile: str = typer.Option(
        "strict", "--policy-profile", "--profile", help="Built-in policy profile"
    ),
    policy_file: Path | None = typer.Option(None, "--policy", help="Custom policy file"),
    format: str = typer.Option("text", "--format", help="Output format: text|json|sarif|junit|compact"),
    out: Path | None = typer.Option(None, "--out", help="Write report to file"),
    fail_on: str = typer.Option("block", "--fail-on", help="Exit non-zero on warn or block"),
    auto_intel: bool = typer.Option(True, "--auto-intel/--no-auto-intel", help="Auto-refresh managed intel"),
    intel_max_age_minutes: int = typer.Option(
        60, "--intel-max-age-minutes", help="Auto-intel refresh max age in minutes"
    ),
    url_max_links: int = typer.Option(25, "--url-max-links", help="Maximum links to follow for URL targets"),
    url_same_origin_only: bool = typer.Option(
        True,
        "--url-same-origin-only/--no-url-same-origin-only",
        help="Only follow links on same origin as root URL target",
    ),
    ai_assist: bool = typer.Option(
        False,
        "--ai-assist/--no-ai-assist",
        help="Enable optional AI semantic risk analysis (off by default)",
    ),
    extended_ai_checks: bool | None = typer.Option(
        None,
        "--extended-ai-checks/--no-extended-ai-checks",
        help="Deprecated alias for --ai-assist",
        hidden=True,
    ),
    ai_provider: str = typer.Option(
        "auto",
        "--ai-provider",
        help="AI provider: auto|openai|anthropic|gemini|openai_compatible",
    ),
    ai_model: str | None = typer.Option(None, "--ai-model", help="AI model name"),
    ai_base_url: str | None = typer.Option(
        None,
        "--ai-base-url",
        help="Optional custom API base URL (for self-hosted or proxy endpoints)",
    ),
    ai_timeout_seconds: int = typer.Option(20, "--ai-timeout-seconds", help="AI request timeout in seconds"),
    ai_required: bool = typer.Option(
        False,
        "--ai-required/--ai-optional",
        help="Fail scan if AI assist is requested but unavailable",
    ),
    ai_report_out: Path | None = typer.Option(
        None,
        "--ai-report-out",
        help="Write raw AI JSON response to file for review/audit",
    ),
) -> None:
    load_dotenv()
    if extended_ai_checks is not None:
        ai_assist = extended_ai_checks
    if policy_profile not in BUILTIN_PROFILES:
        console.print(
            f"[bold red]Invalid --policy-profile:[/] {policy_profile}. "
            f"Expected one of: {', '.join(BUILTIN_PROFILES)}"
        )
        raise typer.Exit(2)
    if format not in {"text", "json", "sarif", "junit", "compact"}:
        console.print("[bold red]Invalid --format:[/] expected text, json, sarif, junit, or compact")
        raise typer.Exit(2)
    if fail_on not in {"warn", "block", "never"}:
        console.print("[bold red]Invalid --fail-on:[/] expected warn, block, or never")
        raise typer.Exit(2)
    if intel_max_age_minutes < 1:
        console.print("[bold red]Invalid --intel-max-age-minutes:[/] expected >= 1")
        raise typer.Exit(2)
    if url_max_links < 0:
        console.print("[bold red]Invalid --url-max-links:[/] expected >= 0")
        raise typer.Exit(2)
    if ai_timeout_seconds < 1:
        console.print("[bold red]Invalid --ai-timeout-seconds:[/] expected >= 1")
        raise typer.Exit(2)

    if policy_file:
        policy = load_policy_file(policy_file)
        policy_source = str(policy_file)
    else:
        policy = load_builtin_policy(policy_profile)
        policy_source = f"builtin:{policy_profile}"

    if auto_intel:
        stats = sync_managed(max_age_seconds=intel_max_age_minutes * 60)
        if stats["updated"] > 0 or stats["errors"] > 0:
            console.print(
                f"[dim]intel refresh updated={stats['updated']} "
                f"skipped={stats['skipped']} errors={stats['errors']}[/dim]"
            )

    try:
        report = scan(
            target,
            policy,
            policy_source,
            url_max_links=url_max_links,
            url_same_origin_only=url_same_origin_only,
            ai_assist=ai_assist,
            ai_provider=ai_provider,
            ai_model=ai_model,
            ai_base_url=ai_base_url,
            ai_timeout_seconds=ai_timeout_seconds,
            ai_required=ai_required,
            ai_report_out=ai_report_out,
        )
    except (ScanError, ValueError) as exc:
        console.print(f"[bold red]Scan failed:[/] {exc}")
        raise typer.Exit(2)

    if format == "json":
        payload = report.to_json()
        if out:
            out.write_text(payload, encoding="utf-8")
            console.print(f"Wrote report to {out}")
        else:
            console.print(payload)
    elif format == "sarif":
        payload = json.dumps(report_to_sarif(report), indent=2)
        if out:
            out.write_text(payload, encoding="utf-8")
            console.print(f"Wrote report to {out}")
        else:
            console.print(payload)
    elif format == "junit":
        payload = report_to_junit_xml(report)
        if out:
            out.write_text(payload, encoding="utf-8")
            console.print(f"Wrote report to {out}")
        else:
            console.print(payload)
    elif format == "compact":
        payload = report_to_compact_text(report)
        if out:
            out.write_text(payload, encoding="utf-8")
            console.print(f"Wrote report to {out}")
        else:
            console.print(payload)
    else:
        render_report(report, console=console)
        if out:
            out.write_text(report.to_json(), encoding="utf-8")
            console.print(f"[cyan]Saved JSON report:[/] {out}")

    if fail_on == "warn" and report.verdict.value in {"warn", "block"}:
        raise typer.Exit(1)
    if fail_on == "block" and report.verdict.value == "block":
        raise typer.Exit(1)


@app.command("explain")
def explain_cmd(report: Path = typer.Argument(..., exists=True, readable=True)) -> None:
    data = json.loads(report.read_text(encoding="utf-8"))
    from skillscan.models import ScanReport

    render_report(ScanReport.model_validate(data), console=console)


@app.command("diff")
def diff_cmd(
    baseline: Path = typer.Argument(..., exists=True, readable=True, help="Baseline report JSON"),
    current: Path = typer.Argument(..., exists=True, readable=True, help="Current report JSON"),
    format: str = typer.Option("text", "--format", help="Output format: text|json"),
) -> None:
    if format not in {"text", "json"}:
        console.print("[bold red]Invalid --format:[/] expected text or json")
        raise typer.Exit(2)

    baseline_data = json.loads(baseline.read_text(encoding="utf-8"))
    current_data = json.loads(current.read_text(encoding="utf-8"))

    baseline_findings = baseline_data.get("findings", [])
    current_findings = current_data.get("findings", [])

    baseline_map = {_finding_key(f): f for f in baseline_findings}
    current_map = {_finding_key(f): f for f in current_findings}

    new_keys = sorted(set(current_map) - set(baseline_map))
    resolved_keys = sorted(set(baseline_map) - set(current_map))
    persistent_keys = sorted(set(baseline_map) & set(current_map))

    payload = {
        "baseline": str(baseline),
        "current": str(current),
        "new_count": len(new_keys),
        "resolved_count": len(resolved_keys),
        "persistent_count": len(persistent_keys),
        "new": [current_map[k] for k in new_keys],
        "resolved": [baseline_map[k] for k in resolved_keys],
    }

    if format == "json":
        console.print(json.dumps(payload, indent=2))
        return

    console.print(
        Panel(
            (
                f"[bold]Baseline:[/bold] {baseline}\n"
                f"[bold]Current:[/bold] {current}\n"
                f"[bold green]New:[/bold green] {len(new_keys)}\n"
                f"[bold yellow]Resolved:[/bold yellow] {len(resolved_keys)}\n"
                f"[bold cyan]Persistent:[/bold cyan] {len(persistent_keys)}"
            ),
            title="SkillScan Diff",
        )
    )


@policy_app.command("show-default")
def show_default(profile: str = typer.Option("strict", "--profile")) -> None:
    policy = load_builtin_policy(profile)
    console.print(Panel(policy.model_dump_json(indent=2), title=policy.name))


@policy_app.command("validate")
def validate(path: Path = typer.Argument(..., exists=True, readable=True)) -> None:
    policy = load_policy_file(path)
    console.print(f"[green]Valid policy:[/] {policy_summary(policy)}")


@intel_app.command("status")
def intel_status() -> None:
    store = load_store()
    console.print(f"Intel root: {intel_dir()}")
    console.print(f"Sources: {len(store.sources)}")
    for source in store.sources:
        p = Path(source.path)
        mtime = p.stat().st_mtime if p.exists() else 0
        console.print(
            f"- {source.name} ({source.kind}) "
            f"enabled={source.enabled} path={source.path} mtime={mtime}"
        )


@intel_app.command("list")
def intel_list() -> None:
    store = load_store()
    for source in store.sources:
        console.print(f"{source.name}\t{source.kind}\tenabled={source.enabled}\t{source.path}")


@intel_app.command("add")
def intel_add(
    path: Path = typer.Argument(..., exists=True, readable=True),
    type: str = typer.Option(..., "--type", help="ioc|vuln|rules"),
    name: str = typer.Option(..., "--name", help="Source name"),
) -> None:
    source = add_source(name=name, kind=type, source_path=path)
    console.print(f"Added intel source: {source.name} ({source.kind})")


@intel_app.command("remove")
def intel_remove(name: str = typer.Argument(...)) -> None:
    ok = remove_source(name)
    if not ok:
        raise typer.Exit(1)
    console.print(f"Removed intel source: {name}")


@intel_app.command("enable")
def intel_enable(name: str = typer.Argument(...)) -> None:
    if not set_enabled(name, True):
        raise typer.Exit(1)
    console.print(f"Enabled: {name}")


@intel_app.command("disable")
def intel_disable(name: str = typer.Argument(...)) -> None:
    if not set_enabled(name, False):
        raise typer.Exit(1)
    console.print(f"Disabled: {name}")


@intel_app.command("rebuild")
def intel_rebuild() -> None:
    store = load_store()
    console.print(f"Rebuilt intel index ({len(store.sources)} sources)")


@intel_app.command("sync")
def intel_sync(
    force: bool = typer.Option(False, "--force", help="Force refresh even if data is fresh"),
    max_age_minutes: int = typer.Option(60, "--max-age-minutes", help="Refresh age threshold in minutes"),
) -> None:
    if max_age_minutes < 1:
        raise typer.Exit(2)
    stats = sync_managed(max_age_seconds=max_age_minutes * 60, force=force)
    console.print(
        f"Managed intel sync complete: updated={stats['updated']} "
        f"skipped={stats['skipped']} errors={stats['errors']}"
    )


@app.command("uninstall")
def uninstall(
    keep_data: bool = typer.Option(False, "--keep-data", help="Keep .skillscan data on disk"),
) -> None:
    clear_runtime(keep_data=keep_data)

    # Best effort removal for local installer layout.
    runtime = Path.home() / ".skillscan" / "runtime"
    if runtime.exists() and not keep_data:
        shutil.rmtree(runtime, ignore_errors=True)

    bin_path = Path.home() / ".local" / "bin" / "skillscan"
    if bin_path.exists():
        bin_path.unlink(missing_ok=True)

    msg = "SkillScan uninstalled."
    if keep_data:
        msg += f" Data preserved under {data_dir()}"
    console.print(msg)


if __name__ == "__main__":
    app()
