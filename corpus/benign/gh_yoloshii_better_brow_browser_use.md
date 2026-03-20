---
name: browser-use
description: Agentic browser automation with persistent sessions and ARIA snapshot-based navigation. Use when user needs to browse websites, interact with web pages, fill forms, login to sites, warm up social accounts, bypass anti-bot protection, take screenshots, execute JavaScript on pages, manage cookies, handle multi-tab workflows, extract page content as Markdown, search page text, find elements by role or text, upload files, download files, use WebMCP structured tools on Chrome 146+ pages, or perform any multi-step browser task. Three stealth tiers (Playwright, Patchright, Camoufox) with auto-escalation for anti-bot, session persistence with cookie/storage profiles, element ref system, WebMCP tool discovery, new-element detection between snapshots, action loop detection with escalating warnings, auto popup dismissal, download handling, click-by-coordinate fallback, context compaction for long sessions, idle session GC, and per-session locking.
allowed-tools: Bash(curl*), Bash(python*), Bash(pkill*), Read
triggers:
  - browse
  - visit
  - navigate to
  - open website
  - warm up
  - social warming
  - browser agent
  - interact with page
  - fill form
  - login to
  - bypass anti-bot
  - screenshot
  - execute javascript
  - manage cookies
  - stealth browser
  - anti-detect
  - extract page content
  - page to markdown
  - search page text
  - find element
  - upload file
  - download file
  - webmcp
  - structured tools
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: yoloshii/better-browser-use
# corpus-url: https://github.com/yoloshii/better-browser-use/blob/db3b4897a3117bcbf9b7ec3446fcf9a8db6a6c88/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Browser-Use Skill

Agentic browser controller. YOU are the agent — observe page state via ARIA snapshots, reason about what to do, execute actions, repeat until done.

## Quick Start

```bash
# Launch session
curl -s -X POST http://127.0.0.1:8500/ -H 'Content-Type: application/json' \
  -d '{"op":"launch","tier":1,"url":"https://example.com"}'

# Snapshot (get ARIA tree with @e1, @e2 refs)
curl -s -X POST http://127.0.0.1:8500/ -H 'Content-Type: application/json' \
  -d '{"op":"snapshot","session_id":"<id>","compact":true}'

# Click element
curl -s -X POST http://127.0.0.1:8500/ -H 'Content-Type: application/json' \
  -d '{"op":"action","session_id":"<id>","action":"click","params":{"ref":"@e1"}}'

# Close
curl -s -X POST http://127.0.0.1:8500/ -H 'Content-Type: application/json' \
  -d '{"op":"close","session_id":"<id>"}'
```

## Execution

Persistent HTTP server on port 8500. All requests: `POST /` with JSON body.

Server binds `127.0.0.1` by default. Set `BROWSER_USE_TOKEN` for Bearer auth. Set `BROWSER_USE_EVALUATE=1` to enable arbitrary JS execution.

```bash
# Health check (no auth required)
curl -s http://127.0.0.1:8500/health

# With auth
curl -s -X POST http://127.0.0.1:8500/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <token>' \
  -d '<json>'

# Start server
BROWSER_USE_TOKEN=<secret> ~/.venvs/scraper/bin/python3 ~/sirus-skills/browser-use/scripts/server.py --port 8500

# Stop
pkill -f 'server.py --port 8500'
```

Idle sessions auto-reaped after TTL (default: 1 hour).

## Agent Loop

1. **Launch** session (optionally with profile)
2. **Navigate** to target URL
3. **WebMCP Discover** (optional) — `{"op":"action","action":"webmcp_discover"}` to probe for structured tools
4. **If WebMCP tools found:**
   - Read tool schemas (names, descriptions, inputSchema)
   - **Prefer `webmcp_call`** for form submissions and structured actions
   - Fall back to ARIA for non-tool interactions (scrolling, reading, navigation)
5. **If no WebMCP tools (standard path):**
   - **Snapshot** — get ARIA tree with refs (@e1, @e2, ...)
   - **Reason** — analyze tree, decide action(s)
   - **Act** — execute using refs
   - **Observe** — check result, re-snapshot if page changed
6. **Repeat** until done
7. **Save** state and **close**

After navigating to a new page, re-run `webmcp_discover` (tools change per page).

## Operations

### Launch
```json
{"op": "launch", "tier": 1, "url": "https://example.com", "profile": "my-identity"}
```
Returns: `{success, session_id, tier, url, title}`

