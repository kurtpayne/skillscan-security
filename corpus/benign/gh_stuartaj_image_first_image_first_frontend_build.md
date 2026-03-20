---
name: image-first-frontend-build
description: "Build UI features with an image-first workflow: generate a visual mockup first, implement the frontend to match it, then run a parity pass and fix differences. Use when users ask to build a new app/page/component or improve an existing frontend and want strong visual direction before coding."
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: StuartAJ/image-first-frontend-build-skill
# corpus-url: https://github.com/StuartAJ/image-first-frontend-build-skill/blob/d1252eddfe9530241c750ef554e8ae6629088f62/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Image First Frontend Build

## Workflow

Follow this sequence every time:

P0. Tool capability preflight.
0. Detect mode (`greenfield` vs `existing-system`).
1. Define scope and constraints.
2. Run existing-system audit (when mode is `existing-system`).
3. Define quality bar and anti-generic guardrails.
4. Generate mockup directions (or deterministic fallback if image generation is unavailable).
5. Select direction with weighted rubric.
6. Extract design tokens and complete state matrix (`required` vs `N/A`).
7. Build from the chosen direction and enforce performance budgets.
8. Run objective QA gates, parity scoring, and artifact capture.
9. Apply correction loops until acceptance criteria are met.

## Operating Modes

Select one mode at the start of every run:

- `fast`: Minimal verification for exploratory iteration and local design loops. Not sufficient for merge-ready signoff.
- `release`: Full verification and evidence set. Required for merge-ready, CI, and audit-grade reports.

## Step P0: Tool Capability Preflight

Before any design work, detect tool availability and record a chosen execution path:

- Image generation available (`yes`/`no`).
- Screenshot capture available (`yes`/`no`).
- `axe` automation available (`yes`/`no`).
- Operating mode selected (`fast` or `release`).

Execution path selection:

- `full`: image generation + screenshots + `axe` available.
- `no-image`: image generation unavailable; use structured text wireframe + token spec.
- `no-screenshot`: screenshot capture unavailable; continue with explicit manual mismatch evidence.
- `no-axe`: `axe` unavailable; run strict manual accessibility checklist and mark automation gap.
- `no-image+no-screenshot`: image generation and screenshots unavailable.
- `no-image+no-axe`: image generation unavailable and `axe` omitted.
- `no-screenshot+no-axe`: screenshot capture unavailable and `axe` omitted.
- `no-image+no-screenshot+no-axe`: image generation/screenshot capture unavailable and `axe` omitted.

Do not proceed until one path is explicitly selected.

## Step 0: Mode Detection

Determine mode before style decisions:

- `greenfield`: new or exploratory UI; choose a bold direction within product goals.
- `existing-system`: preserve established design language and component patterns.

State the selected mode explicitly.

## Step 1: Define Scope

Create a short design brief before prompt generation. Extract and confirm:

- User goal (new app, new feature, or UI improvement).
- Audience and primary task.
- Target surfaces (page/component/modal + key states).
- Breakpoints (minimum: `375`, `768`, `1024`, `1440`).
- Brand constraints (colors, typography, spacing, tone).
- Functional requirements (inputs, interactions, loading/error/empty states).
- Content constraints (real content, realistic lengths, realistic empty/error copy).
- Accessibility expectations (contrast, keyboard traversal, focus visibility).

If requirements are ambiguous, ask only the minimum clarifying questions needed to produce a useful mockup prompt.

## Step 2: Existing-System Audit Checklist

Run this step only when mode is `existing-system`, before prompting:

- Run the extractor script to build initial context:

```bash
node scripts/extract_design_system_context.mjs --repo-root . --baseline artifacts/ui-parity/<previous-run-id>/existing-system-context.json --out artifacts/ui-parity/<run-id>/existing-system-context.json
```

If this is the first existing-system run and `<previous-run-id>` is unavailable, omit `--baseline`; accept `drift.level: "unknown"` and require explicit signoff before implementation.

- Review extracted tokens and reusable components.
- Review reported design-system drift score and treat `medium/high` drift as a risk that needs explicit signoff.
- Define explicit reuse targets:
  - `must-reuse`
  - `allowed-extend`
  - `do-not-change`

Do not continue without explicit reuse targets in `existing-system` mode.

## Step 3: Define Non-Negotiable Quality Bar

Before generating directions, set these non-negotiables:

