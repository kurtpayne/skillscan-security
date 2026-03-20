---
name: trigger-trap
description: Trap and rewrite/cancel undesired outbound agent asks before they reach the operator. Use when an agent needs enforcement for evidence-first questioning, anti-veiled-ask behavior (for example "if you want"), and 1-3-1 bypass rules through a pre-send ask-gate with audit logs and proof tests.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: sene1337/trigger-trap
# corpus-url: https://github.com/sene1337/trigger-trap/blob/d8be0a9ccce3537a108efae6bff5d1c706600908/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Trigger Trap

Implement a pre-send ask-gate that blocks or rewrites low-quality asks before they trigger the human.

Treat Trigger Trap as a runtime hard gate for behavior drift that can persist even when bootstrap-file hard gates exist. Bootstrap rules define policy; Trigger Trap enforces it at send time.

## Outcomes
- Enforce evidence-first before question-form outbound messages.
- Catch veiled asks (`if you want`, `if you'd like`, `let me know if`) even without `?`.
- Allow explicit structured bypasses (1-3-1, DONE/BLOCKED, HEARTBEAT_OK).
- Produce auditable decisions in a log.
- Extend easily: add or remove pattern rules, bypass rules, target scopes, and action modes without redesigning the whole gate.

## Files in this skill
- `scripts/pre-ask-gate.sh` — mint short-TTL evidence token.
- `scripts/send-guard.sh` — CLI guard for outbound text checks.
- `scripts/ask-gate-runtime-proof.mjs` — matrix proof harness.
- `references/runtime-integration.md` — runtime plugin wiring and config.
- `references/validation-matrix.md` — pass/fail matrix and smoke checklist.

## Workflow
1. Wire the runtime gate (see `references/runtime-integration.md`).
2. Configure owner target, mode (`rewrite|cancel`), token TTL, and audit path.
3. Run proof harness and ensure all matrix cases pass.
4. Run one live smoke message for blocked veiled ask + one allowed bypass.
5. Review logs to confirm real behavior and report only from concrete evidence.

## Guardrails
- Scope the gate to the target channel/recipient you intend to protect (explicit Telegram channel + explicit operator chat ID).
- Default to `cancel` in production to prevent user-facing block spam; pair with next-turn 1-3-1 remediation injection.
- Use `dryRun=true` for safe rollout tuning, then switch to `dryRun=false` for enforcement.
- Use fail-open behavior on hook errors (fallback passthrough) so delivery is never silently broken by gate bugs.
- Never treat script existence as proof; require runtime evidence + logs.
- Mandatory: review `ask-guard.log` decisions (ALLOW/BLOCK/PASS/BYPASS) to determine whether Trigger Trap is working as intended.