### Snapshot
```json
{"op": "snapshot", "session_id": "<id>", "compact": true}
```
Returns: `{success, tree, refs, url, title, tab_count}`

ARIA tree format:
```
Page: https://x.com/home | Title: Home / X
Tab 1 of 1

- navigation "Main"
  - link "Home" @e1
  - link "Explore" @e2
- main
  - heading "Home" @e3 [level=1]
  - article
    - link "@username · 2h" @e4
    - text "Post content here..."
    - button "Like" @e5 [pressed=false]
    - button "Reply" @e6
```

### Action
```json
{"op": "action", "session_id": "<id>", "action": "click", "params": {"ref": "@e5"}}
```
Server uses ref_map from last snapshot. Override with `"ref_map": {...}` if needed.

Returns: `{success, extracted_content, error, page_changed, new_url}`

### Screenshot
```json
{"op": "screenshot", "session_id": "<id>", "full_page": false}
```
Returns: `{success, screenshot}` (base64 PNG)

### Save / Close / Status / Profile
```json
{"op": "save", "session_id": "<id>", "profile": "my-identity"}
{"op": "close", "session_id": "<id>", "save_profile": "my-identity"}
{"op": "status"}
{"op": "status", "session_id": "<id>"}  → includes action_count, duration_seconds, humanize, humanize_intensity
{"op": "profile", "action": "list"}
{"op": "profile", "action": "create", "name": "x-primary", "domain": "x.com"}
{"op": "profile", "action": "load", "name": "x-primary"}
{"op": "profile", "action": "delete", "name": "x-primary"}
```

## Actions

### Core
| Action | Params | Description |
|--------|--------|-------------|
| `navigate` | `{url}` | Go to URL |
| `click` | `{ref}` | Click element by ref |
| `dblclick` | `{ref}` | Double-click element by ref |
| `rightclick` | `{ref}` | Right-click element by ref (opens context menu) |
| `fill` | `{ref, value}` | Atomic fill (clears first). For forms. |
| `type` | `{ref, text, delay_ms?}` | Character-by-character typing. For compose/search. |
| `scroll` | `{direction: up\|down, amount: int\|"page"}` | Scroll page |
| `snapshot` | `{compact?, max_depth?, cursor_interactive?}` | ARIA tree + refs |
| `screenshot` | `{full_page?}` | Base64 PNG |
| `wait` | `{ms?, selector?, text?, state?, timeout?}` | Wait for time, selector, or text. `state`: visible\|hidden\|attached (default: visible). Max 30s. |
| `evaluate` | `{js, deep_query?, frame_url?}` | Execute JavaScript (requires BROWSER_USE_EVALUATE=1). Set `deep_query: true` to inject `deepQuery(sel)` / `deepQueryAll(sel)` helpers that pierce shadow DOM. |
| `done` | `{result, success?}` | Mark task complete |
| `solve_captcha` | `{}` | Auto-detect + solve CAPTCHA on page (CapSolver → 2Captcha fallback) |

### Extended
| Action | Params | Description |
|--------|--------|-------------|
| `press` | `{key, ref?}` | Keyboard press ("Enter", "Tab", "Escape") |
| `select` | `{ref, value}` | Dropdown selection |
| `go_back` | `{}` | Browser back |
| `cookies_get` | `{domain?}` | Get cookies |
| `cookies_set` | `{cookies: [...]}` | Set cookies |
| `cookies_export` | `{path, domain?}` | Export cookies to JSON file. Optional domain filter. Read-only. |
| `cookies_import` | `{path}` | Import cookies from JSON file into browser context |
| `tab_new` | `{url?}` | New tab |
| `tab_switch` | `{index}` | Switch tab (0-based) |
| `tab_close` | `{index}` | Close tab |

### WebMCP (Chrome 147+)
| Action | Params | Description |
|--------|--------|-------------|
| `webmcp_discover` | `{}` | Probe page for WebMCP tools (imperative + declarative). Run after navigate. |
| `webmcp_call` | `{tool, args}` | Call a WebMCP tool with structured arguments |

WebMCP tools appear in snapshot headers after discovery. Use `webmcp_call` instead of fill/click/snapshot cycles when tools are available.

