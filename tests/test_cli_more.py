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

    invalid_fail_on = runner.invoke(app, ["scan", target, "--fail-on", "bad"])
    assert invalid_fail_on.exit_code == 2

    invalid_intel_age = runner.invoke(app, ["scan", target, "--intel-max-age-minutes", "0"])
    assert invalid_intel_age.exit_code == 2
    invalid_url_links = runner.invoke(app, ["scan", target, "--url-max-links", "-1"])
    assert invalid_url_links.exit_code == 2
    invalid_ai_timeout = runner.invoke(app, ["scan", target, "--ai-timeout-seconds", "0"])
    assert invalid_ai_timeout.exit_code == 2


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
