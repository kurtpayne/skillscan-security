---
name: web3-sdl-workflows
description: Run a Web3 SDL for smart contract projects using either a project-wide baseline workflow or a diff-driven workflow based on recent commits and diffs. Make sure to use this skill whenever the user asks for or would benefit from a threat model, SDL, smart contract security review, audit-style review, STRIDE-Web3 analysis, changed-contract or PR security analysis, recent-commit review, integration/fuzz/invariant planning or execution, or a detailed security report for Solidity or Foundry code, even if they do not explicitly mention "SDL."
compatibility:
  required_tools:
    - git
    - forge
  optional_tools:
    - pandoc
    - xelatex
    - solidity-auditor
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: wiimdy/web3-sdl-skill
# corpus-url: https://github.com/wiimdy/web3-sdl-skill/blob/919107a4b1a59b4b0a67260245509783c98e5f98/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Web3 SDL Workflows

Use this file as a router. Keep the root context small, then load only the
references needed for the selected workflow. This keeps the skill focused and
leaves room for repository-specific evidence.

## Supported Workflows

- `project-sdl`
  - Route repository-wide baseline work here.
- `diff-sdl`
  - Route branch, PR, and recent-change security work here.

## Loading Order

1. Read [`references/mode-selection.md`](references/mode-selection.md).
2. Load exactly one workflow file:
   - [`references/project-sdl.md`](references/project-sdl.md)
   - [`references/diff-sdl.md`](references/diff-sdl.md)
3. Always load:
   - [`references/tob-tooling.md`](references/tob-tooling.md)
   - [`references/testing-requirements.md`](references/testing-requirements.md)
   - [`references/reporting-requirements.md`](references/reporting-requirements.md)
4. Read [`references/configuration.md`](references/configuration.md) only when
   `sdl-config.yml` exists or the user asks to tune defaults.
5. Read [`references/risk-scoring.md`](references/risk-scoring.md) for Stage 2
   or any later stage that depends on a prioritized risk register.
6. Read [`references/semantic-validation.md`](references/semantic-validation.md)
   when external touchpoints, oracles, config keys, validators, or proposals are
   in scope.
7. Read [`references/runtime-validation.md`](references/runtime-validation.md)
   when fork, RPC, or runtime-backed checks matter.
8. In `diff-sdl`, read [`references/threat-enrichment.md`](references/threat-enrichment.md)
   when the run needs extra threat ideation from subagents.
9. Read [`references/audit-preparation.md`](references/audit-preparation.md) for
   Stage 4 or final delivery.
10. Read [`references/ci-gates.md`](references/ci-gates.md) when the run happens
    in CI, in a PR workflow, or under a strict completion contract.

Load only one workflow file unless the user explicitly asks for both. This
prevents the skill from mixing baseline guidance with diff-specific guidance.

## Stage Selection

Keep the selected workflow and run only the requested stages. Respect the
dependency chain below so later stages still inherit enough context:

- Stage 1: threat model
- Stage 2: threat identification and prioritization
- Stage 3: integration tests, fuzzing, invariant tests
- Stage 4: detailed report

Create the minimum threat-model context first when the user asks for Stage 2,
3, or 4 without an existing threat model. This matters because threat ranking,
test design, and reporting all depend on the same system assumptions.

## Shared Rules

- Use the repository as the source of truth.
- Let recent commits and diffs drive threat identification in `diff-sdl` so the
  review stays anchored to the actual change surface.
- Run integration tests, fuzzing, and invariant tests in `diff-sdl` before
  reporting success. If prerequisites are missing, stop and report the blocker
  instead of filling the gap with narrative.
- Back every finding with code, diff, test, or runtime evidence so the report
  remains auditable.
- Write outputs under the mode-specific directories:
  - `sdl-output/project-sdl/`
  - `sdl-output/diff-sdl/`

## Bundled Resources

- Run [`scripts/collect_change_scope.sh`](scripts/collect_change_scope.sh) in
  `diff-sdl` to collect branch, commit, and diff context quickly and
  consistently.
- Run [`scripts/render_final_report.sh`](scripts/render_final_report.sh) after
  writing `final-report.md` to render the required `final-report.pdf`.
- Reuse [`assets/templates/final-report-outline.md`](assets/templates/final-report-outline.md)
  when assembling the final narrative so reports keep the same structure.