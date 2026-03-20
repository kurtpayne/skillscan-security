---
name: things-todo
description: Generate a clickable Things 3 import link from tasks discussed in conversation. Use this skill whenever Claude produces a list of actions, tasks, to-dos, next steps, or a project plan that the user might want to track — even if they don't explicitly say "Things" or "todo list." Also trigger when the user says things like "ajoute ça dans Things", "fais-moi une todo", "crée les tâches", "envoie ça dans Things", "make a task list", "send to Things", "plan this out as tasks", or any variation. If a conversation ends with a clear set of actionable items, proactively offer to generate the Things link. Always use this skill instead of outputting a plain markdown checklist when the user could benefit from real task management.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: viktorvuka/claude-things-skill
# corpus-url: https://github.com/viktorvuka/claude-things-skill/blob/33749b5388f19a31430bd525974e9480f12b3460/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Things 3 Todo List Generator

Generate a clickable `things:///json` URL that imports tasks directly into Things 3 on macOS/iOS.

## When to use

- The user explicitly asks for tasks, a todo list, or to send something to Things
- Claude has produced a plan, a set of next steps, or action items
- A brainstorm, brief, or project discussion has landed on concrete actions
- Proactively offer the Things link whenever a conversation yields clear actionable outputs

## First-time setup

Before generating any tasks, Claude needs to know the user's Things 3 structure. If no configuration has been provided yet (check Claude's memory), ask the user to share:

1. **Areas** — their list of Things areas (ongoing life/work buckets). Ask: "What are your Areas in Things 3?"
2. **Active projects** — projects currently in progress. Ask: "What are your active projects?"
3. **Tags** — their tag list, including exact names with emojis if any. Ask: "What tags do you use? Include emojis if your tag names contain them — the names must match exactly."

Once provided, Claude should store this configuration in memory (via memory_user_edits) so it persists across conversations. The configuration should be stored as a concise structured summary.

If the user's Things structure changes, they can ask Claude to update it at any time ("update my Things tags", "j'ai un nouveau projet", etc.).

**If no configuration exists yet, Claude can still generate tasks** — it just won't use tags, areas, or target existing projects. It should mention this and suggest running the setup.

## Things 3 JSON URL Scheme

The URL format is:

```
things:///json?data=<URL-encoded JSON array>
```

The JSON payload is an **array** of objects. Each object has a `type` and an `attributes` dict.

### Object types

#### `to-do` (single task → goes to Inbox)

```json
{
  "type": "to-do",
  "attributes": {
    "title": "Task title",
    "notes": "Optional notes or context",
    "when": "2025-06-15",
    "deadline": "2025-06-20",
    "tags": ["tag1", "tag2"],
    "checklist-items": [
      {"type": "checklist-item", "attributes": {"title": "Subtask 1"}},
      {"type": "checklist-item", "attributes": {"title": "Subtask 2"}}
    ]
  }
}
```

#### `project` (group of tasks → creates a Things project)

```json
{
  "type": "project",
  "attributes": {
    "title": "Project name",
    "notes": "Project description",
    "when": "2025-06-15",
    "deadline": "2025-06-30",
    "tags": ["tag1"],
    "items": [
      {
        "type": "heading",
        "attributes": {
          "title": "Phase 1"
        }
      },
      {
        "type": "to-do",
        "attributes": {
          "title": "Task inside project",
          "notes": "Details",
          "tags": ["tag1"],
          "checklist-items": [
            {"type": "checklist-item", "attributes": {"title": "Subtask A"}}
          ]
        }
      },
      {
        "type": "heading",
        "attributes": {
          "title": "Phase 2"
        }
      },
      {
        "type": "to-do",
        "attributes": {
          "title": "Another task in next phase"
        }
      }
    ]
  }
}
```

**Important structural rules:**
- **Headings** are separate objects with `"type": "heading"` placed in the `items` array — they are NOT an attribute on a to-do.
- **Checklist items** must each have `"type": "checklist-item"` and an `"attributes"` dict with `"title"`.
- To-dos listed after a heading belong to that heading until the next heading.

### Attribute reference

| Attribute | Type | Notes |
|---|---|---|
| `title` | string | Required. Keep concise and actionable (start with a verb). |
| `notes` | string | Optional. Context, links, details. Supports Markdown. |
| `when` | string | Optional. Start date: `"2025-06-15"` or `"evening"` or `"someday"`. |
| `deadline` | string | Optional. Hard deadline: `"2025-06-20"`. |
| `tags` | array of strings | Optional. Tags must already exist in Things to appear. |
| `checklist-items` | array of objects | Optional. Each must have `"type": "checklist-item"` and `"attributes": {"title": "..."}`. |
| `list` | string | Optional. Name of an existing Things project to add the task to. |
| `area` | string | Optional. Name of an existing Things area to assign the project/task to. |
| `items` | array | Projects only. Contains `to-do` and `heading` objects. Headings are `{"type": "heading", "attributes": {"title": "..."}}`. |

### Date formats

- Specific date: `"2025-06-15"` (ISO format, YYYY-MM-DD)
- Today: `"today"`
- Evening: `"evening"`
- Someday: `"someday"`
- No date: omit the field entirely

## Tag usage guidelines

**Things 3 has tag inheritance.** Tags cascade down: area → project → task, and parent tag → child tag. Never add a tag that's already inherited from the parent context.

