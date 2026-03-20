---
name: nasa-safe-code-rater
description: Score C/C++ code against NASA safe coding guidance using 10 normalized rules, produce a 0-100 safety score, and return an English report with findings, exclusions, and remediation. Use when the user invokes $nasa-safe-code-rater or asks to audit a repository/current file/diff for NASA-style safe C coding compliance.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: mslmyilmaz5/nasa-safe-code-rater
# corpus-url: https://github.com/mslmyilmaz5/nasa-safe-code-rater/blob/483b72659ae5805221911a09d87c1c170ea3c38b/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# NASA Safe Code Rater

Use this skill to evaluate C/C++ code with a NASA-inspired 10-rule model and generate a scored report.

## Inputs

Accept optional user arguments:
- `target=repo|file|diff` (default `repo`)
- `path=<file-or-dir>` (required for `target=file`)
- `include_cpp=true|false` (default `true`)

If arguments are absent, run repository-wide analysis.

## Required Workflow

1. Resolve scope from user input.
2. Analyze only C/C++ files by default (`.c`, `.h`, `.cpp`, `.hpp`).
3. List non-C/C++ files as excluded items.
4. Evaluate all 10 rules in `references/nasa_rules.md`.
5. Produce an English markdown report containing:
- Executive summary
- Overall score and risk class (`Good`, `Warning`, `Critical`)
- Rule-by-rule findings table
- Top 5 remediation actions
- Insufficient evidence section

## Execution Commands

Use these scripts from the skill directory:

```bash
python3 scripts/analyze_repo.py --root <repo-path> --mode repo --json-out /tmp/nasa_analysis.json
python3 scripts/score_report.py --analysis /tmp/nasa_analysis.json --format markdown
```

For single file mode:

```bash
python3 scripts/analyze_repo.py --root <repo-path> --mode file --path <file-path> --json-out /tmp/nasa_analysis.json
```

For diff mode:

```bash
python3 scripts/analyze_repo.py --root <repo-path> --mode diff --json-out /tmp/nasa_analysis.json
```

To refresh normalized rules from a source PDF:

```bash
python3 scripts/extract_nasa_rules.py --pdf <path-to-pdf> --out references/nasa_rules.md
```

## Quality Gates

Require for critical findings:
- At least one concrete evidence line per failed rule.
- Rule IDs traceable to `references/nasa_rules.md`.

If no C/C++ files are in scope, return `not applicable` with reason and next step.