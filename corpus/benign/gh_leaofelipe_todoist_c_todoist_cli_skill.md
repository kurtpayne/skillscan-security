---
name: todoist-cli-skill
version: 1.0.5
description: Manage tasks and projects in Todoist using the Official Todoist CLI tool (https://github.com/Doist/todoist-cli). Use when user asks about tasks, to-dos, reminders, productivity, or when the todoist-official skill is explicitly requested. Supports tasks, projects, labels, sections, reminders, comments, activity logs, stats, and workspaces.
homepage: https://github.com/leaofelipe/todoist-cli-skill
metadata:
  clawdbot:
    emoji: "✅"
    requires:
      bins: ["td"]
      env: ["TODOIST_API_TOKEN"]
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: leaofelipe/todoist-cli-skill
# corpus-url: https://github.com/leaofelipe/todoist-cli-skill/blob/899d34c8d5419022973f18ece25859cf5572787d/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Todoist CLI (`td`)

Uses the [Official Todoist CLI tool](https://github.com/Doist/todoist-cli) for task management.

> **AI/LLM note (from the CLI itself):** Use `td task add` (not `td add`) for structured task creation. Use `--json` or `--ndjson` for parseable output.

## Installation

```bash
npm install -g @doist/todoist-cli
```

## Setup

Get your API token at: https://todoist.com/app/settings/integrations/developer

```bash
td auth token "your-token"
# or
export TODOIST_API_TOKEN="your-token"
```

## Viewing Tasks

```bash
td today                          # Today + overdue
td upcoming                       # Next 7 days
td upcoming 14                    # Next N days
td inbox                          # Inbox tasks
td completed                      # Completed today
td completed --since 2026-01-01   # Completed since date
```

## Adding Tasks

Prefer `td task add` with structured flags for reliability:

```bash
td task add "Review PR" --due "today" --priority p1 --project "Work"
td task add "Call mom" --due "sunday" --labels "family"
td task add "Prep slides" --project "Work" --section "Q1" --order 0  # 0 = top
td task add "Subtask" --parent <ref>
td task add "Meeting" --due "tomorrow 10am" --duration 1h
```

Quick add (natural language, for humans — avoid in automation):

```bash
td add "Buy milk tomorrow p1 #Shopping @errands"
```

## Listing & Viewing Tasks

```bash
td task list                          # All tasks
td task list --project "Work"         # By project
td task list --priority p1            # By priority
td task list --label "urgent"         # By label
td task list --due today              # Due today
td task list --filter "p1 & today"    # Raw Todoist filter query
td task list --json                   # JSON output
td task view <ref>                    # Task details
td view <todoist-url>                 # View any entity by URL
```

## Managing Tasks

```bash
td task complete <ref>                # Complete task
td task complete <ref> --forever      # Complete recurring task permanently
td task uncomplete id:<id>            # Reopen task (requires id:xxx)
td task update <ref> --due "next week" --priority p2
td task update <ref> --content "New title"
td task update <ref> --labels "a,b"   # Replaces existing labels
td task move <ref> --project "Personal"
td task reschedule <ref> "next monday" # Preserves recurrence
td task delete <ref>
```

## Projects

```bash
td project list
td project create --name "New Project"
td project view <ref>
td project update <ref> --name "Renamed"
td project archive <ref>
td project delete <ref>               # Must have no uncompleted tasks
```

## Sections

```bash
td section list <project>
td section create --project "Work" --name "Q2"
td section update <id> --name "Renamed"
td section delete <id>
```

## Labels

```bash
td label list
td label create --name "urgent"
td label update <ref> --name "renamed"
td label delete <name>
td label view <ref>                   # View label + its tasks
```

## Comments

```bash
td comment list <task-ref>
td comment add <task-ref> "Note about this task"
td comment add <task-ref> --project   # Comment on project instead
td comment update <id> "Updated text"
td comment delete <id>
```

## Reminders

```bash
td reminder list <task-ref>
td reminder add <task-ref> --due "tomorrow 9am"
td reminder update <id> --due "friday 10am"
td reminder delete <id>
```

## Activity & Stats

```bash
td activity                           # Recent activity log
td activity --type task --event completed --since 2026-03-01
td stats                              # Karma + productivity stats
```

## Usage Examples

**User: "What do I have today?"**
```bash
td today
```

**User: "Add 'buy milk' to my tasks"**
```bash
td task add "Buy milk" --due "today"
```

**User: "Remind me to call the dentist tomorrow"**
```bash
td task add "Call the dentist" --due "tomorrow"
```

**User: "Mark the grocery task as done"**
```bash
td task list --filter "search: grocery" --json   # Find ref
td task complete <ref>
```

**User: "What's on my work project?"**
```bash
td task list --project "Work"
```

**User: "Show my high priority tasks"**
```bash
td task list --priority p1
```

**User: "What did I complete this week?"**
```bash
td completed --since 2026-03-10
```

## Notes

- `<ref>` can be a task name (fuzzy match), URL, or `id:xxx`
- `--order 0` = top of list (differs from mjrussell's `--order top`)
- Priority: p1 = highest, p4 = lowest
- Due dates support natural language ("tomorrow", "next monday", "jan 15")
- `--json` / `--ndjson` recommended for any programmatic parsing
- `--full` adds all fields to JSON output
- `--accessible` / `TD_ACCESSIBLE=1` adds text labels to color-coded output (useful in non-TTY contexts)