
[![CI](https://github.com/kurtpayne/skillscan-security/actions/workflows/ci.yml/badge.svg)](https://github.com/kurtpayne/skillscan-security/actions/workflows/ci.yml)
[![CodeQL](https://github.com/kurtpayne/skillscan-security/actions/workflows/codeql.yml/badge.svg)](https://github.com/kurtpayne/skillscan-security/actions/workflows/codeql.yml)
[![PyPI](https://img.shields.io/pypi/v/skillscan-security.svg)](https://pypi.org/project/skillscan-security/)
[![Docker Hub](https://img.shields.io/docker/v/kurtpayne/skillscan-security?label=docker)](https://hub.docker.com/r/kurtpayne/skillscan-security)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](pyproject.toml)

**Free. Private. Offline. No API key required.**

Security scanner for AI agent skills and MCP tool bundles. Part of the [SkillScan](https://skillscan.sh) project.

SkillScan Security catches the obvious stuff so you don't have to pay Claude to find it. It runs entirely on your machine — no network calls, no telemetry, no tokens spent — and returns deterministic verdicts before you ever send a skill to an online scanner.

Use it as a free pre-filter in your CI pipeline. If it blocks, you know immediately. If it passes, you've already eliminated the easy wins before handing off to a deeper (and more expensive) analysis layer.

Verdicts: `allow` · `warn` · `block`

Default policy: `strict`.

---

## Why SkillScan First

Online AI scanners (Invariant, Lakera Guard, and others) are excellent at nuanced intent analysis. They are also billed per token. Running them on every skill in a large repository is expensive.

SkillScan handles the deterministic layer for free:

- Download-and-execute chains
- Secret exfiltration patterns
- Credential harvesting instructions
- Malicious binary artifacts
- Known-bad IOC domains and IPs
- Vulnerable dependency versions
- Prompt injection and instruction override attempts
- Social engineering credential requests

If SkillScan blocks it, you don't need to spend tokens on it. If it passes, you have a clean bill of health on the obvious vectors before your paid scanner runs.

---

## Features

1. **Offline-first.** No network calls required. Runs entirely on your machine.
2. Archive-safe extraction and static analysis.
3. Binary artifact classification and flagging (executables, libraries, bytecode, blobs).
4. Malware and instruction-abuse pattern detection (70+ static rules, 15 chain rules).
5. Instruction hardening pipeline (Unicode normalization, zero-width stripping, bounded base64 decode, action-chain checks).
6. IOC extraction with local intel matching (163 domains, 1,310 IPs, 2 CIDRs — updated twice daily).
7. Dependency vulnerability checks (23 Python + 4 npm packages via OSV.dev).
8. Social engineering and credential-harvest instruction detection (SE-001, SE-SEM-001).
9. Policy profiles (`strict`, `balanced`, `permissive`) + custom policies.
10. Pretty terminal output + JSON / SARIF / JUnit / compact reports.
11. Auto-refresh managed intel feeds (default checks every scan, 1-hour max age).
12. Versioned YAML rulepack for flexible detection updates.
13. Adversarial regression corpus with expected verdicts.
14. Default-on local semantic prompt-injection classifier (NLTK/classical features, no external API).
15. Optional offline ML detection (`--ml-detect`) using a fine-tuned DeBERTa adapter — no API key, no cloud.

---

## Distribution Status

- PyPI: `pip install skillscan-security`
- Docker: `docker pull kurtpayne/skillscan-security`
- Pre-commit hook: `skillscan-security>=0.3.1`

Release process: `docs/RELEASE_CHECKLIST.md` and `docs/RELEASE_ONBOARDING.md`.

SBOMs: Python CycloneDX (`sbom-python.cdx.json`) and Docker SPDX (`sbom-docker.spdx.json`) are included in release artifacts.

Docker default behavior: the image includes ClamAV and enables it by default (`SKILLSCAN_CLAMAV=true`). Override with `--no-clamav`.

---

## Install

### Option A: convenience installer

```bash
curl -fsSL https://raw.githubusercontent.com/kurtpayne/skillscan/main/scripts/install.sh | bash
```

### Option B: pip

```bash
pip install skillscan-security
```

**Base install is ~25 MB.** No torch, no transformers, no heavy ML stack. The `--ml-detect` flag requires an optional extra:

```bash
# CPU-only ONNX inference (~200 MB) — recommended for most users
pip install 'skillscan-security[ml-onnx]'

# Full PyTorch backend (~500 MB) — for GPU environments
pip install 'skillscan-security[ml]'
```

### Option C: local/dev install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

---

## Quick Start

```bash
skillscan scan ./examples/suspicious_skill
```

Scan directly from URL (including GitHub blob URLs):

```bash
skillscan scan "https://github.com/blader/humanizer/blob/main/SKILL.md?plain=1"
```

Save reports:

```bash
# JSON
skillscan scan ./target --format json --out report.json --fail-on never
# SARIF (GitHub code scanning)
skillscan scan ./target --format sarif --out skillscan.sarif --fail-on never
# JUnit XML (CI test report ingestion)
skillscan scan ./target --format junit --out skillscan-junit.xml --fail-on never
# Compact (terse CI logs)
skillscan scan ./target --format compact --fail-on never
```

Render a saved report:

```bash
skillscan explain ./report.json
```

Optional offline ML detection (requires `[ml-onnx]` or `[ml]` extra):

```bash
skillscan scan ./target --ml-detect
```

The ML detector uses a fine-tuned DeBERTa adapter. It runs entirely on your machine — no API calls, no tokens, no cloud. It is the right tool for subtle semantic attacks that the static rules don't catch. For nuanced intent analysis that requires reasoning about context, see the [integration bridges](#integration-bridges) below.

---

## Highlighted Examples

### 1. Download-and-execute chain (critical)

```console
$ skillscan scan examples/showcase/01_download_execute --fail-on never
╭─────────────────────────────── Verdict: BLOCK ───────────────────────────────╮
│ Target: examples/showcase/01_download_execute                                │
│ Policy: strict                                                               │
│ Score: 360                                                                   │
│ Findings: 2                                                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
Top Findings:
- MAL-001 (critical) Download-and-execute chain
- CHN-001 (critical) Dangerous action chain: download plus execute
```

### 2. Secret exfiltration chain (critical)

```console
$ skillscan scan examples/showcase/15_secret_network_chain --fail-on never
╭─────────────────────────────── Verdict: BLOCK ───────────────────────────────╮
│ Target: examples/showcase/15_secret_network_chain                            │
│ Policy: strict                                                               │
│ Score: 285                                                                   │
│ Findings: 2                                                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
Top Findings:
- EXF-001 (high) Sensitive credential file access
- CHN-002 (critical) Potential secret exfiltration chain
```

### 3. Social engineering credential harvest (critical)

```console
$ skillscan scan examples/showcase/20_social_engineering_credential_harvest --fail-on never
╭─────────────────────────────── Verdict: BLOCK ───────────────────────────────╮
│ Target: examples/showcase/20_social_engineering_credential_harvest           │
│ Policy: strict                                                               │
│ Score: 95                                                                    │
│ Findings: 2                                                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
Top Findings:
- SE-001 (high) Social engineering credential harvest
- PINJ-SEM-001 (medium) Semantic prompt injection signal
```

### 4. npm lifecycle supply-chain abuse

```console
$ skillscan scan examples/showcase/21_npm_lifecycle_abuse --fail-on never
╭─────────────────────────────── Verdict: BLOCK ───────────────────────────────╮
│ Target: examples/showcase/21_npm_lifecycle_abuse                             │
│ Policy: strict                                                               │
│ Score: 465                                                                   │
│ Findings: 3                                                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
Top Findings:
- MAL-001 (critical) Download-and-execute chain
- CHN-001 (critical) Dangerous action chain: download plus execute
- SUP-001 (high) Risky npm lifecycle script: preinstall
```

### 5. Executable binary artifact detection

```console
$ skillscan scan examples/showcase/24_binary_artifact --fail-on never
╭─────────────────────────────── Verdict: WARN ────────────────────────────────╮
│ Target: examples/showcase/24_binary_artifact                                 │
│ Policy: strict                                                               │
│ Score: 35                                                                    │
│ Findings: 1                                                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
Top Findings:
- BIN-001 (high) Executable binary artifact present
```

---

## Command Summary

- `skillscan scan <path>`
- `skillscan explain <report.json>`
- `skillscan policy show-default --profile strict|balanced|permissive`
- `skillscan policy validate <policy.yaml>`
- `skillscan intel status|list|add|remove|enable|disable|rebuild`
- `skillscan intel sync [--force]`
- `skillscan rule list [--format json]`
- `skillscan uninstall [--keep-data]`
- `skillscan-security version`

See full command docs: `docs/COMMANDS.md`.

---

## Policies

Built-ins:

1. `strict` (default)
2. `balanced`
3. `permissive`

Use a custom policy:

```bash
skillscan scan ./target --policy ./examples/policies/strict_custom.yaml
```

---

## Intel Management

Add a local IOC source:

```bash
skillscan intel add ./examples/intel/custom_iocs.json --type ioc --name team-iocs
```

View sources:

```bash
skillscan intel status
skillscan intel list
```

Managed intel auto-refresh runs by default on `scan`. You can tune or disable it:

```bash
skillscan scan ./target --intel-max-age-minutes 60
skillscan scan ./target --no-auto-intel
skillscan intel sync --force
```

---

## Integration Bridges

SkillScan is designed to be the **free pre-filter** in a layered scanning pipeline. It handles deterministic checks locally so you don't spend tokens on the obvious cases. For nuanced intent analysis, pair it with an online scanner.

### Use SkillScan as a pre-filter for Invariant

[Invariant Analyzer](https://github.com/invariantlabs-ai/invariant) provides deep semantic analysis of agent traces and skill files. Run SkillScan first to eliminate clear-cut cases:

```bash
# Only send to Invariant if SkillScan doesn't block
skillscan scan ./skill --format json --out pre-filter.json --fail-on never
if [ "$(jq -r '.verdict' pre-filter.json)" != "block" ]; then
  invariant analyze ./skill
fi
```

Or in CI:

```yaml
- name: SkillScan pre-filter
  run: skillscan scan ./skills --format sarif --out skillscan.sarif
  continue-on-error: true

- name: Upload SkillScan results
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: skillscan.sarif

- name: Deep scan (only if SkillScan passes)
  if: steps.skillscan.outcome == 'success'
  run: invariant analyze ./skills
```

### Use SkillScan as a pre-filter for Lakera Guard

[Lakera Guard](https://www.lakera.ai/) provides real-time prompt injection detection via API. SkillScan catches the static patterns for free before you hit the API:

```python
import subprocess, json, requests

result = subprocess.run(
    ["skillscan", "scan", skill_path, "--format", "json", "--fail-on", "never"],
    capture_output=True, text=True
)
report = json.loads(result.stdout)

if report["verdict"] == "block":
    # SkillScan caught it — no API call needed
    raise ValueError(f"Skill blocked by SkillScan: {report['top_findings']}")

# SkillScan passed — send to Lakera for semantic analysis
response = requests.post(
    "https://api.lakera.ai/v1/prompt_injection",
    headers={"Authorization": f"Bearer {LAKERA_API_KEY}"},
    json={"input": skill_content}
)
```

### Pre-commit hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/kurtpayne/skillscan-security
    rev: v0.3.1
    hooks:
      - id: skillscan
        args: [--fail-on, warn]
```

---

## Example Fixtures

1. Benign sample: `examples/benign_skill`
2. Suspicious sample: `examples/suspicious_skill`
3. OpenAI-style sample: `examples/openai_style_tool`
4. Claude-style sample: `examples/claude_style_skill`
5. Comprehensive detection showcase: `examples/showcase/INDEX.md`
6. Social engineering sample: `examples/showcase/20_social_engineering_credential_harvest`
7. OpenClaw-compromised-style sample: `tests/fixtures/malicious/openclaw_compromised_like`

---

## Cross-Platform Skill Bundles

Starter bundles for OpenClaw/ClawHub, Claude-style skills, and OpenAI Actions are in:

- `integrations/openclaw/`
- `integrations/claude/`
- `integrations/openai/`

See the [Platform Bundles](docs/DISTRIBUTION.md#platform-bundles) section of the Distribution Guide for setup and rollout guidance.

---

## Testing

```bash
./scripts/run_tests.sh test
./scripts/run_tests.sh lint
./scripts/run_tests.sh type
./scripts/run_tests.sh check
```

Or via Makefile:

```bash
make check
```

---

## CI/CD Integration

SkillScan provides a reusable GitHub Actions workflow for scanning skill artifacts in CI pipelines with native SARIF upload to the GitHub Security tab.

```yaml
jobs:
  skillscan:
    uses: kurtpayne/skillscan-security/.github/workflows/skillscan-scan.yml@main
    with:
      scan-path: ./skills
```

See `docs/GITHUB_ACTIONS.md` for full documentation and examples.

---

## Uninstall

```bash
skillscan uninstall
# Keep local data (intel/reports/config):
skillscan uninstall --keep-data
```

Shell script uninstall: `scripts/uninstall.sh`.

---

## Documentation

- Detection model: `docs/DETECTION_MODEL.md`
- Scan overview: `docs/SCAN_OVERVIEW.md`
- Architecture: `docs/ARCHITECTURE.md`
- Threat model: `docs/THREAT_MODEL.md`
- Policy guide: `docs/POLICY.md`
- Intel guide: `docs/INTEL.md`
- Testing guide: `docs/TESTING.md`
- Rules and scoring: `docs/RULES.md`
- Comprehensive examples: `docs/EXAMPLES.md`
- GitHub Actions integration: `docs/GITHUB_ACTIONS.md`
- Distribution: `docs/DISTRIBUTION.md`
- Release onboarding: `docs/RELEASE_ONBOARDING.md`
- Release checklist: `docs/RELEASE_CHECKLIST.md`
- PRD: `docs/PRD.md`

---

## Related

- **[skillscan-lint](https://github.com/kurtpayne/skillscan-lint)** — Quality linter for AI agent skills: readability, clarity, graph integrity
- **[Invariant Analyzer](https://github.com/invariantlabs-ai/invariant)** — Deep semantic analysis of agent traces; use SkillScan as a free pre-filter
- **[Lakera Guard](https://www.lakera.ai/)** — Real-time prompt injection detection API; use SkillScan to eliminate static cases before hitting the API
- **[skills.sh](https://skills.sh)** — Community registry of AI agent skills
- **[ClawHub](https://clawhub.ai)** — MCP skill marketplace
- **[Docker Hub](https://hub.docker.com/r/kurtpayne/skillscan-security)** — `docker pull kurtpayne/skillscan-security`
- **[PyPI](https://pypi.org/project/skillscan-security/)** — `pip install skillscan-security`

---

## License

Licensed under Apache-2.0. See `LICENSE`.

## Security Note

SkillScan performs static analysis by default and does not execute scanned artifacts. For untrusted inputs, run in a trusted isolated environment.

For URL scans, unreadable linked sources are reported as low-severity `SRC-READ-ERR` findings. They are flagged for review but are not treated as malicious by default.
