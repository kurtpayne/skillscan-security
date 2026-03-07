from __future__ import annotations

import json
from pathlib import Path

import yaml
from typer.testing import CliRunner

from skillscan.cli import app

runner = CliRunner()


def test_version_and_policy_commands() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "skillscan" in result.stdout

    show = runner.invoke(app, ["policy", "show-default", "--profile", "strict"])
    assert show.exit_code == 0
    assert "strict" in show.stdout


def test_scan_invalid_options() -> None:
    target = "tests/fixtures/benign/basic_skill"
    invalid_format = runner.invoke(app, ["scan", target, "--format", "bad"])
    assert invalid_format.exit_code == 2

    junit_ok = runner.invoke(
        app,
        ["scan", target, "--format", "junit", "--fail-on", "never", "--no-auto-intel"],
    )
    assert junit_ok.exit_code == 0
    assert "<testsuites>" in junit_ok.stdout

    compact_ok = runner.invoke(
        app,
        ["scan", target, "--format", "compact", "--fail-on", "never", "--no-auto-intel"],
    )
    assert compact_ok.exit_code == 0
    assert "skillscan verdict=" in compact_ok.stdout

    junit_out = Path("/tmp/skillscan-junit.xml")
    if junit_out.exists():
        junit_out.unlink()
    junit_out_result = runner.invoke(
        app,
        [
            "scan",
            target,
            "--format",
            "junit",
            "--out",
            str(junit_out),
            "--fail-on",
            "never",
            "--no-auto-intel",
        ],
    )
    assert junit_out_result.exit_code == 0
    assert "Wrote report to" in junit_out_result.stdout

    compact_out = Path("/tmp/skillscan-compact.txt")
    if compact_out.exists():
        compact_out.unlink()
    compact_out_result = runner.invoke(
        app,
        [
            "scan",
            target,
            "--format",
            "compact",
            "--out",
            str(compact_out),
            "--fail-on",
            "never",
            "--no-auto-intel",
        ],
    )
    assert compact_out_result.exit_code == 0
    assert "Wrote report to" in compact_out_result.stdout

    invalid_fail_on = runner.invoke(app, ["scan", target, "--fail-on", "bad"])
    assert invalid_fail_on.exit_code == 2

    invalid_intel_age = runner.invoke(app, ["scan", target, "--intel-max-age-minutes", "0"])
    assert invalid_intel_age.exit_code == 2
    invalid_url_links = runner.invoke(app, ["scan", target, "--url-max-links", "-1"])
    assert invalid_url_links.exit_code == 2
    invalid_ai_timeout = runner.invoke(app, ["scan", target, "--ai-timeout-seconds", "0"])
    assert invalid_ai_timeout.exit_code == 2

    invalid_rulepack_channel = runner.invoke(app, ["scan", target, "--rulepack-channel", "beta"])
    assert invalid_rulepack_channel.exit_code == 2

    invalid_clamav_timeout = runner.invoke(app, ["scan", target, "--clamav-timeout-seconds", "0"])
    assert invalid_clamav_timeout.exit_code == 2


def test_scan_fail_on_warn_and_block() -> None:
    warn_result = runner.invoke(
        app,
        [
            "scan",
            "examples/showcase/08_unpinned_deps",
            "--no-auto-intel",
            "--fail-on",
            "warn",
        ],
    )
    assert warn_result.exit_code == 1

    block_result = runner.invoke(
        app,
        [
            "scan",
            "examples/showcase/01_download_execute",
            "--no-auto-intel",
            "--fail-on",
            "block",
        ],
    )
    assert block_result.exit_code == 1


def test_scan_json_stdout_and_auto_intel_message(monkeypatch) -> None:
    monkeypatch.setattr(
        "skillscan.cli.sync_managed",
        lambda **_kwargs: {"updated": 1, "skipped": 0, "errors": 0},
    )
    result = runner.invoke(
        app,
        [
            "scan",
            "tests/fixtures/benign/basic_skill",
            "--format",
            "json",
            "--fail-on",
            "never",
        ],
    )
    assert result.exit_code == 0
    assert "intel refresh" in result.stdout
    start = result.stdout.find("{")
    parsed = json.loads(result.stdout[start:])
    assert parsed["metadata"]["target"].endswith("basic_skill")


