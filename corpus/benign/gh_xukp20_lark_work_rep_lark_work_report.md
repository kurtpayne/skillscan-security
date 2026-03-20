---
name: lark-work-report
description: Use this skill when the user wants to report task results to Feishu/Lark after completion, with a preflight check that the reporting channel is available.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: xukp20/lark-work-report-skill
# corpus-url: https://github.com/xukp20/lark-work-report-skill/blob/71c676ec5474755b46000c23fb1dfc78c234056c/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Lark Work Report

Use this skill when the user asks to:
- report completion/progress to Feishu/Lark
- establish or repair a stable "work group" reporting channel before task execution

## Required MCP interfaces

- Find group: `im_v1_chat_list` (`useUAT=true`)
- Send report: `im_v1_message_create` (`useUAT=true`, `receive_id_type=chat_id`)
- Create work group if needed: `im_v1_chat_create` (`useUAT=true`)
- Resolve user identity when needed: `contact_v3_user_batchGetId` (`useUAT=true`)

## Default work-group bootstrap

Target group name: `Codex工作群`

1. Run `im_v1_chat_list` and search exact group name match (`name == "Codex工作群"`).
2. If exactly one match exists, store its `chat_id` and send a short connectivity test message.
3. If no exact match:
   - list likely candidates from `im_v1_chat_list` (names containing `Codex` or `工作群`)
   - ask user to confirm whether one candidate should be used
4. If still unresolved:
   - ask user for identity details (name/mobile/email/open_id)
   - ask if a new `Codex工作群` should be created
   - create group via `im_v1_chat_create`, send a test message, and wait for user confirmation
5. Send one test message to the selected/new group and confirm with the CLI user that the channel is correct.
6. Only after reporting channel is confirmed, proceed with the main task workflow.

## Reporting workflow

After finishing a user task:

1. Send a concise report message to the resolved work-group `chat_id`.
2. Report should include:
   - task summary
   - key outputs/artifacts
   - blockers/risks (if any)
   - next-step suggestion (if any)
3. Keep message text compact. If content is long, split into multiple sequential messages.

## Explicit non-goals

- This skill does **not** monitor Feishu for follow-up instructions.
- This skill does **not** run polling loops for new tasks.
- Task intake/clarification happens in CLI conversation unless the user explicitly requests another workflow.

## Safety and behavior constraints

- Never assume group identity from memory; always verify via API in the current session.
- If sender identity or group identity is ambiguous, confirm with the user before sending task reports.
- Do not silently switch to another group without explicit user confirmation.