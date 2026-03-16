# Automation Guardrails for Pattern Scout

This document defines how automated pattern discovery/update runs must operate.

## Goals
- Keep `main` clean at all times.
- Make updates deterministic, auditable, and reviewable.
- Prevent partial/dirty updates when a run fails.

## Required Workflow

1. **Pre-flight checks**
   - Ensure repo is on `main` and clean.
   - Pull latest `origin/main`.
   - If dirty: stash and exit (do not edit files).

2. **Isolated branch execution**
   - Create a branch: `chore/pattern-update-YYYYMMDD-<rand4hex>`.
   - Perform all research, edits, tests, and commits on this branch.
   - Never edit files directly on `main`.

3. **Validation gate**
   - Must pass (repo venv only):
     - `.venv/bin/ruff check src tests`
     - `.venv/bin/pytest -q`
   - Recommended local wrapper for deterministic runs:
     - `TIMEOUT_SECONDS=900 ./scripts/run_local_validation.sh`
   - CI includes `Pattern Update Guard` workflow with additional policy checks.

4. **PR-first integration**
   - Push branch and open PR to `main`.
   - Merge only after CI passes and review is complete.

5. **Failure handling**
   - If no update is warranted: delete temporary branch and return to `main`.
   - If validation fails: return to `main`; keep failure output in summary.
   - If PR creation fails: keep branch for manual recovery, but return to `main`.

## Policy checks enforced in CI
When `src/skillscan/data/rules/default.yaml` changes, CI requires:
- version bump in `default.yaml`
- at least one new rule ID in diff
- tests updated (`tests/test_rules.py`, `tests/test_showcase_examples.py`)
- showcase fixture updated under `examples/showcase/*`
- docs index updates (`docs/EXAMPLES.md`, `examples/showcase/INDEX.md`)
- rationale update (`docs/RULE_UPDATES.md` or `PATTERN_UPDATES.md`)

## Operational notes
- Keep updates small (prefer one coherent pattern set per PR).
- Include source links in PR and changelog entries.
- Prefer no-change exits over speculative/low-confidence rules.