def test_intel_subcommands(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SKILLSCAN_HOME", str(tmp_path / ".skillscan"))
    sample = tmp_path / "sample.json"
    sample.write_text(json.dumps({"domains": ["z.com"], "ips": [], "urls": []}), encoding="utf-8")

    add = runner.invoke(app, ["intel", "add", str(sample), "--type", "ioc", "--name", "local"])
    assert add.exit_code == 0

    status = runner.invoke(app, ["intel", "status"])
    assert status.exit_code == 0
    assert "Sources: 1" in status.stdout

    listing = runner.invoke(app, ["intel", "list"])
    assert listing.exit_code == 0
    assert "local" in listing.stdout

    disable = runner.invoke(app, ["intel", "disable", "local"])
    assert disable.exit_code == 0

    enable = runner.invoke(app, ["intel", "enable", "local"])
    assert enable.exit_code == 0

    rebuild = runner.invoke(app, ["intel", "rebuild"])
    assert rebuild.exit_code == 0

    sync = runner.invoke(app, ["intel", "sync", "--max-age-minutes", "0"])
    assert sync.exit_code == 2

    monkeypatch.setattr(
        "skillscan.cli.sync_managed",
        lambda **_kwargs: {"updated": 0, "skipped": 1, "errors": 0},
    )
    sync_ok = runner.invoke(app, ["intel", "sync"])
    assert sync_ok.exit_code == 0
    assert "Managed intel sync complete" in sync_ok.stdout

    remove = runner.invoke(app, ["intel", "remove", "local"])
    assert remove.exit_code == 0

    remove_missing = runner.invoke(app, ["intel", "remove", "missing"])
    assert remove_missing.exit_code == 1


def test_policy_validate_and_uninstall(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SKILLSCAN_HOME", str(tmp_path / ".skillscan"))
    policy = tmp_path / "p.yaml"
    policy.write_text(
        """
name: custom
description: custom
thresholds:
  warn: 10
  block: 20
weights:
  malware_pattern: 1
hard_block_rules: []
allow_domains: []
block_domains: []
limits:
  max_files: 100
  max_depth: 3
  max_bytes: 100000
  timeout_seconds: 10
""".strip(),
        encoding="utf-8",
    )

    validate = runner.invoke(app, ["policy", "validate", str(policy)])
    assert validate.exit_code == 0

    bin_dir = tmp_path / ".local" / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
    (bin_dir / "skillscan").write_text("x", encoding="utf-8")

    keep = runner.invoke(app, ["uninstall", "--keep-data"])
    assert keep.exit_code == 0

    no_keep = runner.invoke(app, ["uninstall"])
    assert no_keep.exit_code == 0


def test_scan_passes_url_flags(monkeypatch) -> None:
    calls: dict[str, object] = {}

    def fake_scan(target, policy, policy_source, **kwargs):
        calls["target"] = target
        calls["kwargs"] = kwargs
        return __import__("skillscan.models", fromlist=["ScanReport"]).ScanReport.model_validate(
            {
                "metadata": {
                    "scanner_version": "0.1.0",
                    "target": str(target),
                    "target_type": "url",
                    "ecosystem_hints": ["generic"],
                    "rulepack_version": "x",
                    "policy_profile": "strict",
                    "policy_source": policy_source,
                    "intel_sources": [],
                },
                "verdict": "allow",
                "score": 0,
                "findings": [],
                "iocs": [],
                "dependency_findings": [],
                "capabilities": [],
            }
        )

    monkeypatch.setattr("skillscan.cli.scan", fake_scan)
    result = runner.invoke(
        app,
        [
            "scan",
            "https://example.com/SKILL.md",
            "--url-max-links",
            "50",
            "--no-url-same-origin-only",
            "--fail-on",
            "never",
        ],
    )
    assert result.exit_code == 0
    assert calls["target"] == "https://example.com/SKILL.md"
    kwargs = calls["kwargs"]
    assert kwargs["url_max_links"] == 50
    assert kwargs["url_same_origin_only"] is False


def test_scan_passes_ai_flags(monkeypatch, tmp_path: Path) -> None:
    calls: dict[str, object] = {}

    def fake_scan(target, policy, policy_source, **kwargs):
        calls["target"] = target
        calls["kwargs"] = kwargs
        return __import__("skillscan.models", fromlist=["ScanReport"]).ScanReport.model_validate(
            {
                "metadata": {
                    "scanner_version": "0.1.0",
                    "target": str(target),
                    "target_type": "directory",
                    "ecosystem_hints": ["generic"],
                    "rulepack_version": "x",
                    "policy_profile": "strict",
                    "policy_source": policy_source,
                    "intel_sources": [],
                },
                "verdict": "allow",
                "score": 0,
                "findings": [],
                "iocs": [],
                "dependency_findings": [],
                "capabilities": [],
            }
        )

    monkeypatch.setattr("skillscan.cli.scan", fake_scan)
    ai_out = tmp_path / "ai.json"
    result = runner.invoke(
        app,
        [
            "scan",
            "tests/fixtures/benign/basic_skill",
            "--ai-assist",
            "--ai-provider",
            "anthropic",
            "--ai-model",
            "claude-3-5-sonnet-latest",
            "--ai-base-url",
            "https://api.example.com",
            "--ai-timeout-seconds",
            "15",
            "--ai-required",
            "--ai-report-out",
            str(ai_out),
            "--fail-on",
            "never",
            "--no-auto-intel",
        ],
    )
    assert result.exit_code == 0
    kwargs = calls["kwargs"]
    assert kwargs["ai_assist"] is True
    assert kwargs["ai_provider"] == "anthropic"
    assert kwargs["ai_model"] == "claude-3-5-sonnet-latest"
    assert kwargs["ai_base_url"] == "https://api.example.com"
    assert kwargs["ai_timeout_seconds"] == 15
    assert kwargs["ai_required"] is True
    assert kwargs["ai_report_out"] == ai_out


def test_scan_deprecated_extended_ai_alias(monkeypatch) -> None:
    calls: dict[str, object] = {}

    def fake_scan(target, policy, policy_source, **kwargs):
        calls["kwargs"] = kwargs
        return __import__("skillscan.models", fromlist=["ScanReport"]).ScanReport.model_validate(
            {
                "metadata": {
                    "scanner_version": "0.1.0",
                    "target": str(target),
                    "target_type": "directory",
                    "ecosystem_hints": ["generic"],
                    "rulepack_version": "x",
                    "policy_profile": "strict",
                    "policy_source": policy_source,
                    "intel_sources": [],
                },
                "verdict": "allow",
                "score": 0,
                "findings": [],
                "iocs": [],
                "dependency_findings": [],
                "capabilities": [],
            }
        )

    monkeypatch.setattr("skillscan.cli.scan", fake_scan)
    result = runner.invoke(
        app,
        [
            "scan",
            "tests/fixtures/benign/basic_skill",
            "--extended-ai-checks",
            "--fail-on",
            "never",
            "--no-auto-intel",
        ],
    )
    assert result.exit_code == 0
    assert calls["kwargs"]["ai_assist"] is True


def test_scan_passes_ai_non_blocking_flag(monkeypatch) -> None:
    calls: dict[str, object] = {}

    def fake_scan(target, policy, policy_source, **kwargs):
        calls["kwargs"] = kwargs
        return __import__("skillscan.models", fromlist=["ScanReport"]).ScanReport.model_validate(
            {
                "metadata": {
                    "scanner_version": "0.1.0",
                    "target": str(target),
                    "target_type": "directory",
                    "ecosystem_hints": ["generic"],
                    "rulepack_version": "x",
                    "policy_profile": "strict",
                    "policy_source": policy_source,
                    "intel_sources": [],
                },
                "verdict": "allow",
                "score": 0,
                "findings": [],
                "iocs": [],
                "dependency_findings": [],
                "capabilities": [],
            }
        )

    monkeypatch.setattr("skillscan.cli.scan", fake_scan)
    result = runner.invoke(
        app,
        [
            "scan",
            "tests/fixtures/benign/basic_skill",
            "--ai-assist",
            "--ai-non-blocking",
            "--fail-on",
            "never",
            "--no-auto-intel",
        ],
    )
    assert result.exit_code == 0
    assert calls["kwargs"]["ai_non_blocking"] is True


def test_scan_passes_rulepack_channel(monkeypatch) -> None:
    calls: dict[str, object] = {}

    def fake_scan(target, policy, policy_source, **kwargs):
        calls["kwargs"] = kwargs
        return __import__("skillscan.models", fromlist=["ScanReport"]).ScanReport.model_validate(
            {
                "metadata": {
                    "scanner_version": "0.1.0",
                    "target": str(target),
                    "target_type": "directory",
                    "ecosystem_hints": ["generic"],
                    "rulepack_version": "x",
                    "policy_profile": "strict",
                    "policy_source": policy_source,
                    "intel_sources": [],
                },
                "verdict": "allow",
                "score": 0,
                "findings": [],
                "iocs": [],
                "dependency_findings": [],
                "capabilities": [],
            }
        )

    monkeypatch.setattr("skillscan.cli.scan", fake_scan)
    result = runner.invoke(
        app,
        [
            "scan",
            "tests/fixtures/benign/basic_skill",
            "--rulepack-channel",
            "preview",
            "--fail-on",
            "never",
            "--no-auto-intel",
        ],
    )
    assert result.exit_code == 0
    assert calls["kwargs"]["rulepack_channel"] == "preview"


def test_scan_policy_file_sarif_stdout_and_outfile_and_scan_error(monkeypatch, tmp_path: Path) -> None:
    policy = tmp_path / "policy.yaml"
    policy.write_text(
        yaml.safe_dump(
            {
                "name": "tmp",
                "description": "tmp",
                "thresholds": {"warn": 10, "block": 20},
                "weights": {"malware_pattern": 1},
                "hard_block_rules": [],
            }
        ),
        encoding="utf-8",
    )

    def fake_scan(_target, _policy, policy_source, **_kwargs):
        return __import__("skillscan.models", fromlist=["ScanReport"]).ScanReport.model_validate(
            {
                "metadata": {
                    "scanner_version": "0.1.0",
                    "target": "tests/fixtures/benign/basic_skill",
                    "target_type": "directory",
                    "ecosystem_hints": ["generic"],
                    "rulepack_version": "x",
                    "policy_profile": "strict",
                    "policy_source": policy_source,
                    "intel_sources": [],
                },
                "verdict": "allow",
                "score": 0,
                "findings": [
                    {
                        "id": "MED-001",
                        "category": "misc",
                        "severity": "medium",
                        "confidence": 0.7,
                        "title": "test",
                        "evidence_path": "a.txt",
                        "line": 1,
                        "snippet": "x",
                    }
                ],
                "iocs": [],
                "dependency_findings": [],
                "capabilities": [],
            }
        )

    monkeypatch.setattr("skillscan.cli.scan", fake_scan)
    result = runner.invoke(
        app,
        [
            "scan",
            "tests/fixtures/benign/basic_skill",
            "--policy",
            str(policy),
            "--format",
            "sarif",
            "--fail-on",
            "never",
            "--no-auto-intel",
        ],
    )
    assert result.exit_code == 0
    assert '"version": "2.1.0"' in result.stdout

    sarif_out = tmp_path / "report.sarif"
    out_result = runner.invoke(
        app,
        [
            "scan",
            "tests/fixtures/benign/basic_skill",
            "--policy",
            str(policy),
            "--format",
            "sarif",
            "--out",
            str(sarif_out),
            "--fail-on",
            "never",
            "--no-auto-intel",
        ],
    )
    assert out_result.exit_code == 0
    assert "Wrote report to" in out_result.stdout
    assert sarif_out.exists()

    from skillscan.analysis import ScanError

    monkeypatch.setattr("skillscan.cli.scan", lambda *_a, **_k: (_ for _ in ()).throw(ScanError("boom")))
    failed = runner.invoke(
        app,
        ["scan", "tests/fixtures/benign/basic_skill", "--fail-on", "never", "--no-auto-intel"],
    )
    assert failed.exit_code == 2
    assert "Scan failed" in failed.stdout


def test_scan_with_suppressions_and_strict_expiry(tmp_path: Path) -> None:
    suppressions = tmp_path / "suppressions.yaml"
    suppressions.write_text(
        """
- id: ABU-001
  reason: accepted risk
  expires: 2099-01-01
- id: ABU-999
  reason: expired marker
  expires: 2020-01-01
""".strip(),
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "scan",
            "examples/showcase/03_instruction_abuse",
            "--suppressions",
            str(suppressions),
            "--fail-on",
            "never",
            "--no-auto-intel",
        ],
    )
    assert result.exit_code == 0
    assert "suppressions total=" in result.stdout
    assert "expired suppression ids:" in result.stdout

    strict_result = runner.invoke(
        app,
        [
            "scan",
            "examples/showcase/03_instruction_abuse",
            "--suppressions",
            str(suppressions),
            "--strict-suppressions",
            "--fail-on",
            "never",
            "--no-auto-intel",
        ],
    )
    assert strict_result.exit_code == 1
    assert "Expired suppressions" in strict_result.stdout


def test_scan_with_baseline_report_text_and_json(tmp_path: Path) -> None:
    baseline = tmp_path / "baseline.json"
    baseline.write_text(
        json.dumps(
            {
                "metadata": {
                    "scanner_version": "0.1.0",
                    "target": "x",
                    "target_type": "directory",
                    "ecosystem_hints": ["generic"],
                    "rulepack_version": "x",
                    "policy_profile": "strict",
                    "policy_source": "builtin:strict",
                    "intel_sources": [],
                },
                "verdict": "warn",
                "score": 10,
                "findings": [
                    {
                        "id": "ABU-001",
                        "category": "instruction_abuse",
                        "severity": "high",
                        "confidence": 0.8,
                        "title": "a",
                        "evidence_path": "a.md",
                        "line": 1,
                        "snippet": "x",
                    }
                ],
                "iocs": [],
                "dependency_findings": [],
                "capabilities": [],
            }
        ),
        encoding="utf-8",
    )

    text_result = runner.invoke(
        app,
        [
            "scan",
            "tests/fixtures/benign/basic_skill",
            "--baseline-report",
            str(baseline),
            "--fail-on",
            "never",
            "--no-auto-intel",
        ],
    )
    assert text_result.exit_code == 0
    assert "Baseline Delta" in text_result.stdout

    json_out = tmp_path / "scan-with-delta.json"
    json_result = runner.invoke(
        app,
        [
            "scan",
            "tests/fixtures/benign/basic_skill",
            "--baseline-report",
            str(baseline),
            "--format",
            "json",
            "--delta-format",
            "json",
            "--out",
            str(json_out),
            "--fail-on",
            "never",
            "--no-auto-intel",
        ],
    )
    assert json_result.exit_code == 0
    payload = json.loads(json_out.read_text(encoding="utf-8"))
    assert "report" in payload
    assert "delta" in payload
    assert "new_count" in payload["delta"]


def test_scan_baseline_option_validation_errors(tmp_path: Path) -> None:
    missing = tmp_path / "missing.json"
    missing_result = runner.invoke(
        app,
        [
            "scan",
            "tests/fixtures/benign/basic_skill",
            "--baseline-report",
            str(missing),
            "--fail-on",
            "never",
            "--no-auto-intel",
        ],
    )
    assert missing_result.exit_code == 2
    assert "Baseline report not found" in missing_result.stdout

    baseline = tmp_path / "baseline.json"
    baseline.write_text('{"findings": []}', encoding="utf-8")

    bad_delta_result = runner.invoke(
        app,
        [
            "scan",
            "tests/fixtures/benign/basic_skill",
            "--baseline-report",
            str(baseline),
            "--delta-format",
            "bad",
            "--fail-on",
            "never",
            "--no-auto-intel",
        ],
    )
    assert bad_delta_result.exit_code == 2
    assert "Invalid --delta-format" in bad_delta_result.stdout

    incompatible_format_result = runner.invoke(
        app,
        [
            "scan",
            "tests/fixtures/benign/basic_skill",
            "--baseline-report",
            str(baseline),
            "--format",
            "sarif",
            "--fail-on",
            "never",
            "--no-auto-intel",
        ],
    )
    assert incompatible_format_result.exit_code == 2
    assert "--baseline-report is supported only" in incompatible_format_result.stdout

    json_without_delta_json_result = runner.invoke(
        app,
        [
            "scan",
            "tests/fixtures/benign/basic_skill",
            "--baseline-report",
            str(baseline),
            "--format",
            "json",
            "--fail-on",
            "never",
            "--no-auto-intel",
        ],
    )
    assert json_without_delta_json_result.exit_code == 2
    assert "set --delta-format json" in json_without_delta_json_result.stdout


def test_scan_with_suppressions_no_expired_ids_line(tmp_path: Path) -> None:
    suppressions = tmp_path / "suppressions.yaml"
    suppressions.write_text(
        """
- id: ABU-001
  reason: accepted risk
  expires: 2099-01-01
""".strip(),
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "scan",
            "examples/showcase/03_instruction_abuse",
            "--suppressions",
            str(suppressions),
            "--fail-on",
            "never",
            "--no-auto-intel",
        ],
    )
    assert result.exit_code == 0
    assert "suppressions total=" in result.stdout
    assert "expired suppression ids:" not in result.stdout


