#!/usr/bin/env python3
"""Validate hygiene for automated pattern-update PRs.

Checks only run when src/skillscan/data/rules/default.yaml is changed.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sh(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def changed_files(base: str = "origin/main") -> list[str]:
    out = sh("git", "diff", "--name-only", f"{base}...HEAD")
    return [line for line in out.splitlines() if line]


def changed_file_content(path: str, base: str = "origin/main") -> str:
    try:
        return sh("git", "diff", f"{base}...HEAD", "--", path)
    except subprocess.CalledProcessError:
        return ""


def fail(msg: str) -> None:
    print(f"❌ {msg}")
    sys.exit(1)


def main() -> int:
    files = changed_files()
    print(f"Changed files ({len(files)}):")
    for f in files:
        print(f" - {f}")

    rules_path = "src/skillscan/data/rules/default.yaml"
    if rules_path not in files:
        print("ℹ️ default.yaml not changed; skipping pattern-update policy checks.")
        return 0

    required = {
        "docs/EXAMPLES.md": "docs/EXAMPLES.md should be updated when rules change",
        "examples/showcase/INDEX.md": "examples/showcase/INDEX.md should be updated",
        "tests/test_rules.py": "tests/test_rules.py must include coverage for new rule(s)",
        "tests/test_showcase_examples.py": (
            "tests/test_showcase_examples.py should validate showcase detections"
        ),
    }
    for path, msg in required.items():
        if path not in files:
            fail(msg)

    if not any(p.startswith("examples/showcase/") and p != "examples/showcase/INDEX.md" for p in files):
        fail("At least one showcase fixture under examples/showcase/* must be added/updated")

    if not any(p in files for p in ("docs/RULE_UPDATES.md", "PATTERN_UPDATES.md")):
        fail("Update docs/RULE_UPDATES.md or PATTERN_UPDATES.md with source-backed rationale")

    diff = changed_file_content(rules_path)
    if not re.search(r'^\+version:\s*"\d{4}\.\d{2}\.\d{2}\.\d+"', diff, flags=re.MULTILINE):
        fail("default.yaml version must be bumped (expected YYYY.MM.DD.N)")

    if not re.search(r"^\+\s*-\s+id:\s+[A-Z]{3}-\d{3}", diff, flags=re.MULTILINE):
        fail("No new rule ID added in default.yaml diff")

    print("✅ Pattern-update guard checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