### Search & Discovery
| Action | Params | Description |
|--------|--------|-------------|
| `search_page` | `{query, max_results?}` | Text search across visible page content. Case-insensitive. Read-only, no rate limit. |
| `find_elements` | `{text?, role?}` | Find refs matching criteria in current snapshot. At least one param required. Read-only. |
| `extract` | `{max_chars?, include_links?}` | Full page to markdown. Use when ARIA tree lacks detail. Read-only but expensive. |

### File & Coordinate
| Action | Params | Description |
|--------|--------|-------------|
| `upload_file` | `{ref, path}` | Upload file to input[type=file] near ref |
| `get_downloads` | `{}` | List files downloaded in this session. Read-only. |
| `click_coordinate` | `{x, y}` | Click at viewport coordinates. Last resort for non-ARIA elements. |

### Element Inspection
| Action | Params | Description |
|--------|--------|-------------|
| `get_value` | `{ref}` | Get current value of input/textarea/select. Falls back to textContent. Read-only. |
| `get_attributes` | `{ref}` | Get all HTML attributes + tag name (`_tag`). Read-only. |
| `get_bbox` | `{ref}` | Get bounding box `{x, y, width, height}` in viewport pixels. Use for `click_coordinate` targeting. Read-only. |

### Agent Guidance

**Action cost**: `search_page`, `find_elements`, `get_downloads`, `get_value`, `get_attributes`, `get_bbox`, `cookies_export` are free (read-only, no rate limit). `extract` is expensive (full page parse). Page-changing actions (`navigate`, `click`, `dblclick`, `rightclick`, `fill`, `upload_file`, `click_coordinate`, `cookies_import`) count toward rate limits.

**Action chaining**: Put page-changing actions last. Safe to chain read-only actions before them.

**New element detection**: Elements new since last snapshot are prefixed with `*` in the ARIA tree:
```
- button "Submit" @e1
*- button "Confirm" @e2     <-- NEW since last snapshot
- textbox "Email" @e3
```
New elements often appear after form interactions. Interact with them when relevant.

**SPA re-detection**: After `navigate`, the server tracks the requested URL. If a subsequent `snapshot` sees a different URL (SPA client-side redirect, e.g. `x.com` → `x.com/home`), the response includes `{"spa_navigation": true, "spa_from": "...", "spa_to": "..."}`. The `navigate` response itself flags immediate redirects as `{"spa_redirect": true}`. Use this info to confirm you're on the expected page.

**Loop detection**: The server detects repetitive action patterns. If you receive a `loop_warning` in the response:
- **WARNING**: 3+ repetitions on same page — try a different approach
- **STUCK**: 5+ repetitions — navigate elsewhere or use `evaluate` to inspect DOM
- **CRITICAL**: 7+ repetitions — call `done` immediately with partial results

**Pre-done verification**: Always verify task completion before calling `done`. Take a final snapshot to confirm expected state.

## Auto Popup Dismissal

JavaScript dialogs (alert, confirm, prompt) are automatically handled:
- `alert` / `confirm` / `beforeunload`: Accepted (OK)
- `prompt`: Dismissed (Cancel)

Dismissed popup messages appear in the next snapshot header. No action needed from the agent.

## Download Handling

File downloads are auto-saved to a session temp directory. Check downloads via `get_downloads` action. Downloaded file info appears in snapshot headers when files are available.

## Ref System

- Refs assigned sequentially: `@e1`, `@e2`, `@e3`, ...
- Reset on every new snapshot
- Server persists ref_map from each snapshot — actions use latest automatically
- If action fails with "ref not found", take a new snapshot
- Covers: buttons, links, inputs, checkboxes, headings, articles
- `[cursor-interactive]` = non-ARIA clickables detected by `cursor: pointer`

## Session Persistence

Profiles store identity state across sessions:
```
~/.openclaw/browser-profiles/<name>/
├── cookies.json
├── storage.json    (localStorage + sessionStorage)
├── meta.json       (tier, domain, timestamps)
└── fingerprint.json (Tier 3: BrowserForge)
```

Use `"profile": "<name>"` in launch to restore, `"save_profile": "<name>"` in close to persist.

## Humanization

Tier 2+ sessions auto-enable humanized actions. Set `BROWSER_USE_HUMANIZE=1` to force for all tiers.

When active:
- **click**: Bezier curve mouse movement from actual cursor position, random offset, variable settle delay
- **type**: Gaussian inter-key delays (80ms base), digraph optimization, occasional thinking pauses
- **scroll**: Eased acceleration/deceleration, reading pauses after scroll

