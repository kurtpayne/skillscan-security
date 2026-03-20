---
name: linear-issue
model: sonnet
description: Full Linear issue lifecycle. Use when the user wants to "create a Linear issue", "file a ticket", "read an issue", "show issue details", "update status", "close an issue", "mark done", "add a comment", "leave a handoff note", "check off items", "create a sub-issue", or any mention of tracking/managing work in Linear. Handles read, create, batch create, update, comment, checklist, sub-issue, and handoff workflows.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: kylesnav/linear-issue-skill
# corpus-url: https://github.com/kylesnav/linear-issue-skill/blob/f52db854472837e9443e6549d2df1d3e67a7ec44/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Linear Issue

Full lifecycle management for Linear issues. Read, create, update, comment, check off items, create sub-issues, and hand off between agents — all from one skill.

## Setup

Before first use in a session, load all Linear MCP tools:

```
ToolSearch: "+linear save_issue"
ToolSearch: "+linear get_issue"
ToolSearch: "+linear list_issues"
ToolSearch: "+linear create_comment"
ToolSearch: "+linear list_comments"
ToolSearch: "+linear list_issue_statuses"
ToolSearch: "+linear list_issue_labels"
ToolSearch: "+linear list_projects"
ToolSearch: "+linear list_teams"
```

Use `mcp__plugin_linear_linear__*` tools (not `mcp__claude_ai_Linear__*`).

## Intent Detection

Parse `$ARGUMENTS` to determine mode. **First match wins.**

| Signal | Mode | Example |
|---|---|---|
| Empty | **Ask** | `/linear-issue` |
| Identifier alone, or + "read"/"show"/"get" | **Read** | `/linear-issue PROJ-42` |
| Identifier + "status:"/"done"/"close"/"block" | **Update** | `/linear-issue PROJ-42 status:done` |
| Identifier + "comment"/"note"/"handoff" + text | **Comment** | `/linear-issue comment PROJ-43 "Watch for X"` |
| Identifier + "check"/"uncheck"/"checklist" | **Checklist** | `/linear-issue check PROJ-42 2` |
| "sub"/"child" + identifier + title | **Sub-issue** | `/linear-issue sub PROJ-42 Fix token skip` |
| "handoff" + identifier + "->" + identifier + text | **Compound Handoff** | `/linear-issue handoff PROJ-42 -> PROJ-43 "Watch for X"` |
| No identifier + descriptive text | **Create** | `/linear-issue Add health check endpoint` |
| Multiple items (list/commas) | **Batch Create** | `/linear-issue\n- Fix X\n- Add Y` |

Identifier with no verb defaults to **Read** (safe, non-destructive).

### When `$ARGUMENTS` is empty

Ask what they want to do. Don't guess.

## Defaults

| Field | Default | Override |
|---|---|---|
| Team | `auto-resolved` | User specifies, or auto-selected if only one team exists |
| Assignee | `me` (self-assign) | User says "unassigned" or names someone |
| Priority | None | Infer from context unless user specifies urgency |
| Project | None | Infer from context or ask if ambiguous |
| Labels | Infer from context | User specifies |

### Label inference

Apply labels when obvious from the input:

- **Bug** — "bug", "broken", "fix", "regression", "doesn't work"
- **Feature** — "add", "new", "implement", "create", "build"
- **Improvement** — "improve", "refactor", "optimize", "update", "enhance", "clean up"

If ambiguous, don't label. Labels are optional.

### Project inference

If the user mentions a repo name or project name, check `list_projects` and assign if there's a clear match. If no match or ambiguous, skip — don't ask unless the user seems to expect project assignment.

### Blocking issue creation during work

When working on an issue (not just creating one), if you get stuck:

- **Hit a bug** — Create a related issue with the **Bug** label, link it as blocking the current issue. Move the parent issue to **Blocked** status.
- **Need human input** — Create a related issue with the **User** or **Test** label, link it as blocking the current issue. Move the parent issue to **Blocked** status.

The **Blocked** status signals that an issue can't progress until its blockers are resolved. Move it back to In Progress once unblocked.

## Modes

### Read

Agent briefing format. Dense and structured, no prose.

1. Call `get_issue` with the identifier (request relations)
2. Call `list_comments` for the issue
3. Call `list_issues` with `parentId` to get sub-issues
4. Output:

```
## PROJ-42: Title
Status: In Progress | Priority: High | Labels: Feature, Scope
Project: my-project | Assignee: username
Created: 2026-02-28 | Updated: 2026-03-01

### Description
[description text]

### Checklist [2/5]
1. [x] Step one
2. [x] Step two
3. [ ] Step three
4. [ ] Step four
5. [ ] Step five

### Sub-issues
- PROJ-43: Fix token skip (Done)
- PROJ-44: Add visual assertions (In Progress)

### Comments (3)
[most recent first, with author and date]

### Relations
- Blocks: PROJ-50
- Blocked by: PROJ-39
```