Rules:
- **Don't duplicate area/project tags on tasks.** If a task lives in a project inside an area that already carries a tag, don't add that tag again.
- **Don't duplicate parent tags.** If you assign a child tag, the parent tag is automatically inherited — don't add it.
- **Only add tags that provide NEW information** beyond what the task's context already carries.
- **When in doubt, fewer tags is better.** Let inheritance do the work.
- **Tag names must match exactly** — including emojis, capitalization, and spaces. Things ignores unknown tags silently.

## Productivity principles

When generating tasks, follow these principles (inspired by the FU-Master methodology for Things 3):

### Today vs Anytime vs Someday

- **Today** (`"when": "today"`) = only "Must Dos" — tasks that absolutely HAVE to happen today. Keep this list tight.
- **Anytime** (no `when`, no scheduling) = "Bonus Todos" for the week — tasks that can be tackled at any point. This is the default. Most tasks should land here.
- **Someday** (`"when": "someday"`) = not for this week — ideas, long-term items, things to revisit during weekly review.

**Default to Anytime.** Only use `"when": "today"` for genuine must-dos. Only use `"when": "someday"` for items explicitly not needed this week.

### Deadlines over scheduling

- **Prefer `"deadline"` over `"when"`** for dates. A deadline keeps the task visible in Anytime while ensuring it pops up in Today when due.
- Only use `"when"` (scheduling) when the task literally cannot be started before that date.
- Use `"deadline"` when there's a real due date, even if it's soft. This surfaces the task at the right time without hiding it from Anytime.

### Next actions only

- Every task must be **actionable** — start with a verb, be specific enough to act on immediately.
- Don't create sequences of dependent tasks. Only create the **next action** for each stream of work.
- If a task has prerequisites, put context in the `notes` field, not as separate blocked tasks.
- If there are many possible future steps, use the project `notes` field to list them — only the next actionable steps become to-dos.

## Decision logic: Project vs Inbox

Choose the structure based on context:

- **Use a `project`** when:
  - There are 4+ related tasks forming a coherent initiative
  - Tasks have natural phases or groupings (use `heading` objects in `items` for these)
  - The conversation is about a project, a launch, a brief, or a multi-step plan

- **Add to an existing project** (`"list"` attribute) when:
  - The conversation is clearly about one of the user's active projects
  - The user mentions a project by name

- **Use individual `to-do` items** (Inbox) when:
  - There are 1–3 unrelated or loosely related actions
  - Tasks are quick standalone items
  - The user asks for miscellaneous reminders or next steps

- **Use multiple projects** when the conversation spans clearly distinct initiatives

## Splitting large task lists

When the total number of tasks exceeds **15**, split into multiple links:

- Group logically (by phase, by project, by area) — never split arbitrarily
- Present each group with its own summary and its own clickable link
- Label each link clearly (e.g., "Phase 1 — Research (6 tasks)", "Phase 2 — Production (8 tasks)")
- If tasks belong to different areas/projects, that's a natural split boundary

## How to generate the output

1. **Structure the JSON** following the schema above
2. **URL-encode** the JSON string (full encoding — spaces, quotes, brackets, everything)
3. **Build the URL**: `things:///json?data=` + encoded JSON
4. **Present as a clickable Markdown link**:
   ```
   [Open in Things 3](things:///json?data=...)
   ```

### Critical rules

- **Always use compact JSON** (`separators=(',', ':')` — no spaces after `:` or `,`). This reduces URL length and avoids parsing issues.
- **Always URL-encode the entire JSON payload.** Unencoded JSON will break the link.
- **Start task titles with a verb** — "Send", "Review", "Draft", "Prepare", etc.
- **Keep titles short** (< 60 chars). Put details in `notes`.
- **Only include attributes that have real values** — don't add empty strings or null fields.
- **Use headings** in projects to group tasks by phase, priority, or category when there are 5+ tasks.
- **Match the language of the conversation** for task titles and notes.

### Delivery method

The `things:///` URL scheme doesn't work as a clickable link inside the Claude chat interface. **Always generate an HTML file** with the link(s) and present it to the user via `present_files`. The HTML file should:
- Have a clean, dark-themed UI
- Show the destination and task summary for each link
- Include the clickable link that opens Things when clicked in a browser (Safari)

## Output format

Always present the result as:

1. **Destination** — Always state clearly where the tasks will land:
   - "→ 3 tasks in **Inbox**"
   - "→ New project 'Website Redesign' in area **Work**"
   - "→ 4 tasks added to project **Q2 Launch**"
2. A quick overview listing the tasks (so the user can verify before clicking)
3. The clickable link delivered in an **HTML file** (see Delivery method)

**The destination line is mandatory.** The user must know where to find the tasks in Things before clicking.

## Example output

> **→ New project in Work** · 6 tasks in 2 phases
>
> **Phase 1 — Preparation**
> - Finalize the creative brief (deadline June 15)
> - Prepare visual assets
> - Draft the copy
>
> **Phase 2 — Launch**
> - Publish on LinkedIn
> - Send the newsletter
> - Schedule the Instagram post
>
> [Open in Things 3 →](things:///json?data=%5B%7B%22type%22%3A%22project%22%2C...)

> **→ 2 tasks in Inbox** · anytime and someday
>
> - Reply to Guillaume's email (anytime)
> - Order the Vignelli book (someday)
>
> [Open in Things 3 →](things:///json?data=%5B%7B%22type%22%3A%22to-do%22%2C...)