# Spec: `skillscan lint` Companion Namespace (v0.5 scope)

## Goal
Add a lightweight lint mode that catches obvious policy/rule hygiene issues fast, before full deep scan.

## Positioning
- `skillscan scan`: full security analysis
- `skillscan lint`: fast static guardrails for local dev + pre-commit

## v0.5 scope
1. New CLI namespace:
   - `skillscan lint <path>`
2. Checks included:
   - malformed policy/rule files
   - duplicate rule IDs
   - invalid severity/confidence ranges
   - unreachable/overbroad regex guard (basic compile + sanity)
   - basic workflow anti-pattern checks (unpinned actions in sensitive workflows)
3. Output formats:
   - text (default)
   - json
4. Exit codes:
   - `0` = clean
   - `1` = lint violations
   - `2` = runtime/tooling error

## Non-goals
- replacing `scan`
- AI-assisted semantic reasoning
- deep dependency and IOC analysis

## UX example
```bash
skillscan lint .
skillscan lint . --format json --out lint-report.json
```

## Acceptance criteria
- lint completes in <5s on medium repo (non-cold cache target)
- catches duplicate IDs and invalid patterns deterministically
- compatible with pre-commit and CI
- documented migration path from lint findings to `scan` remediation

## Implementation notes
- Add `lint.py` module and Typer subcommand
- Reuse existing model validation where possible
- Keep lint checks deterministic and side-effect free

## Rollout
- v0.5: core lint checks + docs
- v0.6: optional autofix suggestions for safe classes of findings
