# SkillScan PRD

*Updated March 2026 to reflect the expanded offline skill ecosystem vision.*

## 1. Product Overview

SkillScan is the **canonical offline trust layer for the AI agent skill ecosystem**. Before any skill is loaded into an agent runtime — whether in CI, in a developer's editor, or at the registry gate — SkillScan answers the full question: *should I trust this skill?*

That question has three orthogonal dimensions, each served by a dedicated tool:

| Dimension | Question | Tool |
|---|---|---|
| **Safety** | Is this skill trying to do something malicious? | `skillscan-security` |
| **Quality** | Will this skill work correctly with an LLM agent? | `skillscan-lint` |
| **Provenance** | Is this skill what it claims to be, and has it changed? | `skillscan-provenance` (planned) |

The tools share a common data model (`skillscan-core`), produce compatible output formats (SARIF, JSON), and are orchestrated by a thin wrapper (`skillscan-report`) that produces a unified CI report. All analysis is local, deterministic, and requires no network access or cloud services.

## 2. Problem Statement

AI agent skill files are executable instructions that run with agent-level trust. A malicious or compromised skill can exfiltrate credentials, execute arbitrary code, manipulate agent behavior, or silently expand its declared permission scope. As skill registries grow and skills are shared across teams and organizations, the attack surface expands in three ways that existing tools do not address:

**Supply chain attacks.** A trusted skill is updated with a malicious instruction. Neither the registry nor the consuming agent runtime detects the change. Static per-version scanning misses this because each version looks clean in isolation.

**Typosquatting.** A malicious skill is published with a name or instruction set nearly identical to a popular trusted skill. The difference is one added exfiltration instruction. No existing tool performs instruction-level similarity comparison.

**Permission scope inflation.** A skill declares a narrow `allowed-tools` list but its instructions imply access to tools not in that list. Registries display declared permissions but cannot verify they match actual behavior.

Existing tools do not scan skill files for any of these risks before deployment.

## 3. Goals

1. One-command scan experience for non-expert users.
2. Deterministic, explainable verdicting without mandatory LLM use.
3. Policy-driven flexibility with strict default profile.
4. Data-driven detection content via versioned YAML rulepacks.
5. Local intel data management for IOC and vulnerability enrichment.
6. Clear terminal UX and machine-readable export.
7. Detect supply chain attacks via instruction-level behavioral diff between skill versions.
8. Validate that declared permission scopes match the actual capabilities implied by instructions.
9. Detect instruction-level typosquatting against a known-good skill registry.
10. Provide a local dynamic analysis sandbox (`skillscan-sandbox`) for behavioral verification with user-supplied model credentials.
11. Share a common data model and parsing layer (`skillscan-core`) across all tools in the ecosystem.

## 4. Non-Goals

1. Cloud-based scanning or centralized telemetry.
2. Automatic code remediation.
3. Multi-tenant SaaS control plane.
4. Indirect prompt injection detection from external content fetched at runtime (requires runtime observation).
5. Temporal and conditional payload detection via symbolic execution (requires LLM semantic reasoning or dynamic execution).
6. MCP server infrastructure trust validation (requires infrastructure-level signals).
7. Compositional safety analysis across a live agent session (requires runtime observation of the full invocation graph).

*Note: Items 4–7 are addressed within the constraints of the offline paradigm by `skillscan-sandbox` (Milestone 18), which provides local dynamic analysis using a user-supplied model and a fully instrumented fake tool environment. They are non-goals for the static analysis tools only.*

## 5. The Static Analysis Ceiling — A Design Principle

Static offline analysis has a hard ceiling. Almost all of the highest-value gaps — runtime behavior prediction, indirect injection from external content fetched at runtime, temporal and conditional payloads, MCP server infrastructure trust — require either dynamic execution or infrastructure-level signals. These are not gaps we can close with better regex or a larger corpus.

**This is a feature, not a limitation.** The offline/private/deterministic positioning is the reason teams trust SkillScan in security-sensitive environments. We own the offline trust layer completely and are honest about where dynamic analysis begins. We do not half-build dynamic capabilities that would require phoning home, cloud execution, or user key management we cannot control.

## 6. User Segments

