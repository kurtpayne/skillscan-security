---
name: snip-openclaw-skill
description: Snip provides safe access to a user's connected services (calendar, reminders, and more) with user-configured policies for automatic access, blocked access, and approval-required access.
homepage: https://getsnip.app
metadata: {"openclaw":{"emoji":"✂️","requires":{"bins":["curl","jq"],"env":["SNIP_BEARER_TOKEN"]},"primaryEnv":"SNIP_BEARER_TOKEN"}}
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: frens-app/snip-openclaw-skill
# corpus-url: https://github.com/frens-app/snip-openclaw-skill/blob/b8d88aaa5f6cf236a575a28f70b0e1edd1d049a4/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Snip

Access a user's connected services (calendar, reminders, email, and more) through Snip's permission gateway. Users control which operations are automatic, blocked, or require approval.

## References

- `references/device-grant.md` — interactive setup when no token exists
- `references/system-prompt.md` — instruction block for OpenClaw system prompt
- `references/recovery.md` — error handling and retry rules

## Setup

Run `{baseDir}/scripts/check-token.sh`. If Snip is not connected, ask the user, "Do you want to log in to Snip now?" If yes, walk the user through the device grant flow in `references/device-grant.md`. Never accept bearer tokens pasted into chat.

```bash
export SNIP_API_BASE_URL="${SNIP_API_BASE_URL:-https://api.getsnip.app}"
```

## Common operations

List available operations:

```bash
curl -s -H "Authorization: Bearer ${SNIP_BEARER_TOKEN}" \
  "${SNIP_API_BASE_URL}/v3/operations"
```

Get operation detail:

```bash
curl -s -H "Authorization: Bearer ${SNIP_BEARER_TOKEN}" \
  "${SNIP_API_BASE_URL}/v3/operations/{operationKey}"
```

Submit an operation request (POST to `submitPath` from the operations list):

```bash
curl -s -X POST -H "Authorization: Bearer ${SNIP_BEARER_TOKEN}" \
  -H "Content-Type: application/json" \
  "${SNIP_API_BASE_URL}{submitPath}" \
  -d '{"input": { ... }}'
```

Poll for result:

```bash
curl -s -H "Authorization: Bearer ${SNIP_BEARER_TOKEN}" \
  "${SNIP_API_BASE_URL}/v3/operation-requests/{requestId}"
```

## Example operations (varies by user's connected services)

- `google-calendar:events.list` — fetch upcoming calendar events
- `google-calendar:events.insert` — create a calendar event
- `apple-reminders:reminders.list` — list reminders
- `apple-reminders:reminders.create` — create a reminder
- `gmail:messages.list` — search emails

Available operations depend on the user's connections and permissions. Always check `GET /v3/operations` for the current list.

## Runtime contract

1. `GET /v3/operations` at session start. Cache for `cacheTtlSeconds`.
2. Choose an allowed operation. `POST` to its `submitPath` with `input` plus optional `threadId`, `threadType`, `clientSchemaSetHash`.
3. Poll `GET /v3/operation-requests/{requestId}` until terminal status.
4. Respect `pollAgainAfterMs` and `pollTimeoutMs`.
5. Only confirm success when `completionState=SUCCEEDED` and `status=SUCCESS`.
6. If `completionState=FAILED`, explain failure with `result.resultReason`.

## Status interpretation

- `PENDING_USER_APPROVAL` — tell user it's waiting on approval in Snip.
- `PENDING_EXECUTION` — keep polling, do not ask for manual approval.
- `UNSUPPORTED_OPERATION` — stop, do not retry. Client app needs updating.
- `SUCCESS` with `completionState=SUCCEEDED` — confirm completion.
- `completionState=FAILED` — report `resultReason`, do not claim success.

## Security

- Never print or echo bearer tokens in chat.
- Tokens are persisted automatically via the device grant flow.
- Never paste tokens into system prompts or chat messages.