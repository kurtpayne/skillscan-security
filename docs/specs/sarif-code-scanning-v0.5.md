# Spec: SARIF + GitHub Code Scanning Integration (v0.5 readiness)

## Goal
Make SkillScan feel "first-class" in GitHub Advanced Security pipelines by shipping a documented, copy/paste integration for SARIF upload and triage.

## Why now
SkillScan already emits SARIF (`--format sarif`). The gap is packaging + adoption UX:
- no blessed workflow example
- no opinionated mapping guidance (severity, rule ids)
- no quick-start docs for repositories without existing code scanning

## Scope (v0.5)
1. **Reference workflow** (`.github/workflows/skillscan-code-scanning.yml`)
   - run SkillScan on push + PR
   - output `skillscan.sarif`
   - upload via `github/codeql-action/upload-sarif`
2. **Docs**
   - "Enable in 5 minutes" section in README + docs
   - troubleshooting section (missing permissions, empty SARIF, path mapping)
3. **Policy defaults guidance**
   - recommended CI flag set (`--fail-on block`, `--format sarif`, `--out skillscan.sarif`)
   - strict vs permissive examples
4. **Result hygiene**
   - ensure SARIF `ruleId`, `level`, `location` are stable and useful in PR UI

## Out of scope
- New SARIF schema work (already implemented)
- Full baseline/delta suppression UX in GitHub UI
- Non-GitHub platform integrations

## Acceptance criteria
- A user can copy one workflow file and see SkillScan alerts in Security > Code scanning
- At least one fixture repo validates end-to-end upload
- Docs include screenshot or exact navigation path for alert triage
- CI example validates on a public repo without private secrets

## Proposed workflow snippet
```yaml
name: SkillScan Code Scanning
on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read
  security-events: write

jobs:
  skillscan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: |
          python -m pip install --upgrade pip
          pip install skillscan-security
      - run: |
          skillscan scan . --format sarif --out skillscan.sarif --fail-on never
      - uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: skillscan.sarif
```

## Rollout
- v0.5: docs + reference workflow
- v0.6: optional baseline-aware SARIF filtering for noise reduction
