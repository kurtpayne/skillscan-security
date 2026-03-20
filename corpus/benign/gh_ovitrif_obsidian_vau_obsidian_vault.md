---
name: obsidian-vault
description: >-
  This skill should be used when the user mentions "vault", "obsidian",
  "my notes", "daily note", or references files by Obsidian-style paths
  (e.g. Reviews/Roadmap/review_2_ovi). Also use when the user asks to
  "search my notes", "check my tasks", "update checkboxes", "find in vault",
  or references any .md file that could be in ~/vault.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: ovitrif/obsidian-vault-skill
# corpus-url: https://github.com/ovitrif/obsidian-vault-skill/blob/21af3966d22705f55c7ed57369e7ecb76cd264c5/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Obsidian Vault

The user's Obsidian vault is at `~/vault`. The CLI binary is `obsidian` (in PATH). **Prerequisite:** Obsidian.app must be running for the CLI to work.

## Path Resolution

The CLI has two targeting modes. Choosing the right one avoids failed lookups:

| User says | Looks like | Use | Example |
|---|---|---|---|
| Just a name | `review_2_ovi` | `file=` | `obsidian read file="review_2_ovi"` |
| Folder path | `Reviews/Roadmap/review_2_ovi` | `path=` (append `.md`) | `obsidian read path="Reviews/Roadmap/review_2_ovi.md"` |
| Wikilink | `[[review_2_ovi]]` | Strip brackets, use `file=` | `obsidian read file="review_2_ovi"` |
| Uncertain | Could be either | Resolve first | `obsidian file file="<name>"` |

Rules:
- `file=<name>` resolves by note name (like wikilinks) — no `.md` extension needed
- `path=<path>` requires exact vault-relative path **with** `.md`
- When user gives an Obsidian-style path like `Reviews/Roadmap/review_2_ovi`, append `.md` and use `path=`
- When user gives just a name like `review_2_ovi`, use `file=`
- When unsure, run `obsidian file file="<name>"` first to resolve the path

## Efficient Workflow Patterns

Minimize CLI calls and token usage by choosing the right tier:

### Tier 1 — Single CLI call (preferred)
Direct read, search, or outline. Use when the answer comes from one command.
```
obsidian read file="note_name"
obsidian search query="keyword"
obsidian outline file="note_name"
obsidian tasks file="note_name" verbose
```

### Tier 2 — CLI resolve + Claude native tools (2 calls)
Use CLI to find the path, then Claude's Read/Edit tools for manipulation. Better for large edits.
```
obsidian file file="note_name"     → gets vault-relative path
Read ~/vault/<resolved-path>       → read with Claude's native tool
Edit ~/vault/<resolved-path>       → edit with Claude's native tool
```

### Tier 3 — Search then act (multiple calls)
Search to discover files, then act on results.
```
obsidian search query="keyword"    → find matching files
obsidian read file="match1"        → read each relevant result
```

**Rule:** prefer `obsidian outline` before reading large files — it shows the heading structure so you can decide what sections to read.

## Core Operations Quick Reference

### Reading
```bash
obsidian read file="note_name"                    # Read by name
obsidian read path="folder/note.md"               # Read by path
obsidian outline file="note_name"                  # Heading structure first
```

### Searching
```bash
obsidian search query="keyword"                    # Basic search
obsidian search query="keyword" path="Reviews"     # Scoped to folder
obsidian search:context query="keyword"            # With line context
obsidian search query="keyword" total              # Match count only
obsidian tags counts sort=count                    # Most-used tags
obsidian tag name="project" verbose                # Files with tag
```

### Task Management
```bash
obsidian tasks file="note_name" verbose            # List with line numbers
obsidian tasks todo                                # All incomplete tasks
obsidian tasks daily                               # Today's tasks
obsidian task file="note_name" line=<n> done        # Complete a task
obsidian task file="note_name" line=<n> toggle      # Toggle a task
```

### Writing & Modifying
```bash
obsidian append file="note_name" content="text"    # Append to file
obsidian prepend file="note_name" content="text"   # Prepend to file
obsidian create name="New Note" content="text"     # Create new file
obsidian create path="folder/note.md" content="x"  # Create at path
```

### Properties
```bash
obsidian properties file="note_name"               # List file properties
obsidian property:read name="status" file="note"   # Read property
obsidian property:set name="status" value="done" file="note"  # Set property
obsidian property:remove name="old_prop" file="note"  # Remove property
```

### Links & Graph
```bash
obsidian links file="note_name"                    # Outgoing links
obsidian backlinks file="note_name"                # Incoming links
obsidian orphans                                   # No incoming links
obsidian deadends                                  # No outgoing links
obsidian unresolved                                # Broken links
```

### File Management
```bash
obsidian files folder="Reviews"                    # List files in folder
obsidian folders                                   # List all folders
obsidian move file="note_name" to="Archive"        # Move file
obsidian rename file="note_name" name="new_name"   # Rename file
obsidian delete file="note_name"                   # Delete (to trash)
```

## Task / Checkbox Workflow

This is a primary use case. The workflow depends on how many tasks need updating:

### Viewing tasks
```bash
obsidian tasks file="note_name" verbose    # Lists tasks with line numbers
obsidian tasks todo                        # All incomplete tasks in vault
obsidian tasks daily                       # Tasks from today's daily note
```

### Updating single tasks (1-3 tasks)
Use the CLI directly:
```bash
obsidian task file="note_name" line=<n> done       # Mark complete
obsidian task file="note_name" line=<n> todo       # Mark incomplete
obsidian task file="note_name" line=<n> toggle     # Toggle status
obsidian task file="note_name" line=<n> status="/" # Custom status char
```

### Bulk updates (>3 tasks)
Use Claude's native Edit tool instead of N CLI calls:
1. `obsidian file file="note_name"` → get path
2. Read `~/vault/<path>` with Claude's Read tool
3. Edit `~/vault/<path>` with Claude's Edit tool to update all checkboxes at once

### Adding tasks
```bash
obsidian append file="note_name" content="- [ ] New task"
obsidian daily:append content="- [ ] Task for today"
```

## Daily Notes

Format: `YYYY-MM-DD.md` at vault root. Weekly notes: `<week>_weekly.md` (e.g. `26_weekly.md`).

```bash
obsidian daily:read                                # Read today's note
obsidian daily:append content="- [ ] New task"     # Add to today
obsidian daily:prepend content="## Morning"        # Prepend to today
obsidian daily:path                                # Get today's note path
obsidian read file="2026-02-22"                    # Read specific date
obsidian read file="26_weekly"                     # Read weekly note
```

## Vault Structure

Key folders and their purposes:

| Folder | Purpose |
|---|---|
| `Reviews/` | Review documents, roadmaps, analysis |
| `Plans/` | Project plans, strategies |
| `Tasks/` | Task lists, kanban-style tracking |
| `Intel/` | Research, intelligence gathering, references |
| `Business/` | Business-related documents |
| `Meetings/` | Meeting notes |
| `Updates/` | Status updates, changelogs |
| `Inbox/` | Quick capture, unsorted notes |
| `_Archive/` | Archived/inactive content |
| `_Templates/` | Note templates |
| `_Assets/` | Attachments, images |
| `_Styles/` | CSS snippets |
| `_Web/` | Web clippings |

Root-level files include daily notes (`YYYY-MM-DD.md`), weekly notes (`NN_weekly.md`), `Board.md`, `Backlog.md`, and `scratch.md`.

## Additional Resources

For the full 100+ command reference with all options, see `references/cli-reference.md` in this skill directory.