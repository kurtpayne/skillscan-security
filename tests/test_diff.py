from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from skillscan.cli import app

runner = CliRunner()


def _write_report(path: Path, findings: list[dict]) -> None:
    path.write_text(
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
                "findings": findings,
                "iocs": [],
                "dependency_findings": [],
                "capabilities": [],
            }
        ),
        encoding="utf-8",
    )


def test_diff_text_and_json(tmp_path: Path) -> None:
    base = tmp_path / "base.json"
    curr = tmp_path / "curr.json"

    _write_report(
        base,
        [
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
    )
    _write_report(
        curr,
        [
            {
                "id": "ABU-001",
                "category": "instruction_abuse",
                "severity": "high",
                "confidence": 0.8,
                "title": "a",
                "evidence_path": "a.md",
                "line": 1,
                "snippet": "x",
            },
            {
                "id": "MAL-001",
                "category": "malware_pattern",
                "severity": "critical",
                "confidence": 0.9,
                "title": "b",
                "evidence_path": "b.md",
                "line": 2,
                "snippet": "y",
            },
        ],
    )

    text_result = runner.invoke(app, ["diff", str(base), str(curr)])
    assert text_result.exit_code == 0
    assert "New:" in text_result.stdout

    json_result = runner.invoke(app, ["diff", str(base), str(curr), "--format", "json"])
    assert json_result.exit_code == 0
    payload = json.loads(json_result.stdout)
    assert payload["new_count"] == 1
    assert payload["resolved_count"] == 0
    assert payload["persistent_count"] == 1


def test_diff_invalid_format(tmp_path: Path) -> None:
    base = tmp_path / "base.json"
    curr = tmp_path / "curr.json"
    _write_report(base, [])
    _write_report(curr, [])

    result = runner.invoke(app, ["diff", str(base), str(curr), "--format", "bad"])
    assert result.exit_code == 2
    assert "Invalid --format" in result.stdout