Mouse position is tracked via page-level listener — Bezier curves start from real cursor position, not a fixed point.

Sensitive domains (linkedin.com, facebook.com, x.com, instagram.com) auto-boost humanize intensity to 1.3x when humanization is active. No configuration needed.

Non-humanized path unchanged for Tier 1 speed.

## Rate Limiting

Server enforces per-domain action rate limits (from `Config.SENSITIVE_RATE_LIMITS`):

| Domain | Limit |
|--------|-------|
| default | 8/min |
| linkedin.com | 4/min |
| facebook.com | 5/min |
| x.com / twitter.com | 6/min |
| instagram.com | 4/min |

Read-only actions (snapshot, screenshot, cookies_get, cookies_export, search_page, find_elements, extract, get_downloads, get_value, get_attributes, get_bbox) are exempt.
If rate limited, response includes `{"code": "RATE_LIMITED", "wait_seconds": N}`.

## Block Detection & CAPTCHA Solving

After page-changing actions, server runs lightweight block detection.
If blocked, response includes `{"blocked": true, "protection": "<type>"}`.

Detected protections: cloudflare, datadome, akamai, perimeterx, captcha, generic.

**Auto-solve**: When CAPTCHA/Cloudflare is detected and `CAPSOLVER_API_KEY` is set, the server automatically attempts to solve it inline. On success: `{"blocked": false, "captcha_solved": true, "solver": "capsolver", "solve_time_s": 3.2}`. On failure: `{"blocked": true, "captcha_solve_failed": true}`.

**Manual solve**: Use `{"action": "solve_captcha"}` to explicitly trigger solving on any page with a CAPTCHA. Supports reCAPTCHA v2/v3, hCaptcha, Cloudflare Turnstile.

## Error Handling

| Error | Recoverability | Action |
|-------|---------------|--------|
| Element not found / ref invalid | RECOVERABLE | Re-snapshot, retry with new refs |
| Navigation timeout | RECOVERABLE | Retry navigate, check URL |
| Page crashed / context destroyed | NON_RECOVERABLE | Close session, relaunch |
| Anti-bot detection (403/captcha) | ESCALATABLE | Escalate tier or rotate proxy |
| Rate limited (429) | RECOVERABLE | Wait, then retry with reduced frequency |
| CAPTCHA detected | ESCALATABLE | Escalate tier or wait and retry |
| Session not found / expired | NON_RECOVERABLE | Launch new session |
| Auth error (401/403 on server) | NON_RECOVERABLE | Check BROWSER_USE_TOKEN |
| Response truncated | RECOVERABLE | Use more targeted snapshot (compact=true, reduce max_depth) |

## Stealth Tiers

| Tier | Engine | Tracker Blocking | Humanize | When |
|------|--------|-----------------|----------|------|
| 1 | Playwright (Chromium) | No | Opt-in | General browsing, friendly sites |
| 2 | CloakBrowser (C++ patched Chromium) / Patchright fallback | Yes | Auto | reCAPTCHA v3 (0.9 score), FingerprintJS, BrowserScan — binary-level stealth |
| 3 | Camoufox (Firefox C++ fork) | Yes | Auto | Turnstile, DataDome — with GeoIP + residential proxy |

## Architecture

| Component | File | Purpose |
|-----------|------|---------|
| Server | `scripts/server.py` | aiohttp HTTP server, auth, request routing, rate limiting, block detection |
| Agent | `scripts/agent.py` | stdin/stdout JSON interface (alternative to server) |
| Browser Engine | `scripts/browser_engine.py` | Multi-tier browser lifecycle, tracker blocking, session management, idle GC |
| Actions | `scripts/actions.py` | Action dispatcher (45 actions) with humanization + shadow DOM piercing |
| CAPTCHA Solver | `scripts/captcha_solver.py` | CapSolver + 2Captcha integration, sitekey extraction, token injection |
| Behavior | `scripts/behavior.py` | Bezier mouse curves, Gaussian typing delays, eased scrolling |
| Detection | `scripts/detection.py` | Anti-bot detection (Cloudflare/DataDome/Akamai/PerimeterX), site profiles |
| Fingerprint | `scripts/fingerprint.py` | SQLite-backed fingerprint persistence per domain, rotation on block rate |
| Rate Limiter | `scripts/rate_limiter.py` | Per-domain sliding window rate limiter |
| Snapshot | `scripts/snapshot.py` | ARIA tree parser, ref assignment, new-element detection |
| Session | `scripts/session.py` | Profile persistence (cookies/storage/fingerprints), path-safe naming |
| FSM | `scripts/agent_fsm.py` | State machine for agent loop |
| Compaction | `scripts/context_compaction.py` | LLM history summarization |
| Errors | `scripts/errors.py` | Error classification with AI-friendly transforms |
| Config | `scripts/config.py` | Settings, geo profiles, env vars |
| Models | `scripts/models.py` | Pydantic v2 type definitions |

