---
name: windows-toolchain-forensics
description: Forensic debugger for messy Windows dev setups. Use when users report in casual language that installs "look done" but still fail, PATH/shell behavior is inconsistent, tools only work in one terminal/editor, or prior-agent changes cannot be verified.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: ahmiershadowman-commits/Windows-Toolchain-Forensics
# corpus-url: https://github.com/ahmiershadowman-commits/Windows-Toolchain-Forensics/blob/d6931b36ba15d03a0055ab10a6954d8802bcffc5/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Windows Toolchain Forensics

Execute forensic triage for broken Windows development environments using a safety-first, evidence-first workflow.

## Trigger quickly on casual language (tightly wired)

Activate this skill when user intent matches environment fragmentation, even if wording is non-technical.

### Plain-language trigger phrases

- "my Windows setup is a mess"
- "PATH is cursed" / "my path is broken"
- "it works here but not there"
- "agent/bot said it fixed it but it's still broken"
- "I don't know what's actually installed anymore"
- "I installed it and it still says command not found"
- "VS Code works but terminal doesn't" (or the reverse)
- "everything got worse after installing X"

### Hard trigger conditions

Run this skill if **any** of the following are true:

1. The same command behaves differently across shells/editors.
2. Tool resolution is ambiguous (multiple binaries, unknown path origin, shim/wrapper suspicion).
3. Prior-agent claims conflict with current machine behavior.
4. Multiple ecosystems are failing and root cause is unclear.
5. Package-manager success does not match runtime reality.

If none apply, do standard troubleshooting instead.

## Follow these operating rules

1. Start in **INSPECTION** mode (read-only).
2. Treat all claims as untrusted until verified.
3. Negotiate capabilities up front (what can/can't be observed in this host).
4. Check policy and security stop conditions before remediation.
5. Require explicit approval before state-changing commands.
6. Prefer reversible changes, quarantine, and rollback manifests over destructive cleanup.
7. Verify each fix across PowerShell, CMD, and relevant editor/WSL contexts.
8. Treat CMD `Command Processor\AutoRun` as a mandatory shell-mutation check, not optional.
9. For GPU/runtime validation, prefer capability probes (real execution) over metadata fields.

## Run this workflow

### 1) Frame the case

- Capture failing command(s), context(s), and expected behavior.
- Capture what changed recently (installer, agent action, policy update, shell profile edits).
- Define a measurable success condition.

### 1.5) Capability negotiation (mandatory)

Before deep inspection, explicitly state whether you can do each of the following:

- run shell commands,
- inspect filesystem,
- inspect env variables,
- compare multiple shells/contexts,
- read registry/policy surfaces,
- access prior-agent claim history.

If any are unavailable, mark affected conclusions as **Unknown (access-limited)** instead of "not present."

### 2) Enforce mode state

Use this state object in responses when remediation is being discussed:

```json
{
  "mode_state": {
    "current_mode": "INSPECTION",
    "pending_changes": [],
    "approved_changes": [],
    "rollback_available": false
  }
}
```

Transition only as follows:

- INSPECTION → GUIDED: user requests proposed changes.
- GUIDED → EXECUTION: user explicitly approves concrete change list.
- Any mode → INSPECTION: failure, timeout, ambiguity, or user cancel.

### 3) Check stop conditions first

Before proposing repair, validate policy/security blockers (execution policy, MOTW/SmartScreen/Defender, AppLocker/WDAC, proxy/cert constraints, privilege limits).

Execution policy must be interpreted correctly:

- script/profile execution may be blocked,
- while interactive diagnostics may still work.

Also explicitly distinguish Windows PowerShell 5.1 from PowerShell 7+ during triage.

Mandatory shell-policy checks must include:

- `HKCU\Software\Microsoft\Command Processor\AutoRun`
- `HKLM\Software\Microsoft\Command Processor\AutoRun`

Any non-empty AutoRun value is a high-priority branch because it can mutate CMD behavior globally.

Load `references/RED-FLAG-INDEX.md` for rapid indicator-to-root-cause mapping, then escalate blockers before touching toolchain state.

### 4) Perform layered forensics

Use the full staged procedure in `references/PLAYBOOK.md`.

At minimum, inspect:

- **Layer 0:** policy/security blockers.
- **Layer 1:** PATH and environment precedence.
- **Layer 2:** package manager/shim integrity.
- **Layer 3:** runtime and dependency coherence.
- **Layer 4:** shell/profile/editor injection.
- **Layer 5:** project-local isolation (venv, nvm/fnm/volta, WSL boundaries, repo config).
- **Layer 6:** prior-agent drift and phantom changes.

### 5) Classify evidence in every conclusion

Label findings as:

- **Observed**: direct command/file output.
- **Strong inference**: corroborated signals with no conflict.
- **Weak inference**: plausible but unverified.

Never present inference as fact.

Use confidence tags directly in findings:

- **Observed**
- **Strong inference**
- **Weak inference**
- **Unknown**

### 6) Produce constrained remediation

When user asks for fixes:

- Propose smallest safe diff first.
- Include rollback steps before execution steps.
- Explicitly list commands that mutate system state.
- Avoid duplicate-installer thrash; remove shadowing causes before reinstalling.

### 7) Verify and harden

After each change:

- Re-run failing command(s) in all affected contexts.
- Confirm selected interpreter/runtime/binary path is canonical.
- Emit residual risks and what was intentionally not changed.

Mandatory verification triad for environment-policy changes:

1. **Registry/user policy state** (key/value exists as expected),
2. **Fresh external shell** (new PowerShell/CMD process),
3. **Current long-lived app host** (editor/agent host session inheritance).

Do not mark a fix complete until all three states are checked or explicitly marked unknown.

If cleanup targets protected paths (for example under `Program Files`), branch early:

- classify as **requires elevation/ownership change** when non-admin,
- do not leave it mixed into ordinary low-risk cleanup.

If stabilized, generate a baseline using `references/BASELINE-ARTIFACT-TEMPLATE.md`.

## Use packaged references surgically

- Load `references/RED-FLAG-INDEX.md` for quick triage and stop-doing guidance.
- Load `references/PLAYBOOK.md` for full staged execution details.
- Load `references/BASELINE-ARTIFACT-TEMPLATE.md` at stabilization/handoff time.
- Load `references/NOTES.md` only for deployment and host-capability guidance.

## Output contract (always)

Respond in this exact high-level structure:

1. Situation Snapshot
2. Verified Facts
3. Likely Fragmentation Points
4. Root-Cause Ranking
5. Next Safe Actions
6. Remaining Unknowns
7. Definition of Done