1. Developers building or consuming AI agent skills.
2. Security engineers gating internal usage.
3. CI maintainers enforcing scan policies.
4. Incident responders triaging suspicious bundles.
5. Skill registry operators validating submissions before publication.
6. Agent runtime developers integrating trust checks at the loading layer.

## 7. User Stories

1. As a developer, I can scan a skill folder and quickly understand whether I should trust it.
2. As security staff, I can enforce strict thresholds and custom blocklists.
3. As a CI owner, I can fail builds when scans are blocked.
4. As an analyst, I can inspect a saved report with formatted evidence.
5. As an IT team, I can add and manage local intel feeds without external services.
6. As a registry operator, I can run a unified scan (security + lint) on skill submissions and get a single pass/fail verdict.
7. As a security engineer, I can diff two versions of a skill and see which instruction changes are security-relevant.
8. As a developer, I can verify that a skill's declared `allowed-tools` matches what its instructions actually require.
9. As a developer, I can run a skill through a local agent sandbox with my own API key and see what it actually does.

## 8. Product Requirements

### 8.1 Input and Extraction

1. Accept folder, file, and archive inputs.
2. Enforce archive safety checks (path traversal, symlink/hardlink blocks, byte/file limits).
3. Enforce policy scan limits (`max_files`, `max_bytes`, timeout controls).
4. Detect and warn on opaque binary files that cannot be unpacked or recognized as a known media format.

### 8.2 Detection and Analysis (skillscan-security)

1. Static detection of malware-like chains (`curl|bash`, decode-and-exec, risky shell patterns).
2. Instruction-abuse detection in markdown/text.
3. Sensitive access intent detection (`.env`, `id_rsa`, cloud credential markers).
4. IOC extraction from content with basic normalization.
5. Instruction hardening pre-processing: Unicode normalization, zero-width stripping, bounded base64 text-fragment decoding.
6. Deterministic action-chain checks (download+execute, secret+network, privilege+security-disable).
7. Dependency risk checks (vulnerable versions, unpinned version patterns).
8. Capability enumeration (shell, network, filesystem write indicators).
9. Ecosystem hint detection (OpenClaw/ClawHub, Claude-style, OpenAI-style, fallback generic).
10. Offline semantic classifiers for prompt injection and social engineering patterns.
11. Optional offline ML detection (`--ml-detect`) for nuanced instruction-intent risks.
12. Permission scope validation: flag instructions that imply tool access not declared in `allowed-tools` (Milestone 16).
13. Instruction-level typosquatting detection against a known-good skill registry (Milestone 17).

### 8.3 Quality Analysis (skillscan-lint)

1. Structural quality checks: required fields, heading hierarchy, example coverage.
2. LLM-effectiveness checks: passive voice, hedge words, vague quantifiers, ambiguous instructions.
3. SARIF output format for integration with the VS Code extension and `skillscan-report`.
4. `--fix` mode for mechanical rules (whitespace, formatting, missing fields).

### 8.4 Provenance and Diff (skillscan-security + skillscan-core)

1. Instruction-level skill diff: given two versions of a SKILL.md, produce a structured diff with security-relevant changes flagged by rule ID (Milestone 16).
2. Skill identity fingerprinting: deterministic hash of semantically significant skill content, stable across cosmetic changes (Milestone 15).
3. Fingerprint drift detection: `skillscan verify` subcommand for trust-on-first-use (TOFU) workflows (Milestone 16).
4. Instruction-level similarity hashing against a known-good registry (Milestone 17).

### 8.5 Policy Engine

1. Built-in profiles: `strict` (default), `balanced`, `permissive`.
2. Optional custom policy file support.
3. Category weighting and threshold-based scoring.
4. Hard-block rule IDs.
5. Domain allow/block overrides.

### 8.6 Local Intel Layer

1. Built-in IOC and vulnerability datasets.
2. User-managed local sources with add/remove/enable/disable/list/status/rebuild.
3. Source precedence with deterministic merge.
4. Managed intel auto-refresh checks run on each scan.
5. Default refresh when intel age exceeds 60 minutes.
6. Scans proceed even when refresh errors occur.

### 8.7 Output and UX