def test_scan_invalid_suppressions_file_reports_error(tmp_path: Path) -> None:
    suppressions = tmp_path / "bad-suppressions.yaml"
    suppressions.write_text(
        """
- id: ABU-001
  reason: missing expires
""".strip(),
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "scan",
            "examples/showcase/03_instruction_abuse",
            "--suppressions",
            str(suppressions),
            "--fail-on",
            "never",
            "--no-auto-intel",
        ],
    )
    assert result.exit_code == 2
    assert "Invalid suppressions file" in result.stdout


def test_scan_text_out_and_intel_enable_disable_fail(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr("skillscan.cli.set_enabled", lambda _name, _enabled: False)
    en = runner.invoke(app, ["intel", "enable", "missing"])
    dis = runner.invoke(app, ["intel", "disable", "missing"])
    assert en.exit_code == 1
    assert dis.exit_code == 1

    out = tmp_path / "out.json"
    result = runner.invoke(
        app,
        [
            "scan",
            "tests/fixtures/benign/basic_skill",
            "--out",
            str(out),
            "--fail-on",
            "never",
            "--no-auto-intel",
        ],
    )
    assert result.exit_code == 0
    assert out.exists()


def test_benchmark_command_outputs_json_and_passes_thresholds(monkeypatch, tmp_path: Path) -> None:
    class _F:
        def __init__(self, id: str):
            self.id = id

    class _R:
        def __init__(self, ids: list[str]):
            self.findings = [_F(i) for i in ids]

    def fake_scan(target, _policy, _policy_source, **_kwargs):
        if target == "a":
            return _R(["MAL-001", "EXF-001"])
        return _R(["SAFE-001"])

    monkeypatch.setattr("skillscan.cli.scan", fake_scan)

    manifest = tmp_path / "bench.json"
    manifest.write_text(
        json.dumps(
            {
                "cases": [
                    {"target": "a", "expected_ids": ["MAL-001"], "forbidden_ids": ["BAD-001"]},
                    {"target": "b", "expected_ids": [], "forbidden_ids": ["MAL-001"]},
                ]
            }
        ),
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "benchmark",
            str(manifest),
            "--format",
            "json",
            "--min-precision",
            "0.9",
            "--min-recall",
            "1.0",
        ],
    )
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["tp"] == 1
    assert payload["fp"] == 0
    assert payload["fn"] == 0


