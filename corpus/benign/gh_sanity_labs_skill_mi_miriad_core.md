---
name: miriad-core
description: "Miriad platform reference: execute (JavaScript tool chaining — primary surface for multi-step work), list_tools/document_tool (discover tools), workers (cheap fast sub-agents — use by default), board filesystem with optimistic locking, plan system (specs + tasks with CAS), sandboxes (shell, git, tunnels, GPU), datasets (GROQ queries, real-time listeners), board apps (HTML served as iframes with window.__miriad), secrets (auto-redact, transfer_secret, 15min TTL), environment vars, GitHub (gh CLI, App + PAT modes), skills, custom MCP servers, stdio MCPs (run any MCP server from a sandbox via mcpcli), cross-thread bridging, long-term memory, web search, browser automation., embedded LLM functions (reason/comprehend for inline data processing)"
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: sanity-labs/skill-miriad-core
# corpus-url: https://github.com/sanity-labs/skill-miriad-core/blob/8025b2af7b6de32eca5b8dd14ddc5f9aac76b31f/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# miriad-core

Platform capabilities reference. Every feature available to agents, with patterns and gotchas.

## How Tools Work

Agents have three ways to use tools:

1. **Execute scripts** — JavaScript that chains multiple tool calls with zero inference round-trips. **This is the primary surface for multi-step work.**
2. **Execute scripts** — JavaScript that chains multiple tool calls with zero inference round-trips. **This is the primary surface for multi-step work.** Use `list_tools("keyword")` inside execute to discover available tools.
3. **Workers** — background sub-agents with scoped tool access. Cheap, fast, parallel. The default for any well-defined task.

```js
// Execute example: 4 parallel queries in ~1s instead of ~30s sequential
const [sandboxes, datasets, plan, roster] = await Promise.all([
  sandbox_list({}),
  dataset_list({}),
  plan_status({}),
  get_roster({})
]);
return { sandboxes, datasets, plan, roster };
```

→ `references/execute.md`

## Communication

- `send_message` is the **only** way to talk — plain text responses are NOT delivered
- `@callsign` mentions trigger agent invocation; `@channel` broadcasts to all agents
- Messages support markdown, file attachments (`attachments` param with board paths), and `[secret:N]` auto-redaction
- `get_messages` for history (ULID pagination, sender/keyword filters); `message_search` for full-text search
- `get_roster` shows all members with status, active skills
- `set_status` broadcasts what you're working on (visible in roster + cross-thread)
→ `references/messaging.md`, `references/attachments.md`

## Workers — Orchestrate, Don't Do

- **Workers are the default.** A great agent is a great orchestrator. Workers are cheap, fast sub-agents for ANY well-defined task.
- `spawn_worker` with a detailed brief. Workers run in background, file reports when done.
- Workers can use `execute` for multi-step tool chaining. They inherit all parent agent tools.
- Parallel execution: spawn multiple workers for independent tasks. Reports arrive automatically.
- The brief IS your work product. If you can write a clear brief, it's a worker's job.
- NOT using a worker is the exception — only for real-time conversation or decisions requiring full accumulated context.
- **Critical: save work before deleting sandboxes** — commit to git or write to board first.
→ `references/workers.md`

## Execute — JavaScript Tool Chaining

- `execute` runs JavaScript that calls tools as async functions — **no inference round-trips** between calls
- All tools are bare async functions: `sandbox_exec({})`, `dataset_query({})`
- `list_tools("keyword")` discovers available tools by name or description
- `Promise.all()` for parallel calls — 7 tool calls in ~850ms vs ~30-60s sequential
- `progress("msg")` for real-time updates, `console.log()` for debugging (shown on error only)
- `background: true` for fire-and-forget — result arrives as notification, keeps conversation responsive
- **Direct tools** (`web_search`, `web_fetch`, `spawn_worker`, `set_alarm`) are NOT available inside execute — call them directly first, pass results in
→ `references/execute.md`


## Embedded LLM Functions — reason() and comprehend()

- **reason()** — inline LLM call inside execute scripts. Like `jq()` for unstructured data. Processes one item with selectable model tier.
  - `reason({ prompt, data, model: "light"|"workhorse"|"reasoning" })` → `{ result }`
  - Use for: extraction, classification, synthesis, transformation
- **comprehend()** — batch fan-out over arrays. Light model only, auto-batches at ~150k tokens, parallel processing.
  - `comprehend({ prompt, items })` → array of results
  - Use for: classifying/tagging hundreds of items, down-selecting before deeper analysis
- **The pipeline pattern**: `comprehend()` (fan out, classify) → filter → `reason()` (synthesize with workhorse). Only the final result enters your context window.
- Workers can use both — run entire comprehend→reason pipelines in background without touching the agent's context.
→ `references/embedded-llm.md`

## Files & Board

- Persistent filesystem per channel — text in Postgres, binary in S3
- `read`, `write`, `edit`, `glob`, `search` are **direct tools** — call them directly or inside execute scripts
- `write` (optimistic locking via `version`), `read` (line paging or search-anchored with `around`), `edit` (surgical find-replace, must match exactly once)
- `glob`, `search` (full-text across all files), `mv` (atomic, works on folders), `delete` (soft)
- `upload`/`download` for binary files via presigned URLs
- Cross-channel access: pass `channel` param to read/write other channels' files
- Skill files: pass `skill` param (shortId) to access skill filesystems
- **Raw serving**: files at `/channels/:id/raw/*path` with correct Content-Type — enables static sites and binary images
- **Board apps**: HTML files open as iframes with `window.__miriad` (spaceId, channelId) — relative API URLs, no CORS, no auth tokens. Can query datasets directly.
→ `references/filesystem.md`, `references/cross-channel-files.md`, `references/board-apps.md`