Omit empty sections. Checklist section only appears if description contains `- [ ]` or `- [x]` items.

### Create

Single-issue fast path. No confirmation needed.

1. **Parse `$ARGUMENTS`** — Extract title and any description content
2. **Resolve team** —
   1. If user specifies a team name → match via `list_teams`
   2. Call `list_teams`
   3. If exactly one team exists → use it automatically
   4. If multiple teams → ask the user which team
3. **Create the issue** — Call `save_issue` with:
   - `title`: Short, imperative. "Add health check endpoint" not "We should add a health check endpoint"
   - `description`: Brief description (see Description Style below), followed by the standard checklist:
     ```
     - [ ] Plan (use plan mode for non-trivial work)
     - [ ] Implement
     - [ ] `/simplify`
     - [ ] `/review` + tests
     - [ ] File new issues for any bugs or unexpected scope creep discovered
     - [ ] Close this ticket when done
     - [ ] Leave a handoff note on the next ticket
     ```
   - `teamId`: Resolved team ID
   - `assigneeId`: `me`
   - `priority`: `3` unless user indicates urgency
   - `labelIds`: From inference (if any)
   - `projectId`: From inference (if any)
4. **Report back** — Show the issue identifier and URL. One line, no fanfare.

### Batch Create

Triggered when the user describes multiple issues (numbered list, comma-separated, or paragraph with multiple distinct tasks).

1. **Parse all issues** from the input
2. **Present a summary table** before creating:

```
I'll create the following issues:

| # | Title | Labels | Project |
|---|---|---|---|
| 1 | Add health check endpoint | Feature | my-api |
| 2 | Fix temperature unit conversion | Bug | my-api |
| 3 | Refactor data fetching layer | Improvement | — |

Dependencies:
- #3 blocked by #2

Create all? (y/n)
```

3. **Wait for approval** — Use AskUserQuestion
4. **Create in dependency order** — Blockers first so you have their IDs for `blockedBy` fields
5. **Report all identifiers** — List all created issues with identifiers and URLs

### Update

Read-before-write. Always fetch the issue first to confirm it exists and show the transition.

1. **Resolve identifier** — Call `get_issue`
2. **Parse changes** — Status shorthand, priority, labels, assignee, etc.
3. **Call `save_issue`** with changed fields only
4. **Report transition** — e.g., `PROJ-42: In Progress → Done`

#### Status shorthand

| Shorthand | Linear State |
|---|---|
| `todo` | Todo |
| `progress` / `wip` / `start` | In Progress |
| `done` / `close` / `complete` | Done |
| `blocked` / `block` | Blocked |
| `backlog` | Backlog |
| `canceled` / `cancel` | Canceled |

If unsure about available statuses, call `list_issue_statuses` to confirm valid states for the team.

### Comment

1. **Resolve identifier** — Call `get_issue` to confirm it exists
2. **Call `create_comment`** with the comment body
3. If the keyword `handoff` appears in the arguments, prefix the comment body with `**Handoff Note**\n\n` for visual distinction in Linear
4. **Report** — `Comment added to PROJ-43.`

### Checklist

Read-modify-write on the issue description field.

- `checklist PROJ-42` → Display items with 1-indexed numbers
- `check PROJ-42 2` → Mark item 2 done (`- [ ]` → `- [x]`)
- `uncheck PROJ-42 2` → Mark item 2 not done (`- [x]` → `- [ ]`)
- `check PROJ-42 all` → Mark all items done

Steps:
1. Call `get_issue` to get current description
2. Parse `- [ ]` and `- [x]` items from description
3. For display: show numbered list with status
4. For mutation: modify the target item(s), call `save_issue` with updated description
5. **Report** — `PROJ-42: Checked item 2 — "Write visual assertions"`

### Sub-issue

1. **Resolve parent** — Call `get_issue` on the parent identifier
2. **Create child** — Call `save_issue` with:
   - `parentId`: Parent issue's ID
   - `teamId`: Inherited from parent
   - `projectId`: Inherited from parent
   - `title`: From arguments
   - `assigneeId`: `me`
3. **Report** — `Created PROJ-55: Fix token skip (child of PROJ-42)`

### Compound Handoff

Convenience syntax: `handoff PROJ-42 -> PROJ-43 "message"`