## Configuration

| Env Variable | Default | Description |
|-------------|---------|-------------|
| `BROWSER_USE_TOKEN` | (empty) | Bearer auth token for server. Omit to disable auth. |
| `BROWSER_USE_EVALUATE` | `1` | Set to `0` to disable `evaluate` (arbitrary JS) action |
| `BROWSER_USE_HUMANIZE` | `0` | Set to `1` to force humanized actions on all tiers (Tier 2+ auto-enables) |
| `BROWSER_USE_GEO` | (empty) | Geo profile for timezone/locale (e.g., `us`, `uk`, `de`, `jp`). See geo profiles below. |
| `PROXY_SERVER` | (empty) | Proxy URL (e.g., `http://proxy:8080`). Used by Tier 2/3. |
| `PROXY_USERNAME` | (empty) | Proxy auth username |
| `PROXY_PASSWORD` | (empty) | Proxy auth password |
| `CLOAKBROWSER_ENABLED` | `auto` | CloakBrowser Tier 2: `auto` (use if installed), `1` (require), `0` (force Patchright) |
| `CLOAKBROWSER_AUTO_UPDATE` | `false` | Allow CloakBrowser binary auto-updates (`true`/`false`) |
| `CLOAKBROWSER_GEOIP` | `auto` | GeoIP from proxy: `auto` (use if cloakbrowser[geoip] installed), `0` (disable) |
| `CAPSOLVER_API_KEY` | (empty) | CapSolver API key for CAPTCHA solving (primary, fast AI) |
| `TWOCAPTCHA_API_KEY` | (empty) | 2Captcha API key for CAPTCHA solving (fallback, human) |

### Geo Profiles

Set `BROWSER_USE_GEO` to match browser timezone/locale to proxy exit location:

| Code | Timezone | Locale |
|------|----------|--------|
| `us` | America/New_York | en-US |
| `us-la` | America/Los_Angeles | en-US |
| `us-tx` | America/Chicago | en-US |
| `uk` | Europe/London | en-GB |
| `de` | Europe/Berlin | de-DE |
| `fr` | Europe/Paris | fr-FR |
| `jp` | Asia/Tokyo | ja-JP |
| `au` | Australia/Sydney | en-AU |
| `br` | America/Sao_Paulo | pt-BR |
| `in` | Asia/Kolkata | en-IN |

## Dependencies

**Core (all tiers):**
- Python 3.10+
- pydantic v2 (`pip install pydantic>=2.0`) — request/response models
- aiohttp (`pip install aiohttp`) — HTTP server
- markdownify (`pip install markdownify`) — HTML→Markdown for `extract` action
- pyee 13.x (`pip install 'pyee>=13,<14'`) — shared event emitter for Playwright + Patchright

**Tier 1 — Playwright (Chromium):**
- playwright 1.51.x (`pip install 'playwright>=1.51,<1.56' && playwright install chromium`)
- Avoid 1.56+ (WSL2 regression: `new_page()` hangs in headless mode)

**Tier 2 — CloakBrowser (stealth Chromium, preferred) or Patchright (fallback):**
- cloakbrowser (`pip install cloakbrowser`) — 26 C++ source-level Chromium patches (canvas, WebGL, audio, TLS, navigator). Binary auto-downloads ~200MB on first use.
- Patchright (`pip install patchright && patchright install chromium`) is an optional fallback for unsupported platforms or if explicitly disabled via `CLOAKBROWSER_ENABLED=0`
- Set `CLOAKBROWSER_ENABLED=0` to force Patchright, `CLOAKBROWSER_AUTO_UPDATE=true` to allow binary updates
- GeoIP auto-detects timezone/locale from proxy when `cloakbrowser[geoip]` is installed

