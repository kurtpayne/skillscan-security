from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import cast

import typer
from rich.console import Console
from rich.panel import Panel

from skillscan import __version__
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
from skillscan.rules import load_builtin_rulepack
from skillscan.sarif import report_to_sarif
from skillscan.suppressions import apply_suppressions


# load_dotenv: reads KEY=VALUE pairs from a .env file into os.environ (no-op if absent)
def _load_dotenv(path: Path = Path(".env")) -> None:
    import os as _os
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#") or "=" not in raw:
            continue
        key, value = raw.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in _os.environ:
            _os.environ[key] = value

app = typer.Typer(help="SkillScan: standalone AI skill security analyzer")
policy_app = typer.Typer(help="Policy operations")
intel_app = typer.Typer(help="Local intel operations")
rule_app = typer.Typer(help="Rule metadata/query operations")
corpus_app = typer.Typer(help="Training corpus management")
model_app = typer.Typer(help="ML model management (download, update, status)")
app.add_typer(policy_app, name="policy")
app.add_typer(intel_app, name="intel")
app.add_typer(rule_app, name="rule")
app.add_typer(corpus_app, name="corpus")
app.add_typer(model_app, name="model")
console = Console()


def _finding_key(finding: dict) -> tuple[str, str, int | None]:
    return (
        finding.get("id", ""),
        finding.get("evidence_path", ""),
        finding.get("line"),
    )


