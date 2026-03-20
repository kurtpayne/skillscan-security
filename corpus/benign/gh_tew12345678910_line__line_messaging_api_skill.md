---
name: line-messaging-api-skill
description: Teach and validate LINE Messaging API payload design. Use when building or reviewing LINE bots, webhook handlers, reply or push message flows, Flex Messages, Quick Replies, Rich Menus, supported LINE message types, or LINE action objects. Use this skill when the model must choose the right LINE UI surface and produce conservative, LINE-compatible JSON without inventing unsupported fields.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Tew12345678910/line-messaging-api-skill
# corpus-url: https://github.com/Tew12345678910/line-messaging-api-skill/blob/286907515b1cbb5f80c0c9a38fb922426d16ef68/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# LINE Messaging API

Use this skill to reason about how LINE bots respond to users and to format valid payloads for the Messaging API.

Prioritize conceptual correctness first, then JSON correctness. If a rich layout is uncertain, fall back to a simpler valid payload.

## Workflow

1. Identify the sending mode.
   Reply when handling a webhook event and a `replyToken` is available.
   Push when proactively sending to a known user, group, or room target.
2. Choose the lightest UI that fits the job.
   Use text for simple answers, quick replies for small choice sets, Flex for rich cards/layouts, and rich menus for persistent navigation.
3. Compose only official LINE message objects and action objects.
4. Validate limits and required fields before returning JSON.

## Response Model

- LINE bots are webhook-driven: LINE sends an event to the backend, then the backend decides how to respond.
- Reply flow: use the `replyToken` from the webhook event and send `1` to `5` message objects in one reply request.
- A `replyToken` can only be used once and must be used within one minute after receiving the webhook.
- Push flow: send `1` to `5` message objects to a known target outside the immediate webhook reply path.
- Message arrays contain LINE message objects only. Rich menu definitions are managed separately and are not reply or push message objects.
- Quick replies attach to an outgoing message object; they are not standalone messages.

## Message Objects

- Know the main message families: `text`, `image`, `video`, `audio`, `location`, `sticker`, `template`, and `flex`.
- Use `text` as the safest fallback when requirements are unclear.
- Use `template` for older structured layouts only when the product already depends on template messages.
- Use `flex` for custom cards, richer information density, and layout control.

## Actions

- Know the major action types: `message`, `postback`, `uri`, `datetimepicker`, `camera`, `cameraRoll`, `location`, `richmenuswitch`, and `clipboard`.
- Match the action to the surface. Not every action is valid in every UI surface.
- `camera`, `cameraRoll`, and `location` are quick reply-only actions.
- `richmenuswitch` can only be used in rich menus.
- When unsure, prefer `message`, `postback`, or `uri` because they are the safest general-purpose actions.

## Flex Messages

- Treat Flex as a hierarchy: container -> blocks -> components.
- Use `bubble` for one card and `carousel` for multiple cards.
- Inside a bubble, use the standard blocks: `header`, `hero`, `body`, and `footer`.
- Use nested `box` components to control layout and grouping.
- Always provide `altText` on the top-level flex message object.
- Keep layouts concise and mobile-first. Avoid dense desktop-style compositions.

## Quick Replies

- Attach quick replies to a message object.
- Use quick replies for lightweight branching, confirmations, or input shortcuts.
- Keep the menu small and focused even though LINE supports up to `13` quick reply items.
- If multiple message objects are sent, only the `quickReply` on the last message object is displayed.
- If the choice set is larger or needs imagery/layout, use Flex instead.

## Rich Menus

- Rich menus are persistent chat navigation surfaces, not message objects.
- Build them from a menu definition with `size`, `name`, `chatBarText`, and `areas`.
- Each `area` needs `bounds` and exactly one `action`.
- A rich menu also needs an image upload and must be set as default or linked to users before it appears in chat.
- Use `richmenuswitch` when the experience needs persistent navigation between menu states or tabs.

## Validation Rules

- Never invent LINE fields or merge schemas from different object families.
- Never mix Flex container structure with rich menu structure.
- Prefer a simpler valid payload over a richer invalid payload.
- Use LINE's validate endpoints when available for message objects and rich menu objects.
- If required details are missing, return text or structured intermediate data instead of broken JSON.

## References

- Read `concepts.md` for webhook flow, reply vs push, and UI selection guidance.
- Read `message-types.md` for the main LINE message families and their core fields.
- Read `actions.md` for action type selection and JSON naming details.
- Read `flex-messages.md` for container, block, and component structure.
- Read `quick-replies.md` for attachment rules, limits, and usage patterns.
- Read `rich-menus.md` for persistent menu structure and area design.
- Read `validation-rules.md` before returning JSON.
- Reuse the payloads in `examples/` as shape references, then adapt them to the user request.