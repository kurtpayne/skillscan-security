---
name: session-recall
description: "Search past session transcripts to recover lost conversation context. MUST use when: (1) the current session is new or has very few messages AND the user's message assumes shared context you don't have (they reference people, events, decisions, or topics not present in your current context), (2) user explicitly refers to a previous conversation ('continue where we left off', 'as we discussed', 'remember when...'), (3) you need to find a specific past discussion by keyword or time range. Key signal: if you find yourself about to reply 'I don't have context' or 'which topic are you referring to' — use this skill FIRST before asking the user to repeat themselves."
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: hchen13/session-recall
# corpus-url: https://github.com/hchen13/session-recall/blob/d8a5589e0cf4e4934ded4dba176fbebb40a6544e/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Session Recall

Search OpenClaw session transcript JSONL files to locate past conversations. Returns file paths and line numbers — read the relevant lines yourself to recover context.

## When to Use

- **Missing context signal**: Current session is new/short AND the user's message references people, events, decisions, or topics not present in your context — they clearly assume you know something you don't
- **Explicit recall**: User says things like "continue where we left off", "as we discussed", "remember when we talked about..."
- **Self-check**: You're about to reply "I don't have context" or "which topic are you referring to" — **stop and use this skill first** before asking the user to repeat themselves
- You need to find when/where a specific topic was discussed

## Commands

### List available agents

Discover which agent IDs exist and how many sessions each has:

```bash
python3 SKILL_DIR/scripts/session-recall.py agents
```

Use this to find valid agent IDs before searching. Your own agent ID is typically visible in your session key (e.g. `agent:myagent:...` → agent ID is `myagent`).

### List recent sessions

Show sessions with time range, turn count, and first message preview:

```bash
python3 SKILL_DIR/scripts/session-recall.py list --agent AGENT_ID --start 48h --limit 10
```

Output example:
```
/path/to/session.jsonl  [03-08 02:15 ~ 03:35]  32 turns  "Can you look into the impact of..."
```

Use this when the user's query is vague — scan previews to identify the right session, then `read` into it.

### Search by keyword

Find specific mentions across transcripts:

```bash
python3 SKILL_DIR/scripts/session-recall.py search "keyword" --agent AGENT_ID --start 7d --limit 20
```

Output example:
```
/path/to/session.jsonl:142  [03-08 02:15] user: ...the keyword appears here in context...
```

The number after `:` is the line number. Use `read --offset LINE --limit 30` to read surrounding context.

### Time Parameters

`--start` and `--end` define the time window for filtering sessions.

| Format | Example | Meaning |
|--------|---------|---------|
| Relative duration | `30m`, `6h`, `2d`, `1w`, `3mo` | Minutes/hours/days/weeks/months ago |
| Absolute date | `2026-03-01`, `03-01` | Specific date (midnight) |
| Absolute datetime | `2026-03-01T14:00` | Specific date and time |
| Keyword | `today`, `yesterday` | Start of today/yesterday |

- `--start 7d` → sessions from the last 7 days
- `--start 2026-02-01 --end 2026-02-28` → sessions within February
- `--end yesterday` → sessions before today
- Omit `--end` to include everything up to now
- Omit both to search all time

### Pagination

Use `--offset` and `--limit` to paginate through results:

```bash
# First page
session-recall list --start 30d --limit 10
# Second page
session-recall list --start 30d --limit 10 --offset 10
# Third page
session-recall list --start 30d --limit 10 --offset 20
```

The tool prints `Showing X-Y of Z` when there are more results beyond the current page.

### All Parameters

| Parameter | Description |
|-----------|-------------|
| `--agent` | Agent ID. Run `session-recall agents` to list available IDs. Omit to search all. |
| `--start` | Start of time window. Accepts durations, dates, datetimes, or keywords. |
| `--end` | End of time window. Same formats as --start. Omit for "up to now". |
| `--limit` | Max results per page. Default: 20 for list, 30 for search. |
| `--offset` | Skip N results for pagination. Default: 0. |

## Workflow

1. **Detect continuity intent** — user implies prior context you don't have
2. **Try `list` first** — scan session previews to narrow down candidates
3. **Then `search`** if you have keywords, or pick a session from the list
4. **`read` the file** at the returned line numbers (offset/limit) to load context
5. **Continue the conversation** with recovered context

## Important Notes

- Replace `SKILL_DIR` with the actual skill directory path when calling
- Only search your own agent's sessions by default
- The tool does NOT use LLM — it's pure text search, fast and free
- For vague queries with no keywords: use `list`, scan previews, then read promising sessions
- Large sessions may have hundreds of lines — read selectively, don't load entire files
- Use `--offset` to paginate when `--limit` doesn't cover all results