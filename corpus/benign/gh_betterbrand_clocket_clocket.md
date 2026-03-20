---
name: clocket
description: >
  Self-hosted, privacy-first calendar for OpenClaw agents. Powered by Radicale (CalDAV).
  Use when an agent needs to manage events, editorial calendars, recurring schedules,
  guest coordination, or reminders — without cloud accounts. Data never leaves the machine.
  Syncs with any CalDAV client (Apple Calendar, Thunderbird, DAVx⁵).
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: betterbrand/clocket
# corpus-url: https://github.com/betterbrand/clocket/blob/630ba63f929dda34b453ef3626978af9f1165be2/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Clocket

Self-hosted calendar management for OpenClaw agents. No cloud. No accounts. No data leaving your machine.

Powered by [Radicale](https://radicale.org), a lightweight CalDAV server that stores everything locally.

## Quick Start

```bash
# Install Radicale + configure + start server
bash scripts/install.sh

# Create a calendar
bash scripts/clocket.sh create "work" "Work Calendar"

# Add an event
bash scripts/clocket.sh add "work" \
  --title "Team Sync" \
  --start "2026-03-10T09:00" \
  --end "2026-03-10T09:30" \
  --tz "America/Los_Angeles"

# Add a recurring event
bash scripts/clocket.sh add "work" \
  --title "Weekly Standup" \
  --start "2026-03-10T09:00" \
  --end "2026-03-10T09:30" \
  --recurring weekly \
  --tz "America/Los_Angeles"

# List events
bash scripts/clocket.sh list "work"

# List upcoming N events
bash scripts/clocket.sh list "work" --upcoming 5

# Update an event
bash scripts/clocket.sh update "work" "event-uid" \
  --title "New Title" \
  --description "Updated notes"

# Delete an event
bash scripts/clocket.sh delete "work" "event-uid"

# List all calendars
bash scripts/clocket.sh calendars
```

## Architecture

```
Agent (OpenClaw) → scripts/clocket.sh → Radicale (localhost:5232) → Local filesystem
                                              ↕
                                        CalDAV Clients
                                   (Apple Calendar, Thunderbird, DAVx⁵)
```

All data stored in `~/.openclaw/workspace/data/radicale/collections/`.

## Editorial Calendar Workflow

Built for content calendars — podcast guests, X Spaces, blog posts:

```bash
# Create editorial calendar
bash scripts/clocket.sh create "spaces" "Weekly X Spaces"

# Add episode with guest tracking
bash scripts/clocket.sh add "spaces" \
  --title "S01E05 - AI Privacy with Jane Doe" \
  --start "2026-04-03T09:30" \
  --end "2026-04-03T10:00" \
  --description "Guest: Jane Doe (@janedoe)\nTopic: Privacy in decentralized AI" \
  --location "X (Twitter) Spaces" \
  --recurring weekly \
  --tz "America/Los_Angeles"

# See what's coming up
bash scripts/clocket.sh list "spaces" --upcoming 4
```

## CalDAV Client Sync

View calendars on your devices by connecting any CalDAV client to `http://127.0.0.1:5232`.
See `references/client-sync.md` for per-platform setup.

## Configuration

Default config: `~/.config/radicale/config`

| Setting | Default | Notes |
|---------|---------|-------|
| Bind address | `127.0.0.1:5232` | Localhost only — never exposed by default |
| Auth | htpasswd (plain) | Use bcrypt if exposing via reverse proxy |
| Storage | `~/.openclaw/workspace/data/radicale/collections/` | Flat files, easy to backup |

## Requirements

- Python 3.8+
- macOS or Linux
- `curl` (for CalDAV requests)

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Server won't start | Check port: `lsof -i :5232` |
| Auth failing | Verify `~/.config/radicale/users` |
| LaunchAgent not loading | `launchctl load ~/Library/LaunchAgents/com.clocket.plist` |
| No events returned | Ensure calendar exists: `bash scripts/clocket.sh calendars` |

## License

MIT