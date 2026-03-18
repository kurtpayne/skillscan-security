"""Seed vuln_db.json from OSV.dev for the top MCP-adjacent packages.

Queries the OSV.dev batch API for known-vulnerable versions of the packages
most commonly found in MCP skill bundles and AI agent tooling. Writes results
to src/skillscan/data/intel/vuln_db.json in the format expected by the
analysis engine:

  {
    "python": {
      "<package>": {
        "<version>": {"id": "CVE-...", "severity": "high", "fixed": "x.y.z"}
      }
    },
    "npm": { ... }
  }

Only the most recent (highest CVSS) vulnerability per package/version is kept
to avoid bloating the DB with duplicate entries for the same version.

Usage:
    python3 scripts/seed_vuln_db.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
VULN_DB_PATH = REPO_ROOT / "src/skillscan/data/intel/vuln_db.json"

OSV_QUERY_URL = "https://api.osv.dev/v1/query"
OSV_BATCH_URL = "https://api.osv.dev/v1/querybatch"
REQUEST_TIMEOUT = 30

SEVERITY_ORDER = {"critical": 4, "high": 3, "medium": 2, "low": 1, "unknown": 0}

# Top MCP-adjacent Python packages to check.
PYTHON_PACKAGES = [
    # MCP SDK and tooling
    "mcp",
    "anthropic",
    "openai",
    "langchain",
    "langchain-core",
    "langchain-community",
    "llama-index",
    "llama-index-core",
    "pydantic",
    "pydantic-core",
    # Common skill dependencies
    "requests",
    "httpx",
    "aiohttp",
    "fastapi",
    "uvicorn",
    "starlette",
    "cryptography",
    "paramiko",
    "pyyaml",
    "jinja2",
    "pillow",
    "numpy",
    "pandas",
    "transformers",
    "torch",
    # Already in DB — keep for continuity
    "bittensor-wallet",
]

# Top MCP-adjacent npm packages to check.
NPM_PACKAGES = [
    # MCP SDK and tooling
    "@modelcontextprotocol/sdk",
    "@anthropic-ai/sdk",
    "openai",
    "@langchain/core",
    "langchain",
    # Common MCP server packages
    "@awslabs/aws-api-mcp-server",
    "@modelcontextprotocol/server-filesystem",
    "@modelcontextprotocol/server-github",
    "@modelcontextprotocol/server-brave-search",
    "@modelcontextprotocol/server-fetch",
    # Common skill dependencies
    "axios",
    "node-fetch",
    "express",
    "fastify",
    "lodash",
    "moment",
    "semver",
    "tar",
    "unzipper",
    "archiver",
]


def cvss_to_severity(score: float | None) -> str:
    if score is None:
        return "medium"
    if score >= 9.0:
        return "critical"
    if score >= 7.0:
        return "high"
    if score >= 4.0:
        return "medium"
    return "low"


def extract_severity(vuln: dict) -> tuple[str, float | None]:
    """Extract the highest severity from a vulnerability record."""
    best_score: float | None = None
    best_sev = "unknown"

    for sev_entry in vuln.get("severity", []):
        stype = sev_entry.get("type", "")
        score_str = sev_entry.get("score", "")
        if stype in ("CVSS_V3", "CVSS_V4") and score_str:
            try:
                # CVSS vector string — extract base score from the end
                if "/" in score_str:
                    # It's a vector; we can't easily parse without a library.
                    # Fall through to database_specific below.
                    pass
                else:
                    score = float(score_str)
                    if best_score is None or score > best_score:
                        best_score = score
                        best_sev = cvss_to_severity(score)
            except ValueError:
                pass

    # Try database_specific CVSS scores (more reliably numeric).
    for db_sev in vuln.get("database_specific", {}).get("severity", []):
        pass  # string like "HIGH" — use as fallback

    db_sev_str = vuln.get("database_specific", {}).get("severity", "")
    if db_sev_str and best_sev == "unknown":
        mapping = {"CRITICAL": "critical", "HIGH": "high", "MODERATE": "medium",
                   "MEDIUM": "medium", "LOW": "low"}
        best_sev = mapping.get(db_sev_str.upper(), "medium")

    if best_sev == "unknown":
        best_sev = "medium"

    return best_sev, best_score


def extract_fixed_version(vuln: dict, ecosystem: str, package: str) -> str | None:
    """Extract the earliest fixed version from affected ranges."""
    for affected in vuln.get("affected", []):
        pkg = affected.get("package", {})
        if pkg.get("name", "").lower() != package.lower():
            continue
        for rng in affected.get("ranges", []):
            for event in rng.get("events", []):
                fixed = event.get("fixed")
                if fixed:
                    return fixed
        # Also check versions list for the last entry (often the fixed version)
        versions = affected.get("versions", [])
        if versions:
            # The fixed version is not in the versions list; skip.
            pass
    return None


def query_osv(ecosystem: str, package: str) -> list[dict]:
    """Query OSV.dev for all vulnerabilities affecting a package."""
    payload = json.dumps({
        "package": {"name": package, "ecosystem": ecosystem}
    }).encode()
    req = urllib.request.Request(
        OSV_QUERY_URL,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "skillscan-seed/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            data = json.loads(resp.read())
        return data.get("vulns", [])
    except (urllib.error.URLError, OSError, json.JSONDecodeError) as exc:
        print(f"    OSV error for {ecosystem}/{package}: {exc}")
        return []


def process_package(ecosystem: str, package: str, osv_ecosystem: str) -> dict[str, dict]:
    """Return a version map {version: {id, severity, fixed}} for a package.

    Strategy: for each CVE, keep only the *latest* (lexicographically last)
    affected version. This captures the "last broken version" which is what
    the scanner needs to flag an installed version as vulnerable, without
    bloating the DB with every historical release.
    """
    vulns = query_osv(osv_ecosystem, package)
    if not vulns:
        return {}

    version_map: dict[str, dict] = {}

    for vuln in vulns:
        vuln_id = vuln.get("id", "UNKNOWN")
        severity, _ = extract_severity(vuln)
        fixed = extract_fixed_version(vuln, osv_ecosystem, package)

        # Collect the latest affected version per CVE.
        latest_version: str | None = None
        for affected in vuln.get("affected", []):
            pkg = affected.get("package", {})
            if pkg.get("name", "").lower() != package.lower():
                continue
            versions = affected.get("versions", [])
            if versions:
                # Use the last version in the list (OSV returns them in order).
                candidate = versions[-1]
                if latest_version is None or candidate > latest_version:
                    latest_version = candidate

        if latest_version is not None:
            existing = version_map.get(latest_version)
            existing_sev = SEVERITY_ORDER.get(existing["severity"], 0) if existing else -1
            if existing is None or SEVERITY_ORDER.get(severity, 0) > existing_sev:
                entry: dict = {"id": vuln_id, "severity": severity}
                if fixed:
                    entry["fixed"] = fixed
                version_map[latest_version] = entry

    return version_map


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed vuln_db.json from OSV.dev.")
    parser.add_argument("--dry-run", action="store_true", help="Print stats without writing.")
    args = parser.parse_args()

    # Hand-curated entries — always preserved verbatim, not subject to capping.
    CURATED_PYTHON: dict[str, dict] = {
        "bittensor-wallet": {
            "4.0.2": {"id": "PYPI-BACKDOOR-2026-0317", "severity": "critical", "fixed": "4.0.1"},
        },
        "pyyaml": {
            "5.3": {"id": "CVE-2020-14343", "severity": "high", "fixed": "5.4"},
        },
    }
    CURATED_NPM: dict[str, dict] = {
        "lodash": {
            "4.17.20": {"id": "CVE-2021-23337", "severity": "high", "fixed": "4.17.21"},
        },
        "@awslabs/aws-api-mcp-server": {
            "0.2.14": {"id": "CVE-2026-4270", "severity": "medium", "fixed": "1.3.9"},
        },
    }

    result_python: dict[str, dict] = {k: dict(v) for k, v in CURATED_PYTHON.items()}
    result_npm: dict[str, dict] = {k: dict(v) for k, v in CURATED_NPM.items()}

    # Cap: keep only the top N entries per package (highest severity first).
    # This keeps the bundled DB small while covering the most important vulns.
    MAX_ENTRIES_PER_PACKAGE = 10

    def cap_version_map(version_map: dict[str, dict], curated: dict[str, dict]) -> dict[str, dict]:
        """Keep curated entries + top N by severity from feed."""
        feed_only = {v: e for v, e in version_map.items() if v not in curated}
        sorted_feed = sorted(
            feed_only.items(),
            key=lambda x: SEVERITY_ORDER.get(x[1].get("severity", "unknown"), 0),
            reverse=True,
        )
        result = dict(curated)
        result.update(dict(sorted_feed[:MAX_ENTRIES_PER_PACKAGE]))
        return result

    print("Querying OSV.dev for Python packages...")
    for pkg in PYTHON_PACKAGES:
        print(f"  {pkg}...", end=" ", flush=True)
        version_map = process_package("python", pkg, "PyPI")
        if version_map:
            curated = result_python.get(pkg, {})
            capped = cap_version_map(version_map, curated)
            result_python[pkg] = capped
            print(f"{len(version_map)} vulns -> {len(capped)} kept")
        else:
            print("no vulns found")
        time.sleep(0.3)

    print("\nQuerying OSV.dev for npm packages...")
    for pkg in NPM_PACKAGES:
        print(f"  {pkg}...", end=" ", flush=True)
        version_map = process_package("npm", pkg, "npm")
        if version_map:
            curated = result_npm.get(pkg, {})
            capped = cap_version_map(version_map, curated)
            result_npm[pkg] = capped
            print(f"{len(version_map)} vulns -> {len(capped)} kept")
        else:
            print("no vulns found")
        time.sleep(0.3)

    # Remove packages with no vulnerable versions.
    result_python = {k: v for k, v in result_python.items() if v}
    result_npm = {k: v for k, v in result_npm.items() if v}

    total_python_versions = sum(len(v) for v in result_python.values())
    total_npm_versions = sum(len(v) for v in result_npm.values())

    print("\nFinal vuln DB:")
    print(f"  Python: {len(result_python)} packages, {total_python_versions} vulnerable versions")
    print(f"  npm: {len(result_npm)} packages, {total_npm_versions} vulnerable versions")

    if args.dry_run:
        print("\n[dry-run] Not writing vuln_db.json.")
        return

    output = {
        "_meta": {
            "generated": datetime.now(UTC).strftime("%Y-%m-%d"),
            "source": "OSV.dev (https://osv.dev)",
            "python_packages_checked": PYTHON_PACKAGES,
            "npm_packages_checked": NPM_PACKAGES,
        },
        "python": result_python,
        "npm": result_npm,
    }

    VULN_DB_PATH.write_text(json.dumps(output, indent=2), encoding="utf-8")
    size_kb = VULN_DB_PATH.stat().st_size / 1024
    print(f"\nWrote {VULN_DB_PATH} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
