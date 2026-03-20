---
name: send-nda
description: >
  Send Gorgias's standard 2-way NDA to a contact via email or iMessage/text.
  Use this skill whenever Romain asks to send an NDA, share the NDA, or forward
  the mutual NDA to someone — regardless of delivery method. Triggers on phrases
  like: "send NDA to [person]", "share our NDA with [email]", "text the NDA to
  [name]", "send the mutual NDA via text", "forward the 2-way NDA", "can you
  send the NDA over", or any variation where Romain wants to get an NDA signed
  by a counterparty. Even if the user just says "send the NDA" with a name or
  contact in context, use this skill.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Gorgias-Solutions/EA
# corpus-url: https://github.com/Gorgias-Solutions/EA/blob/028bffe1121f7a5e2cefff6e55747555bc54837d/send-nda-SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Send NDA Skill

Gorgias has a standard 2-way (mutual) NDA managed by Camille Savary (Head of Legal). When Romain needs to send it to a counterparty, this skill handles drafting the message — by email or iMessage, depending on what Romain prefers.

## The NDA

Gorgias has migrated from PandaDoc to **SpotDraft**. Unlike PandaDoc, SpotDraft does not support a static shareable form link — a new NDA document must be created from the template each time.

### Creating the NDA in SpotDraft (manual step — Romain must do this)

1. Go to the SpotDraft NDA template: https://app.spotdraft.com/editor-v3/templates/28987/new
2. Fill in the counterparty's name and details
3. Send it to the recipient directly from SpotDraft

Once the document is created and sent via SpotDraft, the recipient will receive an email from SpotDraft to review and sign electronically.

> **Note:** There is currently no SpotDraft API integration, so the agent cannot create or send the NDA automatically. Romain must log into SpotDraft to initiate the document. The agent's role is to remind Romain of the steps and provide the template link.

## Choosing the delivery method

- Since SpotDraft sends the NDA directly to the recipient by email, the delivery channel is always email via SpotDraft
- Romain's role is to create the document in SpotDraft; the agent provides the template link and instructions
- iMessage or email can still be used to follow up or notify the recipient that the NDA is on its way

---

## Workflow: iMessage

Use this when Romain says something like "text him the NDA" or "send the NDA via text."

### Step 1: Find the phone number

If Romain provides a phone number, use it directly. If only a name or email is given, search iMessage contacts using `search_contacts` with the person's name. If multiple results come back, confirm with Romain which one.

### Step 2: Draft the message

Keep it casual and natural — this is a text, not an email. If Romain just had a call or meeting with the person, a brief acknowledgment of that makes it feel warm. Include the NDA link with a short line on why it's needed.

Example (adapt to context):
> Hey [First Name], great chatting just now! Sending over our standard NDA so I can share the Gorgias call recordings with you: [NDA link] — let me know if you have any questions!

If there was no recent interaction, a simpler opener works fine:
> Hey [First Name], here's our standard mutual NDA for review and signature: [NDA link] — let me know if you have questions!

### Step 3: Confirm before sending

Show Romain the proposed message and the recipient's number, then wait for explicit confirmation before sending. Never send automatically.

---

## Workflow: Email

Use this when Romain says "email him the NDA" or doesn't specify a channel.

### Step 1: Identify the recipient

Extract the recipient's name and email from Romain's request. If only a name is given, search Gmail for recent emails with that person to find their address. If ambiguous, ask Romain to confirm.

### Step 2: Find an existing thread (preferred)

Search Gmail for an active recent thread with the recipient. If one exists within the last few weeks, reply to it — this keeps the conversation together and feels more natural than a cold standalone email.

### Step 3: Draft the email

Draft from Romain, keeping it brief (Camille's template is intentionally short and direct):

> Hi [First Name],
>
> Here is the link to our standard NDA for review and signature: [NDA link]
>
> Let me know if you have any questions.
>
> Best,
> Romain

For a new standalone email, use subject: `Gorgias x [Company] — NDA`

### Step 4: Save as Gmail draft

Save as a draft — never send automatically. Confirm with Romain: who it's going to, the subject/thread it's in, and a short preview of the body. Let Romain send it himself.

---

## Notes

- Never send or post automatically — always confirm with Romain first, regardless of channel
- No need to CC Camille unless Romain specifically asks
- If Romain says "send the executed NDA" or "attach the signed NDA", that's a different request (a physical signed document) — this skill only handles new NDA initiations via SpotDraft