1. **Update PROJ-42** — Set status to Done via `save_issue`
2. **Comment on PROJ-43** — Call `create_comment` with body prefixed: `**Handoff from PROJ-42**\n\n[message]`
3. **Report** — `PROJ-42 → Done. Handoff note added to PROJ-43.`

## Description Style

Two modes. Default to **brief** unless the user asks for more detail or the issue is clearly implementation-heavy.

### Brief (default)

One to three sentences. Context (why), then what needs to happen, then key details if any.

> The API has no way to verify it's running. Add a `GET /health` endpoint that returns `200 OK` with uptime and version info.

### Structured (on request or for implementation work)

Use when the user says "detailed", "PRD-style", or when the issue involves multiple steps:

```markdown
## Current State
What exists today and why it's insufficient.

## Goal
What success looks like.

## Steps
1. Concrete step
2. Concrete step

## Decision Points
- Open questions that need answers during implementation

## Verification
How to confirm the work is correct.

## Key Constraints
Non-obvious limitations, compatibility requirements, etc.
```

Omit sections that don't apply. An empty section is worse than no section.

## Codebase Context

**Opt-in, not automatic.** Don't explore the codebase unless:

- You're already in a repo and the issue is about that code
- The user explicitly asks you to reference code in the issue
- The issue is a **review or audit** — when the user says "review", "audit", "check", or "make sure", explore relevant repos/files to write an informed issue with specific findings

When including codebase context:
- Reference specific files and line numbers
- Mention relevant patterns or conventions
- Keep it brief — a file path and one-line note, not a code review
- For review issues: call out specific findings

## Cross-Referencing Related Issues

When creating or updating an issue that overlaps with or depends on an existing issue:

- **Deduplicate** — If the new issue absorbs a step from an existing one, update the existing issue to remove that step and reference the new one (e.g., "Handled via PROJ-3")
- **Reference by identifier** — Use Linear identifiers (e.g., PROJ-3) in descriptions, not raw IDs
- **Clarify boundaries** — State explicitly what each issue owns vs. what's handled elsewhere

## Working an Issue

1. Read the ticket — `/linear-issue PROJ-XX`
2. Plan before coding for non-trivial work
3. Execute; stay in scope
4. `/simplify` — review changed code for reuse and quality
5. `/review` and tests — verify acceptance criteria
6. Check off the checklist — `/linear-issue check PROJ-XX all`
7. Close — `/linear-issue PROJ-XX status:done`
8. Handoff — `/linear-issue comment PROJ-NEXT "Handoff: <context>"`
9. File any bugs, scope creep, or test gaps as new issues

**When blocked:** Create a blocking issue, link it, set this issue to Blocked.
**Test failures:** Fix inline if small and in scope; file a bug ticket otherwise.

## Error Handling

| Error | Response |
|---|---|
| Issue not found | "PROJ-999 not found. Check the identifier." |
| No checklist in description | "PROJ-42 has no checklist items." |
| Invalid status shorthand | Show valid statuses from `list_issue_statuses` |
| Ambiguous identifier | Show matches, ask to specify |

## Examples

### Read an issue
```
/linear-issue PROJ-42
```
→ Shows full agent briefing: status, description, checklist progress, sub-issues, comments, relations.

### Create a single issue
```
/linear-issue Add health check endpoint to my-api API
```
→ Creates one issue titled "Add health check endpoint" in auto-detected team, assigned to me, labeled Feature, project my-api.

### Batch create
```
/linear-issue
- Add retry logic to NOAA API calls
- Fix incorrect probability clamping at boundaries
- Add CLI flag for custom date ranges
```
→ Shows summary table, waits for approval, creates all three.

### Update status
```
/linear-issue PROJ-42 status:done
```
→ `PROJ-42: In Progress → Done`

### Add a comment
```
/linear-issue comment PROJ-43 "Token sync works but palette order changed — next agent should verify"
```
→ `Comment added to PROJ-43.`

### Handoff note
```
/linear-issue handoff PROJ-43 "Toggle tokens validated, visual tests still need assertions"
```
→ Comment added with **Handoff Note** prefix.

### Check off a checklist item
```
/linear-issue check PROJ-42 2
```
→ `PROJ-42: Checked item 2 — "Write visual assertions"`

### Create a sub-issue
```
/linear-issue sub PROJ-42 Fix token skip in toggle component
```
→ `Created PROJ-55: Fix token skip in toggle component (child of PROJ-42)`

### Compound handoff
```
/linear-issue handoff PROJ-42 -> PROJ-43 "All token work complete, visual tests next"
```
→ `PROJ-42 → Done. Handoff note added to PROJ-43.`

### Bare invocation
```
/linear-issue
```
→ Asks what the user wants to do.