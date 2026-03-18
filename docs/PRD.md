# SkillScan PRD

## 1. Product Overview

SkillScan is a standalone, offline-first CLI security analyzer for AI skills and tool bundles (code + markdown instructions). It evaluates artifacts before install/use and produces a deterministic verdict:

- `allow`
- `warn`
- `block`

SkillScan focuses on practical supply-chain and instruction-abuse risk for ecosystems including OpenClaw/ClawHub-style skills, Claude-style skills, and OpenAI-style tool bundles.

## 2. Problem Statement

AI skill bundles combine executable code and natural language instructions. Existing scanners typically inspect code only and miss instruction-layer abuse patterns such as coercive prerequisites and exfiltration instructions.

Teams need a local tool that:

1. Works in untrusted environments without cloud dependency.
2. Surfaces permissions, IOCs, dependency risk, and suspicious instruction behavior.
3. Is easy for default users and tunable for IT/security operators.

## 3. Goals

1. One-command scan experience for non-expert users.
2. Deterministic, explainable verdicting without mandatory LLM use.
3. Policy-driven flexibility with strict default profile.
4. Data-driven detection content via versioned YAML rulepacks.
5. Local intel data management for IOC and vulnerability enrichment.
6. Clear terminal UX and machine-readable export.

## 4. Non-Goals (v1)

1. No GUI application.
2. No SaaS control plane (RBAC/API keys/multi-tenant).
3. No public signing or transparency log workflow.
4. No automatic code remediation.
5. No mandatory dynamic detonation.

## 5. User Segments

1. Developers evaluating third-party skills.
2. Security engineers gating internal usage.
3. CI maintainers enforcing scan policies.
4. Incident responders triaging suspicious bundles.

## 6. User Stories

1. As a developer, I can scan a skill folder and quickly understand whether I should trust it.
2. As security staff, I can enforce strict thresholds and custom blocklists.
3. As a CI owner, I can fail builds when scans are blocked.
4. As an analyst, I can inspect a saved report with formatted evidence.
5. As an IT team, I can add and manage local intel feeds without external services.

## 7. Product Requirements

### 7.1 Input and Extraction

1. Accept folder, file, and archive inputs.
2. Enforce archive safety checks (path traversal, symlink/hardlink blocks, byte/file limits).
3. Enforce policy scan limits (`max_files`, `max_bytes`, timeout controls).

### 7.2 Detection and Analysis

1. Static detection of malware-like chains (`curl|bash`, decode-and-exec, risky shell patterns).
2. Instruction-abuse detection in markdown/text.
3. Sensitive access intent detection (`.env`, `id_rsa`, cloud credential markers).
4. IOC extraction from content with basic normalization.
5. Instruction hardening pre-processing:
6. Unicode normalization and zero-width stripping.
7. Bounded base64 text-fragment decoding.
8. Deterministic action-chain checks (download+execute, secret+network, privilege+security-disable).
9. Dependency risk checks (vulnerable versions, unpinned version patterns).
10. Capability enumeration (shell, network, filesystem write indicators).
11. Ecosystem hint detection (OpenClaw/ClawHub, Claude-style, OpenAI-style, fallback generic).
12. Offline semantic classifiers for prompt injection and social engineering patterns.
13. Optional offline ML detection (`--ml-detect`) for nuanced instruction-intent risks.

### 7.3 Policy Engine

1. Built-in profiles: `strict` (default), `balanced`, `permissive`.
2. Optional custom policy file support.
3. Category weighting and threshold-based scoring.
4. Hard-block rule IDs.
5. Domain allow/block overrides.

### 7.4 Local Intel Layer

1. Built-in IOC and vulnerability datasets.
2. User-managed local sources with add/remove/enable/disable/list/status/rebuild.
3. Source precedence with deterministic merge.
4. Managed intel auto-refresh checks run on each scan.
5. Default refresh when intel age exceeds 60 minutes.
6. Scans proceed even when refresh errors occur.

### 7.5 Output and UX

1. Pretty non-interactive terminal output with clear sections.
2. JSON report export for automation.
3. Explain command to render existing reports.
4. Exit code gates via `--fail-on warn|block|never`.
5. SARIF, JUnit, and compact output formats for CI integration.

### 7.6 Install and Uninstall

1. Convenience `curl|bash` installer script.
2. CLI and shell uninstaller with `--keep-data` option.

## 8. CLI Specification

1. `skillscan scan <path>`
2. `skillscan explain <report.json>`
3. `skillscan policy show-default --profile <name>`
4. `skillscan policy validate <policy.yaml>`
5. `skillscan intel status|list|add|remove|enable|disable|rebuild`
6. `skillscan uninstall [--keep-data]`
7. `skillscan version`
8. ML flags on `scan`: `--ml-detect` (requires `skillscan model sync` first).
9. `skillscan model sync|status` for managing the local ML model checkpoint.

## 9. Data Model (Report)

Report includes:

1. Metadata: scanner version, target path/type, policy, intel sources, ecosystem hints.
2. Verdict and score.
3. Findings with IDs, categories, severities, confidence, and evidence paths/snippets.
4. IOC list with list-match status.
5. Dependency vulnerability entries.
6. Capability entries.
7. Semantic classifier scores and optional ML findings.

## 10. Security Model

1. No execution of scanned artifacts in default path.
2. Archive extraction hardening.
3. Binary/null-byte filtering for text-only analysis.
4. Deterministic policy scoring and block gates.
5. Local data operation by default.

## 11. Testing Requirements

1. Unit tests for parser/extraction safety and IOC extraction.
2. Policy profile and scoring tests.
3. Fixture-based malicious and benign regression tests.
4. Ecosystem detection tests.
5. Dependency risk/unpinned behavior tests.
6. CI validation on pull requests.

## 12. Documentation Requirements

1. README quickstart and command reference.
2. Threat model, policy guide, intel guide, testing guide.
3. Examples covering benign, suspicious, and compromised-style artifacts.
4. Clear uninstall and data-retention behavior.

## 13. Roadmap

### v0.1 (current)

1. Static scanner core with strict default policy.
2. Local intel management.
3. Pretty CLI output and JSON export.
4. Test fixtures and CI.

### v0.2

1. Broader dependency parser coverage.
2. SARIF export.
3. Optional plugin interface for ecosystem-specific analyzers.

### v0.3+

1. Optional sandboxed behavior profile.
2. Corpus expansion and held-out eval set for detection quality measurement.

## 14. Success Criteria

1. New users can install and run first scan in <5 minutes.
2. Strict profile blocks known malicious test fixtures.
3. Docs provide clear policy/intel customization path.
4. CI remains green with deterministic test results.
