---
name: mailescrow
description: Human-in-the-loop email proxy. Use this skill to send and receive emails through a human approval gate. Every message — outbound and inbound — is held until a human approves it.
homepage: https://github.com/acroca/mailescrow
metadata: {"clawdbot":{"requires":{"bins":[],"env":["MAILESCROW_API_URL"]}}}
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: acroca/mailescrow
# corpus-url: https://github.com/acroca/mailescrow/blob/79424cf5dde9e823000a43b446b5dee71bce7c2b/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# mailescrow

> Human-in-the-loop email proxy. Use this skill to send and receive emails through a human approval gate. Every message — outbound and inbound — is held until a human approves it.

## Overview

mailescrow exposes a REST API on a configurable address (`$MAILESCROW_API_URL`). All requests are unauthenticated and use JSON.

Outbound emails you submit are **not sent immediately** — a human must approve them in the web UI first.
Inbound emails you receive have **already been approved** by a human before they reach you.

## When to use which endpoint

| I want to…                                      | Use                                      |
|-------------------------------------------------|------------------------------------------|
| Send an email                                   | `POST $MAILESCROW_API_URL/api/emails`                       |
| Check whether any replies have arrived          | `GET $MAILESCROW_API_URL/api/emails`                        |
| Check how many emails are waiting for approval  | `GET $MAILESCROW_API_URL/api/emails/pending/count`          |

## Send an email

Submit an outbound email for human review. The email is held until approved.

```
POST $MAILESCROW_API_URL/api/emails
Content-Type: application/json
```

```json
{
  "to": ["recipient@example.com"],
  "subject": "Your subject here",
  "body": "Plain text body."
}
```

**Fields:**
- `to` (array of strings, required) — one or more recipient addresses
- `subject` (string, required) — email subject
- `body` (string, optional) — plain text body

**Response `201 Created`:**
```json
{ "id": "550e8400-e29b-41d4-a716-446655440000" }
```

The returned `id` is informational only — you cannot query or cancel a pending email by ID through the API.

## Receive approved inbound emails

Fetch all inbound emails that a human has approved for you to read.

```
GET $MAILESCROW_API_URL/api/emails
```

**Response `200 OK`:**
```json
[
  {
    "id": "...",
    "from": "sender@example.com",
    "to": ["you@example.com"],
    "subject": "Re: Your subject",
    "body": "Reply text here.",
    "received_at": "2026-02-20T10:00:00Z"
  }
]
```

Returns `[]` when no approved emails are waiting. Returns all available emails in a single call.

> **This call is destructive.** Emails are permanently deleted from mailescrow after being returned. Do not call this endpoint unless you are ready to process and store the results.

## Check pending IDs

Returns the IDs of all emails (in both directions) currently waiting for human approval. Safe to poll — does not consume or modify anything.

```
GET $MAILESCROW_API_URL/api/emails/pending/count
```

**Response `200 OK`:**
```json
{ "ids": ["550e8400-e29b-41d4-a716-446655440000", "..."] }
```

Returns an empty array when nothing is waiting. Use this to avoid sending more emails while previous ones are still awaiting approval, or to notify a human that their attention is needed.

## Gotchas

- **Outbound emails are never sent immediately.** There is no way to bypass the approval step. If you need a reply quickly, call `GET $MAILESCROW_API_URL/api/emails/pending/count` and check whether the returned `ids` array is empty to know if your previous email has been reviewed yet.
- **`GET $MAILESCROW_API_URL/api/emails` consumes the emails.** Call it only when you are ready to act on the results. If you call it and discard the response, those emails are gone.
- **You cannot retrieve an email by ID.** The `id` in the submit response is not queryable. Pending emails can only be managed through the web UI.
- **There is no delivery confirmation.** A `201` response means the email was accepted into the queue, not that it was sent. Watch `GET $MAILESCROW_API_URL/api/emails/pending/count` (check that the returned `ids` array is empty) to confirm the human has reviewed it.
- **Sender address is fixed.** The `from` address is configured on the server (`relay.username`) — you cannot override it per request.
- **Multiple recipients are supported.** Pass multiple addresses in the `to` array.