## Plan System

- **Specs** (what to build): draft → active → done → archived
- **Tasks** (how to build it): draft → backlog → slated → ongoing → done → archived
- `plan_status` for quick overview; `plan_update` for atomic CAS (claim tasks, change state); `plan_edit` for surgical body edits
- Tasks link to specs, have assignees. `plan_list` filters by type/state/assignee/spec/search.
→ `references/plan-system.md`

## Secrets & Environment

- User pastes secret in chat → auto-redacted to `[secret:N]` → use `transfer_secret` to store permanently (env var or MCP header). **15-minute TTL** on ephemeral secrets.
- `get_environment` shows resolved env with `[secret]` placeholders. `set_environment_var`/`delete_environment_var` for plaintext config.
- Resolution: global secrets → plaintext vars → local secrets (local wins)
- Auto-provisioned: `MIRIAD_SPACE_TOKEN` (API access), `GH_TOKEN`/`GITHUB_TOKEN` (GitHub)
→ `references/secrets.md`, `references/environment.md`

## Sandboxes

- Isolated containers: shell (`exec`), filesystem, git (clone/commit/push with auto-injected creds), tunnels (public URLs for web apps)
- **Daytona** (CPU, always available) and **RunPod** (GPU, BYOK)
- Channel env + secrets auto-injected. Key vars: `MIRIAD_API_URL`, `MIRIAD_SPACE_ID`, `MIRIAD_SPACE_TOKEN`, `GH_TOKEN`
- Ephemeral — commit to git or write to board. Auto-stop after 30min idle.
- `Glob` is already recursive — use `*.ts` not `**/*.ts`
- **Sandbox tools emit raw output** — no truncation, no pagination. The execute layer handles context management. Board read returns {path, content, version, totalLines} only. Use targeted tools — grep for finding, read with offset for viewing.
→ `references/sandboxes.md`, `references/code-exploration.md`

## Datasets

- JSON document database (jsonsphere + GROQ). Create, query, mutate, delete documents.
- Real-time WebSocket listeners via signed URLs (one-time use, 60s TTL, dataset-bound)
- Access via execute (`dataset_query`, etc.), REST API (browser board apps), or space token (sandboxes)
- Lazy provisioning — just start creating datasets, no setup needed
→ `references/datasets.md`

## GitHub

- Two credential modes: **GitHub App** (scoped installation tokens, 55min TTL, auto-refresh) or **PAT** (global secret `GITHUB_PAT`)
- `gh` CLI in sandboxes for full GitHub API surface (repos, PRs, issues, Actions, releases)
- CI monitoring: `curl` GitHub Actions API from sandboxes — the commit status API doesn't show Actions
→ `references/github-cli.md`, `references/ci-monitoring.md`

## Skills & Custom MCP Servers

- Skills inject SKILL.md into system prompt on next invocation. `skills_discover` → `skills_import` → `skills_activate`.
- Custom MCP servers can be registered for third-party integrations (Sanity, etc.) — use `mcp_put` to register, user authorizes OAuth via UI
→ `references/skills-and-mcp.md`

## Cross-Thread & Memory

- Active in multiple threads simultaneously. `list_my_threads`, `search_my_threads`, `get_thread_state` (peek without switching)
- `post_to_thread` to bridge information across channels
- `update_thread_description` (stable label), `update_thread_status` (ephemeral progress), `update_tasks` (personal task list)
- Long-term memory: `ltm_search`, `ltm_glob`, `ltm_read` — persistent knowledge shared across all threads
→ `references/threads-and-memory.md`

## Web & Background

- `web_search` (freshness filters: 24h/1w/1m/1y), `web_fetch` (extract from URL with question), `web_search_images`
- These are **direct tools** — call them directly, not through execute
- `set_alarm` for reminders and scheduled checks. `list_tasks` / `cancel_task` for management.
- `execute({ background: true })` for fire-and-forget I/O pipelines
→ `references/web-and-workers.md`

## Browser Automation

- `agent-browser` CLI in sandboxes — headless Chromium with ref-based interaction (93% context savings vs DOM dumps)
- Workflow: `open` URL → `snapshot -i` (interactive elements) → interact via refs (`click @e1`, `fill @e2 "text"`)
- Screenshots, JavaScript eval, sessions for state persistence
→ `references/agent-browser.md`

## Stdio MCP Servers

- Run **any stdio MCP server** from a sandbox using `mcpcli` (`npx github:sanity-labs/mcpcli`) — no permanent configuration needed
- More flexible than mounted servers: install, call tools on demand, tear down. No OAuth, no slug registration.
- `mcpcli` passes full environment to child processes — API keys just work
- Works with any ecosystem MCP server: fal.ai (18 tools for AI generation), filesystem, databases, etc.
→ `references/stdio-mcp-servers.md`

## For Humans

→ `references/human-onboarding.md` — guide for introducing new human users to the platform