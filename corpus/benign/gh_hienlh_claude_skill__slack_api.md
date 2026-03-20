---
name: slack-api
description: Read Slack messages, threads, channels, download attachments via Python API. Use when you see Slack URLs (https://*.slack.com/archives/*/p*) or need to interact with Slack.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: hienlh/claude-skill-slack-api
# corpus-url: https://github.com/hienlh/claude-skill-slack-api/blob/18f0e5082294c064b85601c005603ba55fdc5c16/skill.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Slack API

Read and interact with Slack using Python (no MCP required).

## Quick Reference

```bash
# Read message/thread from URL
python3 ~/.claude/skills/slack-api/scripts/slack.py --url "SLACK_URL"

# Channel history / Thread replies
python3 ~/.claude/skills/slack-api/scripts/slack.py --history -c CHANNEL_ID -l 10
python3 ~/.claude/skills/slack-api/scripts/slack.py --replies -c CHANNEL_ID --thread-ts TS

# Search / List channels / User info
python3 ~/.claude/skills/slack-api/scripts/slack.py --search "query"
python3 ~/.claude/skills/slack-api/scripts/slack.py --list-channels
python3 ~/.claude/skills/slack-api/scripts/slack.py --user-info USER_ID

# List files from thread (with details)
python3 ~/.claude/skills/slack-api/scripts/slack.py --url "URL" --list-files -v

# Download all files from thread
python3 ~/.claude/skills/slack-api/scripts/slack.py --url "URL" --download-files -o ./downloads

# Output JSON
python3 ~/.claude/skills/slack-api/scripts/slack.py --url "URL" --json
```

## Commands

| Flag | Description | Required |
|------|-------------|----------|
| `--url` | Read from Slack URL | URL |
| `--history` | Channel messages | `-c` |
| `--replies` | Thread replies | `-c`, `--thread-ts` |
| `--search` | Search messages | query |
| `--list-channels` | List channels | - |
| `--user-info` | User details | user_id |
| `--post` | Post message | `-c`, `-t` |
| `--list-files` | List files with details | `--url` or messages |
| `--download-files` | Download all files | `--url` or messages |

## Options

`-c`/`--channel`, `--thread-ts`, `-l`/`--limit` (20), `-o`/`--output-dir` (./slack-downloads), `-v`/`--verbose`, `--json`

## Auth

Tokens loaded from `~/.claude/skills/slack-api/.env`:
```
SLACK_XOXC_TOKEN=xoxc-...
SLACK_XOXD_TOKEN=xoxd-...
```

Get tokens: Browser DevTools -> Application -> Cookies (logged into Slack)

## URL Parsing

`p1767879572095059` -> `1767879572.095059` (insert dot 6 chars from end)