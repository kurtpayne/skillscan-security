# Threat Model

## Assumptions

- Input artifacts are untrusted.
- Scanner host should be considered trusted.
- Offline intel may be stale and should be updated regularly.

## In-Scope Attacks

- Prompt/instruction abuse in markdown
- Download-and-exec shell patterns
- Obfuscated command chains
- IOC reuse across campaigns
- Dependency vulnerabilities in known datasets
- Archive path traversal and unsafe extraction attempts

## Out of Scope (v1)

- Runtime memory forensics
- Public signing and transparency logs
- Multi-tenant identity and access controls

## Security posture notes

1. SkillScan does not execute scanned artifact code in default scan mode.
2. Scanning verdicts are deterministic and do not require LLMs.
3. Optional ML-based semantic analysis (`--ml-detect`) is supported; it runs locally, is non-executing, and uses a locally-stored LoRA adapter with no external API calls.
4. High-confidence ML semantic findings (`PINJ-ML-*`) are surfaced as `WARN` by default; policy can escalate them to `BLOCK`.