**Tier 3 — Camoufox (anti-detect Firefox):**
- camoufox (`pip install camoufox[geoip] && python -m camoufox fetch`)
- playwright (`pip install 'playwright>=1.51,<1.56'`) — Camoufox uses Playwright Firefox protocol
- browserforge (installed with camoufox) — statistical fingerprint generation

**Install order** (to avoid pyee conflicts):
```bash
pip install cloakbrowser                # Tier 2 primary (pulls pyee 12 via playwright dep)
pip install 'pyee>=13,<14'              # Override to 13 — required for patchright compatibility
pip install 'playwright>=1.51,<1.56' && playwright install chromium
pip install patchright && patchright install chromium  # Tier 2 optional fallback
pip install aiohttp 'pydantic>=2.0' markdownify
```

All tiers auto-install their browser binaries on first use if not already present.

## WSL2 Known Issues

| Issue | Tier | Symptom | Workaround |
|-------|------|---------|------------|
| Playwright 1.56+ hangs | 1 | `new_page()` never returns in headless mode | Pin `playwright>=1.51,<1.56` |
| Tier 3 Turnstile failure | 3 | Camoufox passes launch but Cloudflare Turnstile never solves (90s poll, zero captures) | Run on native Linux VM via SSH |
| Virtual GPU fingerprinting | 3 | WSL2's synthetic GPU/display stack produces fingerprints Turnstile detects as non-human | Native KVM VM passes; WSL2 does not |

**Tier 3 on WSL2 is unreliable for Turnstile-protected sites.** Camoufox generates hardware-backed fingerprints from the host GPU — WSL2's virtual GPU (Microsoft Basic Render Driver / vGPU) produces inconsistent canvas, WebGL, and audio fingerprints that Cloudflare detects. Tiers 1-2 work normally on WSL2 for non-Turnstile sites.

**If Tier 3 + Turnstile is required:** SSH to a native Linux VM and run the script there.

## WebMCP Integration

WebMCP is a Chrome 147+ web standard that lets pages expose structured tools for AI agents. When available, it replaces guesswork-based form filling with explicit contracts.

### Requirements
- Chrome Dev (147+), Beta, or Canary installed on the host
- Set `BROWSER_USE_CHROME_CHANNEL=chrome-beta` (or `chrome-dev`, `chrome-canary`)
- Or set `BROWSER_USE_CHROME_PATH=/path/to/chrome` for explicit binary
- Set `BROWSER_USE_WEBMCP=1` to force WebMCP mode, or leave as `auto` (default)

### How It Works
1. On session launch, an init script intercepts `navigator.modelContext.registerTool()`/`unregisterTool()` calls
2. `webmcp_discover` reads captured tools + scans `<form toolname>` elements
3. `webmcp_call` invokes tool.execute() (imperative) or fills+submits form (declarative)
4. Discovered tools appear in subsequent snapshot headers

### Example: WebMCP vs ARIA
```
# Without WebMCP (6+ requests):
snapshot → see @e1-@e6 → fill @e1 "LON" → fill @e2 "NYC" → fill @e3 "2026-06-10" → click @e7 → snapshot

# With WebMCP (2 requests):
webmcp_discover → webmcp_call searchFlights {origin:"LON", destination:"NYC", outboundDate:"2026-06-10"}
```

### When WebMCP Helps
- Form-heavy pages (booking, registration, search)
- Pages with complex input schemas (dropdowns, date pickers, multi-step forms)
- Sites that explicitly declare tool contracts

### When WebMCP Won't Help
- Anti-bot sites (they won't implement WebMCP)
- Content reading / scrolling / navigation
- Sites without WebMCP adoption (most of the web, for now)

### Env Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `BROWSER_USE_WEBMCP` | `auto` | `auto` = detect, `1` = force Chrome channel, `0` = disable |
| `BROWSER_USE_CHROME_CHANNEL` | (empty) | Chrome channel: `chrome-dev`, `chrome-beta`, `chrome-canary`, `chrome` |
| `BROWSER_USE_CHROME_PATH` | (empty) | Explicit Chrome binary path (overrides channel) |

## Do NOT Use For

- Simple URL scraping → use `ultimate-scraper`
- YouTube transcripts → use `youtube-transcript`
- SEO audits → use `seo-crawler`
- Direct API calls → use `curl` / HTTP