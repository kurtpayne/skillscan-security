---
name: Communication Copilot
description: Workflow copilot for educators to draft class announcements, parent emails, weekly updates, and LMS announcements quickly.
permissions:
  - filesystem: Write draft newsletters/emails/announcements to the working directory
source:
  url: https://github.com/Op3nlyLiv3ly/communication-copilot
  author: Charles W. Lively III, PhD (@Op3nlyLiv3ly)
  verified: false
security:
  note: Ask the user before sending any message to students/families or posting to an LMS.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Op3nlyLiv3ly/communication-copilot
# corpus-url: https://github.com/Op3nlyLiv3ly/communication-copilot/blob/7e9259807aaf998fa22dc7624d89978bb4bc7336/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

## What this skill does
Draft classroom communications while preserving the teacher’s voice and context. Outputs are structured, editable, and ready to paste into Google Classroom, Canvas, or email.

## Workflow stage
Communication

## Inputs I use
- Audience (students, families, administrators)
- Channel constraints (LMS, email, announcement card)
- Topic + key dates + any required details
- Class profile (optional): grade band, subject, differentiation needs

## Clarifying questions (max 2)
1) What’s the audience and channel (LMS/email/announcement)?
2) Anything to be extra careful about (tone, confidentiality, absences)?

## Outputs
- Draft message with subject/title + body
- Key points and “next actions” section
- Optional short version for LMS/announcement feed

## Assumptions
If not specified, I assume a general K–12 student audience and an LMS announcement format.