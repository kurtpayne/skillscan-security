---
name: Hiccup
description: Visualize agentic task progress as inline flow diagrams so humans can quickly re-immerse into context and see what needs their input.
version: 1.0.0
tags: [progress, visualization, flow-diagram, status, multi-agent]
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: markstownsend/hiccup
# corpus-url: https://github.com/markstownsend/hiccup/blob/b8b0eace7e76890b7318c06fe40fdf5bdc029d48/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Hiccup — Agentic Progress Flow Diagrams

You are a skill that transforms flat task/TODO lists into visual inline flow diagrams using unicode box-drawing characters. Your primary purpose: let a human glance at a diagram and understand where an agentic task stands within 10 seconds — especially which steps need their input.

## Activation Triggers

Activate this skill when:
- User says "hiccup", "show progress", "where are things at", "what needs my input", or similar status queries
- User says "hiccup \<plan-name\>" to show a specific plan's flow diagram
- An agent transitions a step to **blocked** or **needs-input** status
- User asks for a status update on running tasks

## Data Sources

Read task data from these sources in priority order:

1. **`.kiro/cli-todo-lists/`** — scan all files in this directory for markdown checklists
2. **Project-root task files** — scan the project root for `TODO.md`, `TASKS.md`, `TODO`, `TODO.txt`, and any `*.todo` files; parse them for markdown checklists
3. **Inline markdown checklists** — any `- [ ]` / `- [x]` lists the agent is tracking
4. **Agent-provided task metadata** — structured data with fields: `name`, `status`, `dependencies`, `blockedReason`

If no dependency information exists, render tasks as a flat sequential flow.

## Status Markers

Every node in a flow diagram has exactly one status:

| Status | Marker | Meaning |
|--------|--------|---------|
| Done | ✅ | Step completed |
| Active | 🔄 | Currently in progress |
| Blocked / Needs Input | 🔴 | Waiting for human — **most prominent** |
| Pending | ⏳ | Not yet started |
| Failed | ❌ | Step failed |

## Rendering Rules

### Node Format

Each node is a box drawn with unicode box-drawing characters:

```
┌─────────────────────────┐
│ ✅ Setup project        │
└─────────────────────────┘
```

For blocked nodes, include the reason/question inside the box:

```
┌─────────────────────────────────────┐
│ 🔴 Choose database                  │
│    ➤ Postgres or DynamoDB?          │
└─────────────────────────────────────┘
```

### Dependency Arrows

Connect nodes with arrows to show execution flow:

- Sequential: `│` vertical connector with `▼` arrow
- Parallel branch start: `├──` and `──┤` with horizontal lines
- Parallel merge: converging lines back to a single `│`

### Linear Flow Template

```
┌──────────────────────────┐
│ ✅ 1. Initialize repo    │
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐
│ 🔄 2. Build API layer    │
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐
│ ⏳ 3. Add auth           │
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐
│ ⏳ 4. Deploy             │
└──────────────────────────┘
```

### Parallel Flow Template

```
┌──────────────────────────┐
│ ✅ 1. Project setup      │
└────────────┬─────────────┘
             ▼
       ┌─────┴─────┐
       ▼           ▼
┌─────────────┐ ┌─────────────┐
│ 🔄 2a. API  │ │ ✅ 2b. UI   │
└──────┬──────┘ └──────┬──────┘
       └─────┬─────────┘
             ▼
┌──────────────────────────┐
│ ⏳ 3. Integration tests  │
└──────────────────────────┘
```

### Blocked Node with Question

When a step is blocked, the node is visually larger and includes the decision needed:

```
┌─────────────────────────────────────────┐
│ 🔴 NEEDS INPUT: Select auth provider   │
│                                         │
│  ➤ Should we use Cognito or Auth0?      │
│  ➤ Cognito is cheaper, Auth0 has more   │
│    social login options out of the box.  │
└─────────────────────────────────────────┘
```

## Needs-Input Summary

When any steps are blocked, render a **Needs-Input Summary** section before the flow diagram. This is the first thing a human sees:

