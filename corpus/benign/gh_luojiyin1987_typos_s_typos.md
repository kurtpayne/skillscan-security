---
name: typos
description: Run typos CLI on files and produce LLM-reviewable spelling fixes with optional diff/apply.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: luojiyin1987/typos-skill
# corpus-url: https://github.com/luojiyin1987/typos-skill/blob/594319915cedd3cb4f69862d778409766ced68f1/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Typos Spell Check with LLM Review

Use this skill when the user wants to scan files for spelling errors with the
`typos` CLI and confirm corrections via LLM before applying changes.

## Workflow

1. Run `./typos-skill.sh --export-review review.jsonl [path...]` to generate a
   review file plus a human-readable summary.
2. Read file context at the reported path and line; update each JSON line:
   - `status`: `ACCEPT CORRECT`, `FALSE POSITIVE`, or `CUSTOM`
   - `correction`: required when status is `CUSTOM`
3. Apply approved changes with `./typos-skill.sh --apply-review review.jsonl`.
4. Optional: use `--diff` to preview or `--apply-all` to skip review.

## Review File Rules

- `status` is case-insensitive and supports `_` / `-` separators.
- Accepted statuses:
  - apply: `ACCEPT`, `ACCEPT CORRECT`, `CUSTOM`
  - skip: `FALSE POSITIVE`, `FALSE POSITIVE?`, `FALSEPOSITIVE`, `SKIP`, `REJECT`
- `CUSTOM` requires non-empty `correction`.
- Do not edit locator fields unless you know what you are doing:
  - keep `byte_offset` unchanged
  - keep `occurrence_index` unchanged
  - keep `line_num` consistent with source
- If `byte_offset` is removed and the same typo appears multiple times on one
  line, `occurrence_index` is required to disambiguate the target occurrence.

## Execution Context

- The tool no longer requires running from repo root for `--apply-review`.
- Relative `path` values in `review.jsonl` are resolved relative to the review
  file directory.
- `./typos-skill.sh` still assumes you are in this skill directory; from
  elsewhere, invoke via absolute path.

## Failure Scenarios and Conflict Handling

- `byte_offset mismatch`: source file changed after export.
- `multiple occurrences on the same line`: ambiguous target without
  `byte_offset` / `occurrence_index`.
- `overlapping replacements detected`: two approved edits collide.
- `Missing file`: review `path` is invalid for current workspace.

When any conflict above occurs, apply step fails fast and writes nothing. Fix by
re-exporting review (`--export-review`) from the latest files and re-approving.

## Dependencies

- `typos` (`cargo install typos-cli`)
- `python3`

## Notes

- Script: `typos-skill.sh`
- Apply helper: `scripts/apply-review.py`
- Smoke test: `scripts/smoke-typos-skill.sh`