1. Pretty non-interactive terminal output with clear sections.
2. JSON report export for automation.
3. Explain command to render existing reports.
4. Exit code gates via `--fail-on warn|block|never`.
5. SARIF, JUnit, and compact output formats for CI integration.
6. Unified report (`skillscan-report`) combining security and lint findings from both tools.

### 8.8 Install and Uninstall

1. Convenience `curl|bash` installer script.
2. CLI and shell uninstaller with `--keep-data` option.
3. VS Code extension (Milestone 9) surfacing security and lint findings inline.
4. Pre-commit hook integration.

### 8.9 Local Dynamic Analysis (skillscan-sandbox, Milestone 18)

1. Docker container accepting skill paths, an input prompt, and model credentials.
2. Fully instrumented fake tool environment: canary filesystem, fake network layer, tool call auditor.
3. Default system prompts for common agent personas (coding agent, research agent, customer support agent).
4. Pre-built model configs for Claude, GPT-4o, Gemini, and Ollama (local, no API key required).
5. SARIF output compatible with `skillscan-report` and the VS Code extension.

## 9. CLI Specification

### skillscan-security
1. `skillscan scan <path>`
2. `skillscan explain <report.json>`
3. `skillscan diff <baseline.json> <current.json>` (report diff, existing)
4. `skillscan diff <skill_v1.md> <skill_v2.md>` (instruction diff, Milestone 16)
5. `skillscan verify <skill_path> --baseline <fingerprint>` (Milestone 16)
6. `skillscan policy show-default --profile <name>`
7. `skillscan policy validate <policy.yaml>`
8. `skillscan intel status|list|add|remove|enable|disable|rebuild`
9. `skillscan uninstall [--keep-data]`
10. `skillscan version`
11. ML flags on `scan`: `--ml-detect` (requires `skillscan model sync` first).
12. `skillscan model sync|status` for managing the local ML model checkpoint.

### skillscan-sandbox (Milestone 18)
1. `skillscan-sandbox --skills <path> [<path>...] --prompt <text> --key <api_key>`
2. `skillscan-sandbox --skills <path> [<path>...] --prompt <text> --model ollama/<name>`

## 10. Data Model (Report)

Report includes:

1. Metadata: scanner version, target path/type, policy, intel sources, ecosystem hints.
2. Verdict and score.
3. Findings with IDs, categories, severities, confidence, and evidence paths/snippets.
4. IOC list with list-match status.
5. Dependency vulnerability entries.
6. Capability entries.
7. Semantic classifier scores and optional ML findings.
8. Skill fingerprint (Milestone 15).
9. Permission scope validation findings (Milestone 16).

## 11. Security Model

1. No execution of scanned artifacts in default path.
2. Archive extraction hardening.
3. Binary/null-byte filtering for text-only analysis.
4. Deterministic policy scoring and block gates.
5. Local data operation by default.
6. `skillscan-sandbox` enforces network egress blocking and filesystem isolation at the container level.

## 12. Testing Requirements

1. Unit tests for parser/extraction safety and IOC extraction.
2. Policy profile and scoring tests.
3. Fixture-based malicious and benign regression tests.
4. Ecosystem detection tests.
5. Dependency risk/unpinned behavior tests.
6. CI validation on pull requests.
7. Adversarial regression suite for supply chain attack scenarios (malicious updates, typosquatting, permission scope inflation).

## 13. Documentation Requirements

1. README quickstart and command reference.
2. Threat model, policy guide, intel guide, testing guide.
3. Examples covering benign, suspicious, and compromised-style artifacts.
4. Clear uninstall and data-retention behavior.
5. `SCAN_FEED_POLICY.md` for the public skill feed (Milestone 14).
6. `skillscan-sandbox` design document: canary taxonomy, probe harness format, model config reference.

## 14. Success Criteria

1. New users can install and run first scan in <5 minutes.
2. Strict profile blocks known malicious test fixtures.
3. Docs provide clear policy/intel customization path.
4. CI remains green with deterministic test results.
5. VS Code extension published with security and lint findings surfaced inline.
6. `skillscan diff` detects instruction-level changes between skill versions and flags security-relevant ones.
7. Permission scope validation fires on skills with undeclared tool access.
8. `skillscan-sandbox` runs a skill through a local agent and detects canary file reads and undeclared network calls.
