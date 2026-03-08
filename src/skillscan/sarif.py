from __future__ import annotations

from collections import OrderedDict

from skillscan.models import ScanReport, Severity, confidence_label


def _level_from_severity(severity: Severity) -> str:
    if severity in {Severity.HIGH, Severity.CRITICAL}:
        return "error"
    if severity == Severity.MEDIUM:
        return "warning"
    return "note"


def report_to_sarif(report: ScanReport) -> dict:
    rules: OrderedDict[str, dict] = OrderedDict()
    results: list[dict] = []

    for finding in report.findings:
        if finding.id not in rules:
            rules[finding.id] = {
                "id": finding.id,
                "name": finding.id,
                "shortDescription": {"text": finding.title},
                "properties": {
                    "category": finding.category,
                    "defaultSeverity": finding.severity.value,
                    "confidence": finding.confidence,
                    "confidenceLabel": confidence_label(finding.confidence).value,
                },
            }

        message = finding.title
        if finding.snippet:
            message = f"{message}: {finding.snippet.strip()}"

        clabel = confidence_label(finding.confidence).value
        result: dict = {
            "ruleId": finding.id,
            "level": _level_from_severity(finding.severity),
            "message": {"text": f"{message} [confidence={clabel}]"},
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {"uri": finding.evidence_path},
                        "region": ({"startLine": finding.line} if finding.line else {}),
                    }
                }
            ],
            "properties": {
                "category": finding.category,
                "severity": finding.severity.value,
                "confidence": finding.confidence,
                "confidenceLabel": clabel,
                "mitigation": finding.mitigation,
            },
        }
        results.append(result)

    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "skillscan",
                        "version": report.metadata.scanner_version,
                        "informationUri": "https://github.com/kurtpayne/skillscan",
                        "rules": list(rules.values()),
                    }
                },
                "automationDetails": {
                    "id": f"{report.metadata.policy_profile}:{report.metadata.rulepack_version}"
                },
                "results": results,
            }
        ],
    }