def test_benchmark_command_fails_threshold_gate(monkeypatch, tmp_path: Path) -> None:
    class _F:
        def __init__(self, id: str):
            self.id = id

    class _R:
        def __init__(self, ids: list[str]):
            self.findings = [_F(i) for i in ids]

    monkeypatch.setattr("skillscan.cli.scan", lambda *_a, **_k: _R([]))

    manifest = tmp_path / "bench.json"
    manifest.write_text(
        json.dumps({"cases": [{"target": "x", "expected_ids": ["MAL-001"], "forbidden_ids": []}]}),
        encoding="utf-8",
    )

    result = runner.invoke(app, ["benchmark", str(manifest), "--min-recall", "1.0"])
    assert result.exit_code == 1


def test_benchmark_command_validation_errors(tmp_path: Path) -> None:
    manifest = tmp_path / "bench.json"
    manifest.write_text(json.dumps({"cases": []}), encoding="utf-8")

    bad_profile = runner.invoke(app, ["benchmark", str(manifest), "--policy-profile", "bad"])
    assert bad_profile.exit_code == 2

    bad_format = runner.invoke(app, ["benchmark", str(manifest), "--format", "xml"])
    assert bad_format.exit_code == 2

    bad_min_precision = runner.invoke(app, ["benchmark", str(manifest), "--min-precision", "1.5"])
    assert bad_min_precision.exit_code == 2

    bad_min_recall = runner.invoke(app, ["benchmark", str(manifest), "--min-recall", "-0.1"])
    assert bad_min_recall.exit_code == 2