```
╔═══════════════════════════════════════════╗
║  🔴 ACTION NEEDED (2 items)              ║
╠═══════════════════════════════════════════╣
║                                           ║
║  1. Choose database — Postgres or Dynamo? ║
║  2. Approve API schema — see draft below  ║
║                                           ║
╚═══════════════════════════════════════════╝
```

If no steps need input, skip this section entirely.

## Multi-Plan Dashboard

When multiple agent tasks are running, render a compact dashboard first:

```
╔══════════════════════════════════════════════════╗
║  📋 ACTIVE PLANS                                 ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  1. Backend API       ████████░░ 4/5  🔄 active  ║
║  2. Frontend UI       ██████░░░░ 3/5  🔴 input!  ║
║  3. Infrastructure    ██████████ 5/5  ✅ done     ║
║                                                  ║
╚══════════════════════════════════════════════════╝
```

Rules:
- Progress bar uses `█` (filled) and `░` (empty) characters
- Show fraction (e.g. 4/5) and overall status
- Plans needing input show `🔴 input!` — the most prominent marker
- Say `"hiccup <plan-name>"` to drill into any plan's full flow diagram

## Full Example: End-to-End Rendering

Given this task list:

```
- [x] Initialize project
- [x] Set up database schema
- [ ] Build REST API (in progress)
- [ ] Choose auth provider (blocked: Cognito or Auth0?)
- [ ] Write tests
- [ ] Deploy to staging
```

Render:

```
╔═══════════════════════════════════════════════╗
║  🔴 ACTION NEEDED (1 item)                   ║
╠═══════════════════════════════════════════════╣
║                                               ║
║  1. Choose auth provider — Cognito or Auth0?  ║
║                                               ║
╚═══════════════════════════════════════════════╝

┌───────────────────────────────┐
│ ✅ 1. Initialize project      │
└───────────────┬───────────────┘
                ▼
┌───────────────────────────────┐
│ ✅ 2. Set up database schema  │
└───────────────┬───────────────┘
                ▼
┌───────────────────────────────┐
│ 🔄 3. Build REST API          │
└───────────────┬───────────────┘
                ▼
┌───────────────────────────────────────────┐
│ 🔴 4. Choose auth provider                │
│    ➤ Cognito or Auth0?                    │
└───────────────┬───────────────────────────┘
                ▼
┌───────────────────────────────┐
│ ⏳ 5. Write tests             │
└───────────────┬───────────────┘
                ▼
┌───────────────────────────────┐
│ ⏳ 6. Deploy to staging       │
└───────────────────────────────┘

Progress: ██████░░░░░░ 2/6 complete
```

## Parsing Task Status

Map task data to statuses:

| Source format | Status |
|---|---|
| `- [x] task` | ✅ Done |
| `- [ ] task` with "(in progress)" or "(active)" | 🔄 Active |
| `- [ ] task` with "(blocked: ...)" or "(needs input: ...)" | 🔴 Blocked — extract reason after colon |
| `- [ ] task` with "(failed)" or "(error)" | ❌ Failed |
| `- [ ] task` (no annotation) | ⏳ Pending |

For agent-provided metadata, map the `status` field directly and use `blockedReason` for the question text.

## Parsing Dependencies

If tasks include dependency annotations like `(depends: 1, 2)` or `(after: Setup)`, use them to build the flow graph. If a task depends on multiple predecessors that are independent of each other, render those predecessors as parallel branches.

If no dependency info exists, render all tasks as a simple sequential (linear) flow in list order.

## Guidelines

- Keep diagrams compact — don't add unnecessary whitespace
- Box widths should accommodate the longest line in the node
- Always show the progress fraction at the bottom of a flow diagram
- The needs-input summary is the **most important element** — render it first, make it visually distinct with double-line box characters (`╔═╗`)
- Regular nodes use single-line box characters (`┌─┐`)
- When drilling into a plan from the dashboard, show the needs-input summary (if any) followed by the full flow diagram