- Clear visual hierarchy (primary/secondary/tertiary content is obvious).
- Distinct style direction (not generic template output).
- Accessible interaction states (hover/focus/active/disabled visible).
- Required states planned (default/loading/empty/error/success/disabled).
- Mobile and desktop intent are both explicit.
- Semantic structure is feasible (landmarks, headings, control semantics).

Content realism rule:

- Ban pure lorem ipsum unless user explicitly requests it.
- Use realistic labels, body copy lengths, and realistic error/empty messaging.

## Step 4: Create Mockup Directions (or Deterministic Fallback)

Generate 2-3 distinct visual directions using available image generation.

Prompt templates live in `references/mockup-prompt-templates.md`.

If image generation is unavailable:

- Create structured text wireframes (desktop + mobile hierarchy).
- Produce token spec using `assets/design-token-template.json`.
- Treat wireframe + token spec as the visual contract.

## Step 5: Weighted Direction Selection Rubric

Score each direction using weighted criteria (0-5 each):

- Clarity of hierarchy (`35%`).
- Brand/system fit (`30%`).
- Accessibility feasibility (`20%`).
- Implementation cost (`15%`, higher score means lower cost/risk).

Compute weighted total and choose the highest-scoring direction.

Tie-breakers:

- Prefer higher accessibility feasibility.
- Then prefer lower implementation risk.

Use deterministic scoring script:

```bash
node scripts/score_mockup_directions.mjs --in artifacts/ui-parity/<run-id>/directions-input.json --out artifacts/ui-parity/<run-id>/direction-scores.json --md artifacts/ui-parity/<run-id>/direction-scores.md
```

Record the resulting scoring table in the output.

## Step 6: Extract Design Tokens + State Matrix

Extract implementation tokens from the chosen direction:

- Color system (background/surface/text/accent/semantic states).
- Typography (families/scale/weights/line-height).
- Spacing scale.
- Radius/borders/shadows.
- Motion tokens and reduced-motion behavior.

State matrix requirement:

- For each key component/surface, map:
  - `default`, `loading`, `empty`, `error`, `success`, `disabled`.
- Mark each state as either:
  - `required` (must be implemented), or
  - `N/A` with written justification.

Store this matrix in `artifacts/ui-parity/<run-id>/state-matrix.json` and consume it during state coverage validation.

Rules:

- Blank cells are not allowed.
- `N/A` without justification fails acceptance.
- Any `required` state missing in implementation fails acceptance.

## Step 7: Build From Direction + Enforce Performance Budgets

Implement the frontend using the chosen direction as the contract.

Performance budgets (defaults, enforce pass/fail):

- Route JavaScript budget: `<= 250 KB` (gzip/transfer equivalent).
- Initial image payload budget: `<= 800 KB`.

Required behavior:

- Motion fallback via `prefers-reduced-motion`.
- Avoid heavy visual effects unless explicitly justified by the brief.

## Step 8: Objective QA, Parity, and Artifacts

Run objective QA with script:

```bash
node scripts/run_ui_quality_gates.mjs --url http://localhost:3000 --mode <fast|release> --selected-path <full|no-image|no-screenshot|no-axe|no-image+no-screenshot|no-image+no-axe|no-screenshot+no-axe|no-image+no-screenshot+no-axe> --state-matrix artifacts/ui-parity/<run-id>/state-matrix.json --out-dir artifacts/ui-parity/<run-id>
```

Script expectations:

- Test widths: `375`, `768`, `1024`, `1440`.
- Run cross-browser gates across Chromium, WebKit, and Firefox in `release` mode.
- Check horizontal overflow.
- Check focus visibility and keyboard traversal baseline.
- Run basic `axe` checks when available.
- If `axe` is unavailable, compute WCAG AA contrast fallback in-page and fail on threshold violations.
- Run stress gates in `release` mode: i18n/RTL, 200% zoom, reduced network, long-content overflow.
- Run state discovery automation and fail when required states are untested.
- Emit CI artifacts: JSON, JUnit XML, Markdown summary, run manifest with artifact hashes.
- Validate output against `references/quality-contract.schema.json`.
- Enforce anti-gaming constraints from `references/anti-gaming-rules.md`.

Accessibility thresholds (explicit):

- WCAG AA contrast:
  - normal text `>= 4.5:1`
  - large text `>= 3:1`
- Keyboard traversal:
  - predictable `Tab` navigation through interactive controls
  - no unexpected keyboard trap (except intentional modal traps)
  - visible focus indicator on interactive controls