def test_benchmark_command_manifest_and_case_validation(tmp_path: Path) -> None:
    bad_manifest = tmp_path / "bad.json"
    bad_manifest.write_text(json.dumps({"cases": {"target": "x"}}), encoding="utf-8")
    result = runner.invoke(app, ["benchmark", str(bad_manifest)])
    assert result.exit_code == 2

    bad_case = tmp_path / "bad_case.json"
    bad_case.write_text(json.dumps({"cases": [{"expected_ids": ["MAL-001"]}]}), encoding="utf-8")
    result = runner.invoke(app, ["benchmark", str(bad_case)])
    assert result.exit_code == 2


def test_benchmark_command_scan_error_and_text_output(monkeypatch, tmp_path: Path) -> None:
    manifest = tmp_path / "bench.json"
    manifest.write_text(
        json.dumps(
            {
                "cases": [
                    {"target": "x", "expected_ids": [], "forbidden_ids": []},
                ]
            }
        ),
        encoding="utf-8",
    )

    from skillscan.analysis import ScanError

    def fail_scan(*_a, **_k):
        raise ScanError("boom")

    monkeypatch.setattr("skillscan.cli.scan", fail_scan)
    err = runner.invoke(app, ["benchmark", str(manifest)])
    assert err.exit_code == 2

    class _R:
        findings = []

    def ok_scan(_target, _policy, _policy_source, **kwargs):
        assert kwargs["ai_assist"] is True
        return _R()

    monkeypatch.setattr("skillscan.cli.scan", ok_scan)
    ok = runner.invoke(app, ["benchmark", str(manifest), "--ai-assist", "--format", "text"])
    assert ok.exit_code == 0
    assert "benchmark cases=1" in ok.stdout
