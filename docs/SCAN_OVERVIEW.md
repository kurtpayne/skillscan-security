# Scan Overview

This guide explains what SkillScan checks, why each check is useful, and how safety is enforced.

## Design principles

1. Untrusted input by default.
2. Static analysis first — no API keys, no network calls, no telemetry.
3. Deterministic policy verdicting.
4. Optional offline ML detection for deeper semantic coverage.

## End-to-end scan stages

1. Target preparation:
- Accepts directory, file, archive, or URL target.
- Archives are extracted with traversal/symlink protections and size/count limits.
- URL mode can follow linked sources with safety controls (same-origin default, max link cap).

2. File filtering:
- Iterates text-like files only.
- Classifies non-text artifacts and raises binary findings (`BIN-*`) for executables/libraries/bytecode/blobs.

3. Instruction hardening:
- Unicode normalization (`NFKC`).
- Zero-width character stripping.
- Defanged IOC normalization (for example `hxxp` -> `http`, `[.]` -> `.`).
- Bounded base64 decoding, including split-fragment patterns.

4. Deterministic rule analysis:
- Static rule matches from YAML rulepacks.
- Action extraction and chain detection (download+execute, secret+network, privilege+disable-security).
- Python AST dataflow checks for secret-to-network and dynamic exec flows.
- Prompt-injection/jailbreak wording checks.
- Social engineering credential harvest checks (`SE-001`).
- Subshell/encoded execution pattern checks.
- npm lifecycle hook abuse checks.
- Bidirectional Unicode obfuscation checks (Trojan Source style).

5. IOC and dependency intelligence:
- Extracts URLs/domains/IPs.
- Correlates indicators against built-in + managed + user intel lists.
- Checks vulnerable dependency versions and unpinned requirements.

6. Capability inference:
- Identifies shell/network/filesystem-write capabilities for analyst context.

7. Offline semantic analysis:
- `LocalPromptInjectionClassifier`: stem-and-score classifier for prompt injection/override language.
- `SocialEngineeringClassifier`: stem-and-score classifier for credential solicitation patterns.
- Adds `PINJ-SEM-001` and `SE-SEM-001` findings when scores exceed thresholds.
- Fully offline — no model download, no API key, no network call.

8. Optional offline ML detection (`--ml-detect`):
- Runs `protectai/deberta-v3-base-prompt-injection-v2` via ONNX or torch.
- Catches nuanced instruction-intent risks not captured by string patterns.
- Requires `pip install skillscan-security[ml-onnx]` and `skillscan model sync` first.
- Fully offline once the model is synced — no API key, no network call during scan.

9. Scoring and verdict:
- Applies policy weights/thresholds.
- Applies hard-block rules.

10. Reporting:
- Pretty terminal output (`scan`, `explain`).
- JSON, SARIF, JUnit, and compact output for CI and automation.

## Why this is valuable

1. Catches obvious malware patterns quickly (`curl|bash`, decode-and-exec).
2. Catches instruction-layer abuse (coercive setup, security-control bypass, social engineering).
3. Catches hidden/obfuscated intent through normalization + decode pipeline.
4. Catches infra risk via IOC and vulnerability correlation.
5. Produces consistent, explainable outputs suitable for CI gates and IR triage.
6. Runs entirely offline — no tokens spent, no data leaves the machine.

## Safety model

1. SkillScan does not execute scanned artifacts.
2. Archive extraction is hardened against common abuse vectors.
3. URL fetching uses explicit safety limits and flags unreadable/skipped sources.
4. No data is sent to external services during a scan. The optional `--ml-detect` layer
   runs inference locally using a downloaded model checkpoint.

## Recommended usage

1. Default: run strict local scan first. This is free, fast, and catches the obvious stuff.
2. For deeper semantic coverage: add `--ml-detect` (requires one-time model sync).
3. In CI: use `--fail-on block` and store JSON artifacts.
4. As a pre-filter: run SkillScan before sending skills to online scanners (Invariant,
   Lakera Guard, etc.) to eliminate easy wins and reduce token spend.