def _safe_ratio(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 1.0
    return numerator / denominator


def _build_delta_payload(baseline_data: dict, current_data: dict, baseline_label: str) -> dict:
    baseline_findings = baseline_data.get("findings", [])
    current_findings = current_data.get("findings", [])

    baseline_map = {_finding_key(f): f for f in baseline_findings}
    current_map = {_finding_key(f): f for f in current_findings}

    new_keys = sorted(set(current_map) - set(baseline_map))
    resolved_keys = sorted(set(baseline_map) - set(current_map))
    persistent_keys = sorted(set(baseline_map) & set(current_map))

    return {
        "baseline": baseline_label,
        "new_count": len(new_keys),
        "resolved_count": len(resolved_keys),
        "persistent_count": len(persistent_keys),
        "new": [current_map[k] for k in new_keys],
        "resolved": [baseline_map[k] for k in resolved_keys],
    }


@app.command("version")
def version() -> None:
    console.print(f"skillscan-security {__version__}")


@rule_app.command("list")
def rule_list(
    channel: str = typer.Option("stable", "--channel", help="Rulepack channel: stable|preview|labs"),
    format: str = typer.Option("text", "--format", help="Output format: text|json"),
    technique: str | None = typer.Option(None, "--technique", help="Filter by technique id"),
    tag: str | None = typer.Option(None, "--tag", help="Filter by rule metadata tag"),
) -> None:
    if channel not in {"stable", "preview", "labs"}:
        console.print("[bold red]Invalid --channel:[/] expected stable, preview, or labs")
        raise typer.Exit(2)
    if format not in {"text", "json"}:
        console.print("[bold red]Invalid --format:[/] expected text or json")
        raise typer.Exit(2)

    rp = load_builtin_rulepack(channel=channel)
    rows: list[dict[str, object]] = []
    for r in rp.static_rules:
        md = getattr(r, "metadata", None)
        techniques = [t.id for t in (md.techniques if md else [])]
        tags = list(md.tags) if md else []

        if technique and technique not in techniques:
            continue
        if tag and tag not in tags:
            continue

        rows.append(
            {
                "id": r.id,
                "title": r.title,
                "severity": r.severity.value,
                "category": r.category,
                "techniques": techniques,
                "tags": tags,
                "status": (md.status if md else None),
                "version": (md.version if md else None),
            }
        )

    if format == "json":
        console.print_json(json.dumps(rows, indent=2))
        return

    if not rows:
        console.print("No rules matched filter.")
        return

    for row in rows:
        techniques_row = cast(list[str], row["techniques"])
        tags_row = cast(list[str], row["tags"])
        t = ",".join(techniques_row) if techniques_row else "-"
        g = ",".join(tags_row) if tags_row else "-"
        console.print(f"{row['id']} [{row['severity']}] {row['title']}")
        console.print(f"  category={row['category']} techniques={t} tags={g}")


@rule_app.command("sync")
def rule_sync(
    force: bool = typer.Option(False, "--force", help="Force download even if rules are fresh"),
    ttl: int = typer.Option(3600, "--ttl", help="Cache TTL in seconds"),
) -> None:
    """Pull the latest rule signatures from GitHub without reinstalling the package."""
    from skillscan.rules_sync import sync_rules

    result = sync_rules(force=force, ttl=ttl)
    if result.updated:
        console.print(f"[green]Updated:[/] {', '.join(result.updated)}")
    if result.skipped:
        console.print(f"[dim]Skipped (fresh):[/] {', '.join(result.skipped)}")
    if result.errors:
        console.print(f"[red]Errors:[/] {', '.join(result.errors)}")
        raise typer.Exit(1)
    if not result.updated and not result.errors:
        console.print("[dim]Rules are up to date.[/]")


@rule_app.command("status")
def rule_status() -> None:
    """Show the current rule signature versions (bundled vs. user-local)."""
    from skillscan.rules_sync import USER_RULES_DIR, user_rules_version

    rp = load_builtin_rulepack(channel="stable")
    bundled_version = rp.version.split("+")[0]
    user_version = user_rules_version()
    console.print(f"Bundled rules version : {bundled_version}")
    if user_version:
        console.print(f"User-local version    : {user_version} ({USER_RULES_DIR})")
    else:
        console.print("User-local rules      : not synced (run 'skillscan rule sync')")
    total = len(rp.static_rules)
    console.print(f"Total static rules    : {total}")


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
    rulepack_channel: str = typer.Option(
        "stable",
        "--rulepack-channel",
        help="Rulepack channel: stable|preview|labs",
    ),
    suppressions: Path | None = typer.Option(
        None,
        "--suppressions",
        help="Suppression file (YAML) with id/reason/expires and optional evidence_path/line",
    ),
    strict_suppressions: bool = typer.Option(
        False,
        "--strict-suppressions/--no-strict-suppressions",
        help="Fail scan when suppression file contains expired entries",
    ),
    clamav: bool = typer.Option(
        False,
        "--clamav/--no-clamav",
        envvar="SKILLSCAN_CLAMAV",
        help="Enable optional ClamAV artifact scanning stage (also configurable via SKILLSCAN_CLAMAV)",
    ),
    clamav_timeout_seconds: int = typer.Option(
        30,
        "--clamav-timeout-seconds",
        help="ClamAV scan timeout in seconds",
    ),
    ml_detect: bool = typer.Option(
        False,
        "--ml-detect/--no-ml-detect",
        envvar="SKILLSCAN_ML_DETECT",
        help=(
            "Enable offline ML prompt-injection detection using "
            "protectai/deberta-v3-base-prompt-injection-v2 (Apache 2.0). "
            "Requires: pip install 'skillscan-security[ml-onnx]' (ONNX, recommended) "
            "or 'skillscan-security[ml]' (PyTorch). "
            "Also configurable via SKILLSCAN_ML_DETECT env var."
        ),
    ),
    graph_scan: bool | None = typer.Option(
        None,
        "--graph/--no-graph",
        envvar="SKILLSCAN_GRAPH",
        help=(
            "Enable skill graph analysis (default: on for directory targets, off for single files). "
            "Detects remote Markdown loading (PINJ-GRAPH-001), undocumented high-risk tool grants "
            "(PINJ-GRAPH-002), memory/config file poisoning (PINJ-GRAPH-003), and cross-skill "
            "tool escalation (PINJ-GRAPH-004). Use --no-graph to disable explicitly. "
            "Also configurable via SKILLSCAN_GRAPH env var."
        ),
    ),
    baseline_report: Path | None = typer.Option(
        None,
        "--baseline-report",
        help="Baseline report JSON to compare against this scan (new/resolved findings)",
    ),
    delta_format: str = typer.Option(
        "text",
        "--delta-format",
        help="Baseline delta output format: text|json",
    ),
) -> None:
    _load_dotenv()
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
    if rulepack_channel not in {"stable", "preview", "labs"}:
        console.print("[bold red]Invalid --rulepack-channel:[/] expected stable, preview, or labs")
        raise typer.Exit(2)
    if clamav_timeout_seconds < 1:
        console.print("[bold red]Invalid --clamav-timeout-seconds:[/] expected >= 1")
        raise typer.Exit(2)
    if delta_format not in {"text", "json"}:
        console.print("[bold red]Invalid --delta-format:[/] expected text or json")
        raise typer.Exit(2)
    if baseline_report is not None and not baseline_report.exists():
        console.print(f"[bold red]Baseline report not found:[/] {baseline_report}")
        raise typer.Exit(2)
    if baseline_report is not None and format in {"sarif", "junit", "compact"}:
        console.print("[bold red]--baseline-report is supported only with --format text or json[/]")
        raise typer.Exit(2)
    if baseline_report is not None and format == "json" and delta_format != "json":
        console.print("[bold red]When using --format json with --baseline-report, set --delta-format json[/]")
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
    # Auto-sync rule signatures (signature-as-data layer, same TTL as intel)
    from skillscan.rules_sync import maybe_sync_rules

    rules_result = maybe_sync_rules(max_age_seconds=intel_max_age_minutes * 60)
    if rules_result.updated:
        console.print(f"[dim]rules refresh updated={len(rules_result.updated)}[/dim]")
    # Issue J4: auto-enable graph scan for directory targets unless explicitly overridden.
    # graph_scan is None when the user has not passed --graph or --no-graph.
    _resolved_target = Path(target) if not target.startswith(("http://", "https://")) else None
    effective_graph_scan: bool
    if graph_scan is None:
        effective_graph_scan = bool(_resolved_target and _resolved_target.is_dir())
    else:
        effective_graph_scan = graph_scan

    try:
        report = scan(
            target,
            policy,
            policy_source,
            url_max_links=url_max_links,
            url_same_origin_only=url_same_origin_only,
            clamav=clamav,
            clamav_timeout_seconds=clamav_timeout_seconds,
            ml_detect=ml_detect,
            rulepack_channel=rulepack_channel,
            graph_scan=effective_graph_scan,
        )
    except (ScanError, ValueError) as exc:
        console.print(f"[bold red]Scan failed:[/] {exc}")
        raise typer.Exit(2)

    expired_suppressions = 0
    if suppressions is not None:
        if not suppressions.exists():
            console.print(f"[bold red]Suppressions file not found:[/] {suppressions}")
            raise typer.Exit(2)
        try:
            result = apply_suppressions(report.findings, suppressions)
        except ValueError as exc:
            console.print(f"[bold red]Invalid suppressions file:[/] {exc}")
            raise typer.Exit(2)
        report.findings = result.findings
        expired_suppressions = result.expired_count
        console.print(
            "[dim]"
            f"suppressions total={result.total_entries} "
            f"active={result.active_entries} "
            f"applied={result.suppressed_count} "
            f"expired={result.expired_count}"
            "[/dim]"
        )
        if result.expired_entries:
            expired_ids = ", ".join(sorted({entry.id for entry in result.expired_entries}))
            console.print(f"[dim]expired suppression ids: {expired_ids}[/dim]")

    report_dict = report.model_dump(mode="json")
    delta_payload: dict | None = None
    if baseline_report is not None:
        baseline_data = json.loads(baseline_report.read_text(encoding="utf-8"))
        delta_payload = _build_delta_payload(
            baseline_data=baseline_data,
            current_data=report_dict,
            baseline_label=str(baseline_report),
        )

    if format == "json":
        if delta_payload is not None:
            payload = json.dumps({"report": report_dict, "delta": delta_payload}, indent=2)
        else:
            payload = report.to_json()
        if out:
            out.write_text(payload, encoding="utf-8")
            console.print(f"Wrote report to {out}")
        else:
            typer.echo(payload)
    elif format == "sarif":
        payload = json.dumps(report_to_sarif(report), indent=2)
        if out:
            out.write_text(payload, encoding="utf-8")
            console.print(f"Wrote report to {out}")
        else:
            typer.echo(payload)
    elif format == "junit":
        payload = report_to_junit_xml(report)
        if out:
            out.write_text(payload, encoding="utf-8")
            console.print(f"Wrote report to {out}")
        else:
            typer.echo(payload)
    elif format == "compact":
        payload = report_to_compact_text(report)
        if out:
            out.write_text(payload, encoding="utf-8")
            console.print(f"Wrote report to {out}")
        else:
            typer.echo(payload)
    else:
        render_report(report, console=console)
        if delta_payload is not None:
            if delta_format == "json":
                typer.echo(json.dumps(delta_payload, indent=2))
            else:
                console.print(
                    Panel(
                        (
                            f"[bold]Baseline:[/bold] {delta_payload['baseline']}\n"
                            f"[bold green]New:[/bold green] {delta_payload['new_count']}\n"
                            f"[bold yellow]Resolved:[/bold yellow] {delta_payload['resolved_count']}\n"
                            f"[bold cyan]Persistent:[/bold cyan] {delta_payload['persistent_count']}"
                        ),
                        title="Baseline Delta",
                    )
                )
        if out:
            if delta_payload is not None and delta_format == "json":
                out_payload = json.dumps(
                    {"report": report_dict, "delta": delta_payload},
                    indent=2,
                )
                out.write_text(out_payload, encoding="utf-8")
                console.print(f"Wrote report to {out}")
            else:
                out.write_text(report.to_json(), encoding="utf-8")
                console.print(f"[cyan]Saved JSON report:[/] {out}")

    if strict_suppressions and expired_suppressions > 0:
        console.print("[bold red]Expired suppressions found in strict mode[/]")
        raise typer.Exit(1)

    if fail_on == "warn" and report.verdict.value in {"warn", "block"}:
        raise typer.Exit(1)
    if fail_on == "block" and report.verdict.value == "block":
        raise typer.Exit(1)