- Reduced motion:
  - with reduced-motion preference, non-essential animations are disabled or significantly reduced.

Scorecard (0-2 each, max 12):

- Layout parity
- Visual style parity
- Interaction/state parity
- Responsive parity
- Accessibility quality
- Distinctiveness (not generic/boilerplate)

Passing threshold:

- No category below `1`.
- Total score `>= 9`.
- All objective QA gates pass.
- Performance budgets pass.

Run true visual parity scoring:

```bash
node scripts/compare_ui_screenshots.mjs --baseline-dir artifacts/ui-parity/<run-id>/screenshots/mockup --candidate-dir artifacts/ui-parity/<run-id>/screenshots/implementation --out-dir artifacts/ui-parity/<run-id> --mask-file artifacts/ui-parity/<run-id>/mask.json
```

Parity pass criteria:

- Pixel diff ratio `<= 0.02`.
- SSIM `>= 0.96`.

### Standardized Evidence Artifacts

Use this structure for every run:

- `artifacts/ui-parity/<run-id>/qa-report.json`
- `artifacts/ui-parity/<run-id>/run-manifest.json`
- `artifacts/ui-parity/<run-id>/qa-junit.xml`
- `artifacts/ui-parity/<run-id>/qa-summary.md`
- `artifacts/ui-parity/<run-id>/mismatch-log.jsonl`
- `artifacts/ui-parity/<run-id>/parity-report.json`
- `artifacts/ui-parity/<run-id>/direction-scores.json`
- `artifacts/ui-parity/<run-id>/state-coverage.json`
- `artifacts/ui-parity/<run-id>/screenshots/mockup/<state>-w<width>.png`
- `artifacts/ui-parity/<run-id>/screenshots/implementation/<state>-w<width>.png`

`run-id` format: `YYYYMMDD-HHMMSS`.

## Step 9: Correction Pass and Exit Criteria

Run up to 2 correction loops by default. If still below threshold, report blockers and next targeted fixes.

When a gate fails, use `references/failure-remediation-map.md` to apply targeted patches and rerun the minimal validating command set.

For release validation, run regression benchmark suite:

```bash
node scripts/run_skill_benchmark.mjs --tasks references/benchmark-tasks.md --run-dir artifacts/ui-parity/<run-id> --out artifacts/ui-parity/<run-id>/benchmark-report.json
```

Finish only when:

- Chosen direction parity is strong on desktop and mobile.
- Required states are implemented.
- State matrix rules pass (`required` complete, `N/A` justified).
- Accessibility thresholds pass.
- Performance budgets pass.
- Objective QA and score threshold pass.

## Output Contract

When reporting completion, include:

- Selected mode and preflight path.
- Direction scoring table and chosen direction rationale.
- Token summary.
- State matrix (`required`/`N/A + justification`).
- QA results and budget pass/fail summary.
- Confidence score (`high`/`medium`/`low`) with reasons tied to gate results and tool coverage.
- Existing-system drift score (when mode is `existing-system`).
- Machine-contract validation results.
- Artifact paths (QA report, mismatch log, screenshots).
- Remaining gaps and rationale (if any).

## References

- `references/mockup-prompt-templates.md`: Prompt scaffolds for `greenfield` and `existing-system` directions.
- `references/quality-gates-checklist.md`: Explicit gates, thresholds, and evidence checklist.
- `references/quality-contract.schema.json`: Machine-checkable QA output contract.
- `references/pass-fail-examples.md`: Calibrated examples of acceptable vs reject output quality.
- `references/failure-remediation-map.md`: Gate-to-fix mapping with exact rerun commands.
- `references/anti-gaming-rules.md`: Rules that prevent parity/QA manipulation.
- `references/benchmark-tasks.md`: Regression benchmark task suite for this skill.
- `assets/design-token-template.json`: Token schema for implementation and fallback mode.
- `scripts/run_ui_quality_gates.mjs`: Automated QA runner.
- `scripts/extract_design_system_context.mjs`: Existing-system token/component extractor.
- `scripts/crawl_ui_states.mjs`: Reachable-state discovery and state-coverage gate.
- `scripts/score_mockup_directions.mjs`: Deterministic direction ranking generator.
- `scripts/compare_ui_screenshots.mjs`: Pixel/SSIM parity scorer with optional masks.
- `scripts/run_skill_benchmark.mjs`: Runs benchmark suite and produces regression report.