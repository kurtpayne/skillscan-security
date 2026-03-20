---
name: admiralty
description: Draft structured sailing orders for a Nelson mission from a task description.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: sandeepkv93/admiralty
# corpus-url: https://github.com/sandeepkv93/admiralty/blob/c2f50dff390fc1a67a1e112c7b07888f67e02b5c/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Admiralty

Analyse a raw task description and produce complete, copy-paste-ready sailing orders and a battle plan for downstream execution workflows (including Nelson).

## Phase 1: Reconnoitre

Extract intelligence from the user's task description.

Mandatory repository survey before planning:

- Before drafting orders, inspect the entire target codebase to understand the current state (project layout, key modules, existing workflows, tests, and active git status).
- Do not rely only on the prompt description when code exists; ground the plan in observed repository reality.
- Summarize the current state in recon notes and reference that summary in assumptions/scope.
- If the target codebase is ambiguous (multiple repos), identify candidates and ask the user to confirm the repo before continuing.

Minimum recon evidence to capture:

- Repository root path and active branch.
- `git status --short` summary and whether the worktree is dirty.
- Top-level project layout and primary entrypoints.
- Build/test/lint commands discovered from repo files.
- Dependency/runtime manifests discovered (for example: `go.mod`, `package.json`, `pyproject.toml`, `Cargo.toml`, CI workflows).
- Existing regression boundaries (critical behavior that must not change).

- **Core intent**: State the task's purpose in one sentence.
- **Key entities**: List systems, files, APIs, services, and domains involved.
- **Stated constraints**: Note any explicit requirements, deadlines, or limitations the user mentioned.
- **Implicit constraints**: Infer constraints from context (e.g. language, framework, environment).
- **Gaps**: Identify missing information needed to write complete orders.

Gap handling:

- If more than 2 critical gaps exist: ask up to 3 targeted questions. Each question must include a sensible default so the user can accept quickly.
- If 0-2 gaps exist: fill with conservative defaults from `references/assessment-rubrics.md` section "Common Defaults" and note assumptions in the output.
- If recon evidence is incomplete for a code task, do not finalize orders; ask focused questions or continue reconnaissance.

## Phase 2: Assess

Classify the task along three dimensions using `references/assessment-rubrics.md`.

### Complexity

| Level  | Criteria |
|--------|----------|
| Small  | Single concern, fewer than 3 files, one deliverable |
| Medium | 2-4 concerns, 5-15 files, multiple deliverables |
| Large  | 5+ concerns, 15+ files, architectural impact |

### Threat Tier

Map to Nelson's action stations (Station 0-3). Use the signal-words table and decision tree in the rubrics file. Round UP when uncertain.

### Execution Mode

Select one:

| Mode | When |
|------|------|
| `single-session` | Sequential work, tightly coupled, mostly same files |
| `subagents` | Parallel tasks that only report to admiral |
| `agent-team` | Parallel tasks with cross-task coordination needed |

### Team Sizing

- Small: 1 admiral + 2-3 captains
- Medium: 1 admiral + 4-5 captains
- Large: 1 admiral + 6-7 captains
- Add 1 red-cell navigator at Station 2+

## Phase 3: Draft Orders

Generate two artifacts using the exact template formats below.

### Sailing Orders

```text
Sailing orders:
- Outcome: <one sentence>
- Success metric: <measurable criterion>
- Deadline: <timeframe>

Constraints:
- Token/time budget: <budget>
- Reliability floor: <threshold>
- Compliance/safety constraints: <constraints>
- Forbidden actions: <actions>

Scope:
- In scope: <items>
- Out of scope: <items>

Stop criteria:
- Stop when: <conditions>

Required handoff artifacts:
- Must produce: <artifacts>
```

### Battle Plan

One block per task:

```text
Task ID: <T-n>
- Name: <short name>
- Owner: <captain-n | admiral>
- Deliverable: <concrete output>
- Dependencies: <T-n list or "none">
- Threat tier (0-3): <tier>
- File ownership (if code): <file paths>
- Primary risk: <top failure mode>
- Mitigation: <how risk is controlled>
- Validation required: <evidence needed>
- Rollback note required: yes/no
```

## Pre-Signal Sanity Checks

Before signaling final orders, verify:

- All referenced files/paths are consistent with repository reconnaissance.
- Every task has exactly one owner and explicit dependencies.
- No circular or impossible dependency chain in task ordering.
- Success metric and stop criteria are measurable.
- Validation evidence is defined for every task.
- For Station 1+, include explicit regression checks for critical existing behavior.

## Phase 4: Signal

Present the final output in a single fenced block using this exact envelope:

```text
===== ADMIRALTY SAILING ORDERS =====

Assessment:
- Complexity: <Small | Medium | Large>
- Threat Tier: Station <0-3>
- Execution Mode: <single-session | subagents | agent-team>
- Team: 1 admiral + <n> captains [+ 1 red-cell navigator]
- Confidence: <High | Medium | Low>
- Unknowns: <critical unknowns or "none">
- Assumptions: <list any defaults applied>
- Recon evidence: <repo, branch, status, key manifests/commands>

Sailing orders:
- Outcome: ...
- Success metric: ...
- Deadline: ...

Constraints:
- Token/time budget: ...
- Reliability floor: ...
- Compliance/safety constraints: ...
- Forbidden actions: ...

Scope:
- In scope: ...
- Out of scope: ...

Stop criteria:
- Stop when: ...

Required handoff artifacts:
- Must produce: ...

Battle Plan:

Task ID: T-1
- Name: ...
- Owner: ...
- Deliverable: ...
- Dependencies: ...
- Threat tier (0-3): ...
- File ownership (if code): ...
- Primary risk: ...
- Mitigation: ...
- Validation required: ...
- Rollback note required: ...

[Additional tasks as T-2, T-3, ...]

===== END ORDERS =====
```

## Admiralty Doctrine

- Round threat tier UP when uncertain.
- Prefer fewer tasks with clear ownership over many granular tasks.
- Always state out-of-scope explicitly to prevent scope creep.
- If the task is simple enough to not need Nelson (single-file fix, trivial change), say so and skip order generation.
- Conservative defaults over excessive questions. Only ask when gaps are truly critical.