@app.command("explain")
def explain_cmd(report: Path = typer.Argument(..., exists=True, readable=True)) -> None:
    data = json.loads(report.read_text(encoding="utf-8"))
    from skillscan.models import ScanReport

    render_report(ScanReport.model_validate(data), console=console)


@app.command("benchmark")
def benchmark_cmd(
    manifest: Path = typer.Argument(..., exists=True, readable=True, help="Benchmark manifest JSON"),
    policy_profile: str = typer.Option(
        "strict", "--policy-profile", "--profile", help="Built-in policy profile"
    ),
    format: str = typer.Option("text", "--format", help="Output format: text|json"),
    min_precision: float = typer.Option(0.0, "--min-precision", help="Fail if precision falls below value"),
    min_recall: float = typer.Option(0.0, "--min-recall", help="Fail if recall falls below value"),
) -> None:
    if policy_profile not in BUILTIN_PROFILES:
        console.print(
            f"[bold red]Invalid --policy-profile:[/] {policy_profile}. "
            f"Expected one of: {', '.join(BUILTIN_PROFILES)}"
        )
        raise typer.Exit(2)
    if format not in {"text", "json"}:
        console.print("[bold red]Invalid --format:[/] expected text or json")
        raise typer.Exit(2)
    if not (0.0 <= min_precision <= 1.0):
        console.print("[bold red]Invalid --min-precision:[/] expected 0.0 to 1.0")
        raise typer.Exit(2)
    if not (0.0 <= min_recall <= 1.0):
        console.print("[bold red]Invalid --min-recall:[/] expected 0.0 to 1.0")
        raise typer.Exit(2)

    policy = load_builtin_policy(policy_profile)
    policy_source = f"builtin:{policy_profile}"

    data = json.loads(manifest.read_text(encoding="utf-8"))
    cases = data.get("cases", [])
    if not isinstance(cases, list):
        console.print("[bold red]Invalid manifest:[/] 'cases' must be a list")
        raise typer.Exit(2)

    tp = 0
    fp = 0
    fn = 0
    case_results: list[dict] = []

    for idx, case in enumerate(cases, 1):
        target = case.get("target")
        if not isinstance(target, str):
            console.print(f"[bold red]Invalid case #{idx}:[/] missing string 'target'")
            raise typer.Exit(2)
        expected_ids = set(case.get("expected_ids", []))
        forbidden_ids = set(case.get("forbidden_ids", []))

        try:
            report = scan(
                target,
                policy,
                policy_source,
            )
        except (ScanError, ValueError) as exc:
            console.print(f"[bold red]Benchmark scan failed for {target}:[/] {exc}")
            raise typer.Exit(2)

        found_ids = {f.id for f in report.findings}
        matched = expected_ids & found_ids
        missing = expected_ids - found_ids
        unexpected = forbidden_ids & found_ids

        tp += len(matched)
        fn += len(missing)
        fp += len(unexpected)

        case_results.append(
            {
                "target": target,
                "matched": sorted(matched),
                "missing": sorted(missing),
                "unexpected": sorted(unexpected),
            }
        )

    precision = _safe_ratio(tp, tp + fp)
    recall = _safe_ratio(tp, tp + fn)
    payload = {
        "cases": len(cases),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "results": case_results,
    }

    if format == "json":
        typer.echo(json.dumps(payload, indent=2))
    else:
        console.print(
            f"benchmark cases={payload['cases']} precision={payload['precision']:.4f} "
            f"recall={payload['recall']:.4f} tp={tp} fp={fp} fn={fn}"
        )

    if precision < min_precision or recall < min_recall:
        raise typer.Exit(1)


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
        typer.echo(json.dumps(payload, indent=2))
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


