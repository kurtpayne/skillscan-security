---
name: macos-reminders
description: Use this skill when you need to work with Apple Reminders.app on macOS through the public scripts/commands interface.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: vinitu/macos-reminders-skill
# corpus-url: https://github.com/vinitu/macos-reminders-skill/blob/1abe52c3d3917f18409f4d9c716f55e31a70f438/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# macOS Reminders

Use this skill when the task is about Apple Reminders.app on macOS.

## Main Rule

Use only `scripts/commands`.
Do not call `scripts/applescripts` directly.

## Requirements

- macOS with Reminders.app access
- `jq`
- `remindctl` for the preferred reminder backend

Account and list commands use AppleScript wrappers and still need `jq` to build JSON output.
Reminder commands prefer `remindctl` and `jq`. They try `remindctl` from `PATH`, then `/opt/homebrew/bin/remindctl`, and use AppleScript fallback only when `remindctl` is not available.

Check `remindctl` access with:

```bash
remindctl status
```

## Public Interface

Run commands from `scripts/commands`:

- `scripts/commands/account/*`
- `scripts/commands/list/*`
- `scripts/commands/reminder/*`

Published reminder commands:

- `list.sh`
- `count.sh`
- `today.sh`
- `overdue.sh`
- `upcoming.sh`
- `due-before.sh`
- `due-range.sh`
- `today-or-overdue.sh`
- `create.sh`
- `get.sh`
- `get-by-id.sh`
- `edit.sh`
- `edit-by-id.sh`
- `reschedule.sh`
- `reschedule-by-id.sh`
- `move.sh`
- `move-by-id.sh`
- `complete.sh`
- `delete.sh`
- `delete-by-id.sh`
- `exists.sh`
- `search.sh`

`scripts/commands/reminder/show.sh` exists in the repo but is not part of the public interface.

## Output Rules

- Commands return JSON by default unless noted otherwise.
- `account/show.sh` and `list/show.sh` open Reminders and return JSON like `{"shown": true, ...}`.
- `reminder/show.sh` is not public and opens the UI without the normalized reminder JSON contract.
- `--json`, `--plain`, and `--format=plain|json` are not supported.

## Accounts

List accounts:

```bash
scripts/commands/account/list.sh
```

Read one account property:

```bash
scripts/commands/account/get.sh "iCloud" id
scripts/commands/account/get.sh "iCloud" reminders_count
```

Search accounts:

```bash
scripts/commands/account/search.sh exact-name "iCloud"
scripts/commands/account/search.sh text "cloud"
```

Get default account and default list:

```bash
scripts/commands/account/default-account.sh
scripts/commands/account/default-list.sh
```

Show an account in the app:

```bash
scripts/commands/account/show.sh "iCloud"
```

## Lists

List all lists or lists in one account:

```bash
scripts/commands/list/list.sh
scripts/commands/list/list.sh "iCloud"
```

Create, edit, delete, and check existence:

```bash
scripts/commands/list/create.sh "Errands"
scripts/commands/list/create.sh "Errands" "#34C759" "list.bullet"
scripts/commands/list/edit.sh "Errands" name "Today"
scripts/commands/list/edit.sh "Today" color "#34C759"
scripts/commands/list/delete.sh "Today"
scripts/commands/list/exists.sh "Inbox"
```

Read one list property and search:

```bash
scripts/commands/list/get.sh "Inbox" id
scripts/commands/list/get.sh "Inbox" color
scripts/commands/list/search.sh exact-name "Inbox"
scripts/commands/list/search.sh text "Err" "iCloud"
```

Show a list in the app:

```bash
scripts/commands/list/show.sh "Inbox"
```

## Reminders

Use the `remindctl` reminder ID or a unique ID prefix as the public reminder identity.
Prefer `--id` for reminder read and write commands.

List and count:

```bash
scripts/commands/reminder/list.sh
scripts/commands/reminder/list.sh "Inbox"
scripts/commands/reminder/count.sh "Inbox"
```

Date filters:

```bash
scripts/commands/reminder/today.sh
scripts/commands/reminder/today.sh "Inbox"
scripts/commands/reminder/overdue.sh "Inbox"
scripts/commands/reminder/upcoming.sh 7 "Inbox"
scripts/commands/reminder/due-before.sh "2030-01-01" "Inbox"
scripts/commands/reminder/due-range.sh "2030-01-01" "2030-01-31" "Inbox"
scripts/commands/reminder/today-or-overdue.sh "Inbox"
```

Create:

```bash
scripts/commands/reminder/create.sh "Inbox" "Buy milk"
scripts/commands/reminder/create.sh "Inbox" "Buy milk" "2 liters" --priority high
scripts/commands/reminder/create.sh "Inbox" "Buy milk" --due "2026-03-14 10:00"
```

Read:

```bash
scripts/commands/reminder/get.sh --id "REMINDER-ID"
scripts/commands/reminder/get.sh --id "REMINDER-ID" body
scripts/commands/reminder/get-by-id.sh "REMINDER-ID" priority
```

Edit, move, complete, and delete:

```bash
scripts/commands/reminder/edit.sh --id "REMINDER-ID" body "3 liters"
scripts/commands/reminder/edit.sh --id "REMINDER-ID" due_date "missing"
scripts/commands/reminder/edit-by-id.sh "REMINDER-ID" priority medium
scripts/commands/reminder/reschedule.sh --id "REMINDER-ID" "2030-01-15"
scripts/commands/reminder/reschedule-by-id.sh "REMINDER-ID" "2030-01-15 12:00"
scripts/commands/reminder/move.sh --id "REMINDER-ID" "Errands"
scripts/commands/reminder/move-by-id.sh "REMINDER-ID" "Errands"
scripts/commands/reminder/complete.sh --id "REMINDER-ID"
scripts/commands/reminder/delete.sh --id "REMINDER-ID"
scripts/commands/reminder/delete-by-id.sh "REMINDER-ID"
```

Exists and search:

```bash
scripts/commands/reminder/exists.sh --id "REMINDER-ID"
scripts/commands/reminder/search.sh exact-name "Inbox" "Buy milk"
scripts/commands/reminder/search.sh id "REMINDER-ID"
scripts/commands/reminder/search.sh incomplete "Inbox"
scripts/commands/reminder/search.sh priority high "Inbox"
scripts/commands/reminder/search.sh has-due-date "Inbox"
scripts/commands/reminder/search.sh text "milk" "Inbox"
```

## JSON Contract

Account object:

- `id`
- `name`
- `lists_count`
- `reminders_count`

List object:

- `id`
- `name`
- `container`
- `color`
- `emblem`

Reminder object:

- `id`
- `name`
- `list`
- `body`
- `completed`
- `priority`
- `due_date`

Reminder priority values:

- `none`
- `low`
- `medium`
- `high`

Scalar envelopes:

- `count`: `{"count": N, "list": "..."}`
- `exists`: `{"exists": true, "id": "..."}`
- `exists` when not found: `{"exists": false, "id": null}`
- property read: `{"id": "...", "property": "...", "value": ...}`
- delete: `{"deleted": true, "id": "..."}`

## Not Public

These reminder features are not part of the public interface:

- `show`
- `flagged`
- `container`
- `creation_date`
- `modification_date`
- `completion_date`
- `allday_due_date`
- `remind_me_date`
- AppleScript reminder IDs