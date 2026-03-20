---
name: mac-dev-cache-cleaner
description: Analyze and selectively clean macOS development caches to reclaim disk space. Use when storage/system data spikes, or when users ask to find and safely remove Gradle, Android Studio, CocoaPods, Xcode, simulator, npm/yarn/pnpm, Homebrew, and scattered project caches like node_modules/build/dist folders.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Ppang0405/mac-cleaner-skills
# corpus-url: https://github.com/Ppang0405/mac-cleaner-skills/blob/93e22881dd71ffdf7f389dd9d50df6e4f4ef89ed/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Mac Dev Cache Cleaner

## Overview

Run safe, inspect-first cache cleanup with `scripts/dev_cache_manager.py`.

## Workflow

1. Run scan mode first.
2. Rank large targets by `risk` and `safe` columns.
3. Consult `references/cache-risk-matrix.md` for deletion impact.
4. Run cleanup in dry-run mode with selected keys/paths.
5. Run cleanup with `--apply --yes` only after confirmation.
6. Re-run scan and report reclaimed size.

## Commands

Use `/usr/bin/python3` to avoid environment-specific `python3` shims.

```bash
# 1) Scan known global caches
/usr/bin/python3 scripts/dev_cache_manager.py scan --min-size-mb 512

# 2) Include project trees for scattered node_modules/build folders
/usr/bin/python3 scripts/dev_cache_manager.py scan \
  --project-root ~/Documents/Projects \
  --project-root ~/work \
  --min-size-mb 256 \
  --json-out /tmp/dev-cache-report.json

# 3) Include broad home dot-directories + orphan app-data detection
/usr/bin/python3 scripts/dev_cache_manager.py scan \
  --include-home-dotdirs \
  --include-orphans \
  --min-size-mb 256

# 4) Dry-run cleanup using keys from scan output
/usr/bin/python3 scripts/dev_cache_manager.py clean \
  --key gradle-caches \
  --key cocoapods-cache

# 5) Dry-run cleanup for specific project paths from scan output
/usr/bin/python3 scripts/dev_cache_manager.py clean \
  --path /absolute/project/node_modules \
  --path /absolute/project/android/.gradle

# 6) Execute low/medium-risk cleanup
/usr/bin/python3 scripts/dev_cache_manager.py clean \
  --key gradle-caches \
  --key npm-cache \
  --apply --yes

# 7) Execute high-risk/non-safe cleanup (strict token required)
/usr/bin/python3 scripts/dev_cache_manager.py clean \
  --path /absolute/high-risk/path \
  --allow-unknown-paths \
  --apply --yes \
  --confirm-risk DELETE_HIGH_RISK

# 8) Orphan app-data report
/usr/bin/python3 scripts/dev_cache_manager.py scan-orphans --min-size-mb 50

# Optional: include custom/external app install roots to reduce false positives
/usr/bin/python3 scripts/dev_cache_manager.py scan-orphans \
  --app-root /Volumes/ExternalDrive/Applications \
  --app-root /custom/apps \
  --min-size-mb 50

# 9) Orphan cleanup (strict token required)
/usr/bin/python3 scripts/dev_cache_manager.py clean-orphans \
  --bundle-id com.example.deletedapp \
  --apply --yes \
  --confirm-orphans DELETE_ORPHAN_APP_DATA
```

## Decision Rules

- Prefer low-risk entries first (`safe=yes`).
- Treat medium risk as safe-but-costly (re-index/re-download expected).
- Treat high risk as destructive to emulator/simulator/archive history.
- Require `--confirm-risk DELETE_HIGH_RISK` for high-risk/non-safe apply mode.
- Require `--confirm-orphans DELETE_ORPHAN_APP_DATA` for orphan apply mode.
- Avoid `--allow-unknown-paths` unless the user explicitly approves that path.

## Output Expectations

- Provide a short summary table: selected entries, size, risk, and rationale.
- State whether command was dry-run or apply mode.
- After apply mode, run another scan and report before/after totals.