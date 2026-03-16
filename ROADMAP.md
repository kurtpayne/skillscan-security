# SkillScan Roadmap (Beyond Pattern Adds)

This roadmap focuses on product value beyond adding more static rules.

## North Star

Make SkillScan the easiest and most trusted way to gate AI-skill/tool risk in local dev and CI:

- **Fast to adopt** (`pip` + Docker + CI templates)
- **Actionable outputs** (explainability, low-noise scoring)
- **Broader coverage** (content + artifacts + workflow abuse)
- **Operationally reliable** (versioned releases, compatibility guarantees)

---

## Milestone 0 — Foundation & Packaging (2 weeks)

### Epic A: Distribution Hardening

#### Issue A1 — PyPI publishing pipeline
- Add automated release on git tag.
- Build/test wheels in CI.
- Sign artifacts (or provide checksums + provenance notes).

**Acceptance criteria**
- `pip install skillscan-security` works on Linux/macOS.
- Tagged release publishes package and release notes.
- Install time from clean machine < 5 minutes.

#### Issue A2 — DockerHub multi-arch image
- Build `linux/amd64` and `linux/arm64` images.
- Keep image minimal (slim/distroless where feasible).
- Add documented bind-mount scan examples.

**Acceptance criteria**
- `docker run ... skillscan scan /work` works on both arches.
- Published tags map to app versions.
- Startup + first scan docs validated in CI smoke job.

#### Issue A3 — Distribution docs refresh
- Add dedicated `docs/DISTRIBUTION.md`.
- Include install matrix (`pip`, `docker`, source).
- Add upgrade + rollback guidance.

**Acceptance criteria**
- New user can choose an install path in < 2 minutes.
- Docs include copy-paste commands for all supported paths.

---

## Milestone 1 — CI Adoption & Explainability (2–3 weeks)

### Epic B: CI-Native Integrations

#### Issue B1 — SARIF export
- Add `--format sarif` output.
- Map rule IDs/severity/confidence to SARIF schema.

**Acceptance criteria**
- SARIF validates and uploads in GitHub code scanning.
- Findings preserve stable IDs and source locations.

#### Issue B2 — JUnit/compact CI output
- Add JUnit-compatible summary mode.
- Add compact non-interactive terminal mode for CI logs.

**Acceptance criteria**
- CI can fail on configured thresholds with concise output.
- JUnit report consumable by common CI dashboards.

### Epic C: Explainability & Triage UX

#### Issue C1 — Finding narratives
- Add “why fired” + “likely impact” + “next action” per finding.
- Group related findings into a chain narrative where applicable.

**Acceptance criteria**
- Top findings show root-cause context without reading raw regex.
- At least 3 chain examples produce grouped explanations.

#### Issue C2 — Confidence labels
- Add confidence bands (`experimental`, `medium`, `high`).
- Include confidence guidance in docs.

**Acceptance criteria**
- Reports consistently render confidence bands.
- Policy supports optional confidence minimum for blocking.

---

## Milestone 2 — Detection Breadth (3–4 weeks)

### Epic D: Prompt-Injection Semantic Assist (Hybrid)

#### Issue D1 — Non-blocking semantic pass
- Add optional NLP/LLM-assisted prompt-injection classifier.
- Keep deterministic rules as primary; semantic findings additive.

**Acceptance criteria**
- Semantic mode is opt-in and clearly labeled.
- Reports include evidence snippets, not opaque verdicts.
- No default hard-blocks from semantic-only findings.

#### Issue D2 — Evaluation harness
- Build benchmark set for injection/abuse examples.
- Track precision/recall drift across releases.

**Acceptance criteria**
- Benchmark command exists and runs in CI nightly.
- Regression threshold alerts on quality degradation.

### Epic E: Artifact Scanning Adapters

#### Issue E1 — ClamAV optional adapter
- Add optional ClamAV scan stage for extracted artifacts.
- Merge ClamAV indicators into SkillScan report model.

**Acceptance criteria**
- Adapter can be toggled on/off by CLI flag.
- Missing ClamAV fails gracefully with explicit guidance.
- Findings map to distinct category (`artifact_malware` or similar).

#### Issue E2 — File-type aware scanning policy
- Add policy knobs for binary scanning scope/limits.
- Improve archive traversal and artifact-type classification.

**Acceptance criteria**
- Users can tune binary scan depth/size/time limits.
- No major scan-time regression (>20%) on standard fixture corpus.

---

## Milestone 3 — Team-Scale Operations (2–3 weeks)

### Epic F: Baselines, Suppressions, and Rulepack Channels

#### Issue F1 — Baseline/diff mode
- Add baseline report compare mode to highlight new risks only.

**Acceptance criteria**
- Users can compare `HEAD` vs baseline report in one command.
- Delta output clearly separates new/resolved findings.

#### Issue F2 — Suppression workflow with expiry
- Add suppression file with reason + expiration date.
- Warn on expired suppressions.

**Acceptance criteria**
- Suppressions are auditable and time-bounded.
- Expired suppressions fail CI in strict mode (configurable).

#### Issue F3 — Rulepack channels
- Introduce `stable`, `preview`, `labs` channels for rule updates.

**Acceptance criteria**
- Users can pin channel/version.
- Release notes indicate promoted/experimental rules.

---

## Proposed PR Sequence (Small, Mergeable)

1. `docs: add ROADMAP.md and distribution architecture notes`
2. `build: add PyPI publish workflow + versioning guardrails`
3. `build: add Docker multi-arch publish workflow`
4. `feat(cli): add SARIF exporter`
5. `feat(cli): add JUnit/compact CI output`
6. `feat(report): add finding explainability blocks`
7. `feat(policy): confidence thresholds + labels`
8. `feat(ai): add optional prompt-injection semantic assist`
9. `test: add semantic benchmark harness`
10. `feat(adapter): add optional ClamAV integration`
11. `feat(cli): baseline diff mode`
12. `feat(policy): suppression file with expiry`
13. `feat(rulepack): channel support stable/preview/labs`

---

## Risks & Guardrails

- **False positives from semantic detection**
  - Guardrail: semantic findings are advisory by default; require evidence snippets.

- **Performance regressions from extra scanners**
  - Guardrail: strict budgets (timeout, bytes, files), benchmark gates in CI.

- **Distribution drift / broken installs**
  - Guardrail: release smoke tests for `pip` and Docker on each tag.

- **Complexity creep**
  - Guardrail: keep features optional and policy-driven; preserve deterministic core.

---

## Success Metrics

- Time-to-first-scan: < 5 minutes for `pip` or Docker path.
- CI adoption: SARIF/JUnit used in at least one reference pipeline.
- Quality: lower noisy-findings rate release-over-release.
- Coverage: measurable increase in high-signal detections beyond static pattern adds.
- Usability: analysts can action top findings without opening source files in most cases.
