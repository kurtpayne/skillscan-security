"""Seed the bundled ioc_db.json from the configured managed intel sources.

Strategy
--------
The bundled ioc_db.json ships inside the Python package and is searched on
every scan. It must be:
  - Small enough to not bloat the package (target: <200 KB)
  - Fast to search (linear lookup — keep total entries <5,000)
  - High-signal (low false-positive rate for MCP/AI skill scanning)

Large feeds (Hagezi TIF: 687k domains, URLhaus URLs: 71k) are left for the
runtime managed-source sync (skillscan intel sync), which writes per-feed
files to ~/.skillscan/intel/ and merges them at scan time.

Bundled DB sources (high-precision, small):
  - urlhaus_hosts: active malware-hosting domains (~500 entries)
  - feodotracker_ips: active C2 IPs (~1-50 entries, very high precision)
  - spamhaus_drop: hijacked IP blocks (~1,500 CIDRs)

Runtime-only sources (large, merged at scan time):
  - urlhaus_urls: 71k active malware URLs
  - hagezi_tif_domains: 687k threat intel domains
  - hagezi_tif_ips: 40k threat intel IPs
  - phishing_army_domains: 154k phishing domains
  - kadhosts_domains: 53k malware/ad domains

Usage:
    python3 scripts/seed_ioc_db.py [--dry-run]
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
IOC_DB_PATH = REPO_ROOT / "src/skillscan/data/intel/ioc_db.json"
MANAGED_SOURCES_PATH = REPO_ROOT / "src/skillscan/data/intel/managed_sources.json"

# Only these feeds are baked into the bundled DB.
BUNDLED_FEEDS = {"urlhaus_hosts", "feodotracker_ips", "spamhaus_drop"}

REQUEST_TIMEOUT = 30

# Hand-curated campaign IOCs — always preserved verbatim.
CURATED_DOMAINS = [
    "evil.example",
    "clawdhub1.com",
    "malicanbur.pro",
    "finney.opentensor-metrics.com",
    "finney.metagraph-stats.com",
    "finney.subtensor-telemetry.com",
    "opentensor-cdn.com",
    "t.opentensor-cdn.com",
    "serialmenot.com",
    "crahdhduf.com",
    "weaplink.com",
]

CURATED_IPS = [
    "91.92.242.30",
    "54.91.154.110",
    "45.32.150.251",
    "45.32.151.157",
    "70.34.242.255",
    "173.211.46.22",
    "144.31.224.98",
]

CURATED_URLS = [
    "https://glot.io/snippets/malicious-bootstrap",
    "https://fastdlvrss.s3.us-east-1.amazonaws.com",
    "https://backupdailyawss.s3.us-east-1.amazonaws.com",
]


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "skillscan-seed/1.0"})
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
        payload = resp.read()
    return payload.decode("utf-8", errors="ignore") if isinstance(payload, bytes) else str(payload)


def parse_feed(raw: str, fmt: str) -> dict[str, list[str]]:
    urls: set[str] = set()
    ips: set[str] = set()
    domains: set[str] = set()
    cidrs: set[str] = set()

    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith(("#", ";", "!")):
            continue
        if ";" in line:
            line = line.split(";", 1)[0].strip()
        if not line:
            continue

        if fmt == "url_text" and line.startswith("http"):
            urls.add(line.lower())
        elif fmt == "ip_text":
            token = line.split()[0]
            if token.count(".") == 3:
                ips.add(token)
        elif fmt == "domain_text":
            token = line.split()[0].lower()
            if token.startswith("||") and token.endswith("^"):
                token = token[2:-1]
            if token.startswith("*."):
                token = token[2:]
            if token and "." in token and not token.startswith("//"):
                domains.add(token)
        elif fmt == "hostfile":
            parts = line.split()
            if len(parts) >= 2:
                token = parts[1].lower()
                if token not in ("localhost", "localhost.localdomain", "broadcasthost"):
                    domains.add(token)
        elif fmt == "spamhaus_drop":
            token = line.split()[0]
            if "/" in token:
                cidrs.add(token)
        elif fmt == "cidr_text":
            token = line.split()[0]
            if "/" in token:
                cidrs.add(token)

    return {
        "domains": sorted(domains),
        "ips": sorted(ips),
        "urls": sorted(urls),
        "cidrs": sorted(cidrs),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed bundled ioc_db.json from high-precision feeds.")
    parser.add_argument("--dry-run", action="store_true", help="Print stats without writing.")
    args = parser.parse_args()

    sources = json.loads(MANAGED_SOURCES_PATH.read_text(encoding="utf-8"))

    feed_domains: set[str] = set()
    feed_ips: set[str] = set()
    feed_cidrs: set[str] = set()
    feed_urls: set[str] = set()

    for src in sources:
        name = src["name"]
        if name not in BUNDLED_FEEDS:
            print(f"Skipping (runtime-only): {name}")
            continue
        fmt = src["format"]
        url = src["url"]
        print(f"Fetching {name} ({fmt})...")
        try:
            raw = fetch(url)
            parsed = parse_feed(raw, fmt)
            feed_domains.update(parsed.get("domains", []))
            feed_ips.update(parsed.get("ips", []))
            feed_cidrs.update(parsed.get("cidrs", []))
            feed_urls.update(parsed.get("urls", []))
            print(f"  -> {sum(len(v) for v in parsed.values())} entries "
                  f"({len(parsed['domains'])} domains, {len(parsed['ips'])} IPs, "
                  f"{len(parsed['cidrs'])} CIDRs, {len(parsed['urls'])} URLs)")
        except (urllib.error.URLError, OSError, TimeoutError) as exc:
            print(f"  ERROR: {exc}")
        time.sleep(0.5)

    final_domains = sorted(set(CURATED_DOMAINS) | feed_domains)
    final_ips = sorted(set(CURATED_IPS) | feed_ips)
    final_cidrs = sorted(feed_cidrs)
    final_urls = sorted(set(CURATED_URLS) | feed_urls)

    total = len(final_domains) + len(final_ips) + len(final_cidrs) + len(final_urls)
    print(f"\nFinal bundled DB: {len(final_domains)} domains, {len(final_ips)} IPs, "
          f"{len(final_cidrs)} CIDRs, {len(final_urls)} URLs")
    print(f"Total entries: {total}")

    if args.dry_run:
        print("\n[dry-run] Not writing ioc_db.json.")
        return

    result = {
        "_meta": {
            "generated": datetime.now(UTC).strftime("%Y-%m-%d"),
            "bundled_sources": sorted(BUNDLED_FEEDS),
            "note": (
                "Bundled high-precision IOC DB. Hand-curated campaign IOCs are always included. "
                "Large feeds (URLhaus URLs, Hagezi TIF, Phishing Army, KADhosts) are runtime-only "
                "and merged at scan time via managed_sources.json."
            ),
        },
        "domains": final_domains,
        "ips": final_ips,
        "cidrs": final_cidrs,
        "urls": final_urls,
    }

    IOC_DB_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")

    size_kb = IOC_DB_PATH.stat().st_size / 1024
    print(f"\nWrote {IOC_DB_PATH} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