# ---------------------------------------------------------------------------
# Corpus commands
# ---------------------------------------------------------------------------


@corpus_app.command("sync")
def corpus_sync(
    corpus_dir: Path = typer.Option(None, "--corpus-dir", help="Path to corpus/ directory"),
    min_new: int = typer.Option(50, "--min-new", help="Absolute delta threshold"),
    min_pct: float = typer.Option(0.10, "--min-pct", help="Relative delta threshold (0–1)"),
    check: bool = typer.Option(
        False, "--check", help="Exit 2 if retrain not needed (for CI use)"
    ),
) -> None:
    """Sync corpus manifest and evaluate whether a fine-tune should be triggered."""
    from skillscan.corpus import CorpusManager

    mgr = CorpusManager(
        corpus_dir=corpus_dir,
        min_new_examples=min_new,
        min_delta_pct=min_pct,
    )
    decision = mgr.sync()
    console.print(decision.summary())
    if check and not decision.should_retrain:
        raise typer.Exit(code=2)
    if decision.should_retrain:
        console.print("[bold green]\u2713 Fine-tune triggered[/bold green]")
    else:
        console.print("[dim]Fine-tune not needed[/dim]")


@corpus_app.command("status")
def corpus_status(
    corpus_dir: Path = typer.Option(None, "--corpus-dir", help="Path to corpus/ directory"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
) -> None:
    """Show corpus status and last fine-tune record."""
    import json as _json

    from skillscan.corpus import CorpusManager

    mgr = CorpusManager(corpus_dir=corpus_dir)
    status = mgr.status()
    if json_output:
        console.print(_json.dumps(status, indent=2))
    else:
        console.print(f"[bold]Corpus directory:[/bold] {status['corpus_dir']}")
        console.print(f"[bold]Current examples:[/bold] {status['current_examples']}")
        console.print(f"[bold]Label counts:[/bold] {status['label_counts']}")
        console.print(f"[bold]Last updated:[/bold] {status['last_updated'] or 'never'}")
        ft = status["last_finetune"]
        if ft.get("timestamp"):
            console.print(
                f"[bold]Last fine-tune:[/bold] {ft['timestamp']} "
                f"(corpus size: {ft['corpus_size_at_finetune']}, "
                f"checkpoint: {ft['model_checkpoint']})"
            )
        else:
            console.print("[bold]Last fine-tune:[/bold] [dim]never[/dim]")
        console.print(
            f"[bold]Thresholds:[/bold] "
            f"\u2265{status['thresholds']['min_new_examples']} new examples OR "
            f"\u2265{status['thresholds']['min_delta_pct']:.0%} growth"
        )


@corpus_app.command("record-finetune")
def corpus_record_finetune(
    checkpoint: str = typer.Argument(..., help="Path or name of the model checkpoint"),
    corpus_dir: Path = typer.Option(None, "--corpus-dir", help="Path to corpus/ directory"),
) -> None:
    """Record a completed fine-tune run in the corpus manifest."""
    from skillscan.corpus import CorpusManager

    mgr = CorpusManager(corpus_dir=corpus_dir)
    mgr.record_finetune(checkpoint)
    console.print(f"[green]Recorded fine-tune checkpoint:[/green] {checkpoint}")


# ---------------------------------------------------------------------------
# Model commands
# ---------------------------------------------------------------------------


@model_app.command("sync")
def model_sync_cmd(
    repo_id: str = typer.Option(
        "kurtpayne/skillscan-deberta-adapter",
        "--repo",
        help="HuggingFace Hub repo ID for the LoRA adapter",
    ),
    force: bool = typer.Option(False, "--force", help="Re-download even if already up to date"),
) -> None:
    """Download or update the ML prompt-injection adapter from HuggingFace Hub.

    This is the only way to download the model — it is never auto-downloaded.
    The adapter is stored in ~/.skillscan/models/adapter/ (~50 MB).
    """
    from skillscan.model_sync import sync_model

    console.print(f"[bold]Syncing ML adapter from[/bold] {repo_id}...")
    result = sync_model(repo_id=repo_id, force=force, progress=True)
    if result.success:
        if result.downloaded:
            console.print(
                f"[green]\u2713 Downloaded adapter v{result.version}[/green] "
                f"({result.bytes_downloaded // 1024} KB) — {result.message}"
            )
        else:
            console.print(f"[green]\u2713 {result.message}[/green]")
    else:
        console.print(f"[red]\u2717 Sync failed:[/red] {result.message}")
        raise typer.Exit(1)


@model_app.command("status")
def model_status_cmd(
    repo_id: str = typer.Option(
        "kurtpayne/skillscan-deberta-adapter",
        "--repo",
        help="HuggingFace Hub repo ID for the LoRA adapter",
    ),
    check_remote: bool = typer.Option(False, "--check-remote", help="Check HF Hub for updates"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
) -> None:
    """Show the status of the locally cached ML adapter."""
    import json as _json

    from skillscan.model_sync import get_model_status

    status = get_model_status(repo_id=repo_id, check_remote=check_remote)
    if json_output:
        data = {
            "installed": status.installed,
            "version": status.version,
            "age_days": status.age_days,
            "sha256": status.sha256,
            "repo_id": status.repo_id,
            "stale": status.stale,
            "warn": status.warn,
            "update_available": status.update_available,
            "remote_version": status.remote_version,
        }
        console.print(_json.dumps(data, indent=2))
    else:
        console.print(status.summary())
        if status.stale:
            console.print("[yellow]Run: skillscan model sync[/yellow]")
        elif status.warn:
            console.print("[dim]Run: skillscan model sync (optional)[/dim]")


if __name__ == "__main__":
    app()
