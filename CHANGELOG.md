# Changelog

All notable changes to `skillscan-security` are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.3.2] — 2026-03-18

### Added
- **SE-001**: social engineering credential harvest static rule (HIGH) — detects instructions that solicit API tokens, passwords, or session cookies from users.
- **SE-SEM-001**: offline semantic social engineering classifier — stem-and-score classifier for credential solicitation patterns.
- **Intel DB seeding**: IOC DB expanded from 11 to 1,475 entries (163 domains, 1,310 IPs, 2 CIDRs) from URLhaus, Feodo Tracker, and Spamhaus DROP.
- **Vuln DB seeding**: vuln DB expanded from 4 to 27 packages with 111 versions from OSV.dev.
- **docs/DETECTION_MODEL.md**: comprehensive detection architecture documentation covering all 8 layers.
- **Showcase example 20**: renamed from `20_ai_semantic_risk` to `20_social_engineering_credential_harvest`.

### Removed
- **AI assist layer** (`--ai-assist`, `--ai-provider`, `--ai-model`, `--ai-base-url`, `--ai-required`): removed entirely. SkillScan is repositioned as a free, offline, privacy-first pre-filter. For nuanced semantic analysis, use Invariant Analyzer or Lakera Guard after SkillScan passes.

---

## [0.3.1] — 2026-03-17

### Added
- **Skill graph analysis** (`skillscan scan --graph`): structural analysis of skill invocation graphs. Three new rules:
  - `PINJ-GRAPH-001` — skill loads a remote `.md` file at runtime (dead-drop instruction injection, HIGH)
  - `PINJ-GRAPH-002` — skill grants `Bash`/`Computer`/`Shell` tool without a declared purpose section (MEDIUM)
  - `PINJ-GRAPH-003` — skill instructs agent to write memory files (`SOUL.md`, `MEMORY.md`, `AGENTS.md`, `.claude/settings.json`) (CRITICAL)
- **ML-based prompt injection detection** (`skillscan scan --ml-detect`): ONNX INT8 DeBERTa adapter trained on 111-example corpus. Adds `PINJ-ML-*` findings.
- **`skillscan model` commands**: `model sync` (download/update ONNX model), `model status` (show age, staleness). Emits `PINJ-ML-STALE` at 30 days, `PINJ-ML-UNAVAIL` when not installed.
- **`skillscan rule` commands**: `rule sync` (pull latest rulepack), `rule status` (show version, age).
- **Reusable GitHub Actions workflow** (`.github/workflows/skillscan-reusable.yml`): call from any repo with `uses: kurtpayne/skillscan-security/.github/workflows/skillscan-reusable.yml@main`. Outputs SARIF to GitHub Security tab.
- **Pre-commit hook** (`.pre-commit-hooks.yaml`): `skillscan-security` and `skillscan-lint` hooks for local dev gates.
- **VS Code extension scaffold** (`editors/vscode/`): TypeScript extension with status bar, inline diagnostics, and marketplace publish workflow.
- **Homebrew formula** (`packaging/homebrew/skillscan-security.rb`).
- **Signature-as-data architecture**: rules, IOCs, and ML model are versioned data artifacts separate from the scanner binary. Auto-updated via `corpus-sync` workflow.
- **MAL-029**: Solana RPC blockchain C2 resolution (GlassWorm Wave 5 — `getSignaturesForAddress` dead-drop technique).
- **CORPUS_CARD.md**: reproducibility metadata for the ML training corpus (SHA, example counts, fine-tune history).

### Changed
- `PINJ-ML-UNAVAIL` now emits a finding (was a silent skip) when ML model is not installed and `--ml-detect` is passed.
- `pyproject.toml`: added PyPI classifiers, keywords, project URLs, and Docker Hub / GitHub links.
- README: corrected badge URLs, added PyPI + Docker Hub badges, added skillscan.sh and Related section.

### Fixed
- `eval_strategy` parameter name for `transformers>=4.46` compatibility in fine-tune script.
- Corpus manifest `sha256_index` race condition between corpus-sync and fine-tune jobs (added `push_options: --force-with-lease`).

---

## [0.3.0] — 2026-03-10

### Added
- **Signature-as-data foundation**: `src/skillscan/data/` directory for versioned rules, IOCs, and vulnerability DB.
- **Corpus pipeline**: `corpus/` directory with 111 labeled examples (54 benign / 57 injection), `corpus/manifest.json`, automated scraping via `corpus-sync` workflow.
- **`skillscan corpus` commands**: `corpus status`, `corpus add`, `corpus sync`.
- **MAL-025 through MAL-028**: GlassWorm Wave 4 patterns (npm typosquatting, MCP tool poisoning, cross-server namespace collision, rug-pull mutation).
- **CVE-2026-4270**: `@awslabs/aws-api-mcp-server` path traversal (CVSS 6.8, fixed in 1.3.9).
- **IOC additions**: 6 GlassWorm/PylangGhost IPs, 3 domains.
- **Chain rules**: 14 multi-step attack chain detectors.
- **Action patterns**: 19 behavioral action pattern detectors.
- **Capability patterns**: 3 capability escalation detectors.

### Changed
- Rule count: 64 static + 14 chain + 19 action + 3 capability = **100 total rules**.
- Rules version: `2026.03.17.3`.

---

## [0.2.3] — 2026-02-28

### Added
- Docker Hub release pipeline (`release-docker.yml`).
- PyPI trusted publisher configuration (`release-pypi.yml`) with SBOM and cosign signing.
- SARIF output format for GitHub Security tab integration.
- Offline semantic prompt injection classifier (`PINJ-SEM-001`).
- Policy profiles: `strict`, `balanced`, `permissive`.
- URL scanning: follow links up to configurable depth.

### Fixed
- Archive extraction handling for nested zip/tar.gz artifacts.
- Unicode normalization edge cases in instruction hardening pipeline.

---

## [0.2.0] — 2026-02-10

### Added
- Binary artifact classification (executables, libraries, bytecode, blobs).
- IOC extraction with local intel matching.
- Dependency vulnerability and unpinned-version checks.
- `skillscan intel` command group for managing local intel sources.
- Pretty terminal output with color-coded verdicts.
- JSON report format with structured findings.

---

## [0.1.0] — 2026-01-20

### Added
- Initial release.
- Static analysis of SKILL.md files: malware patterns, instruction abuse, Unicode attacks.
- Archive-safe extraction pipeline.
- Verdicts: `allow`, `warn`, `block`.
- Policy enforcement via YAML policy files.
- `skillscan scan`, `skillscan explain`, `skillscan policy` commands.
- 29 initial detection rules.

[0.3.2]: https://github.com/kurtpayne/skillscan-security/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/kurtpayne/skillscan-security/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/kurtpayne/skillscan-security/compare/v0.2.3...v0.3.0
[0.2.3]: https://github.com/kurtpayne/skillscan-security/compare/v0.2.0...v0.2.3
[0.2.0]: https://github.com/kurtpayne/skillscan-security/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/kurtpayne/skillscan-security/releases/tag/v0.1.0
