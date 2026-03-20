---
name: capture-analytics
description: >
  AI-driven network traffic capture and analysis using mitmproxy/mitmdump + Playwright.
  Triggers on 抓包/流量捕获/网络抓包, HAR 文件分析, websocket/ws 流量, TLS/SSL 分析,
  request replay/流量对比, and API discovery or network debugging requests.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: dtamade/fafafa-skills-capture-analytics
# corpus-url: https://github.com/dtamade/fafafa-skills-capture-analytics/blob/ab09af2329c408eb4c778b7fd14f7a2481f881bf/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Capture Analytics

> AI-driven autonomous network traffic capture and deep analysis.

## Smart URL Extraction

AI 会自动从用户消息中提取 URL：
- "帮我分析 example.com" → URL = https://example.com
- "抓包 http://localhost:3000" → URL = http://localhost:3000
- "看看 192.168.1.1 的请求" → URL = http://192.168.1.1

**Analysis Goal Inference:**
| Keywords | Goal |
|----------|------|
| 性能/慢/延迟/加载 | performance |
| 安全/漏洞/头部/HTTPS | security |
| 调试/错误/失败/500 | debugging |
| API/接口/端点/请求 | api-discovery |
| (none of above) | general |

---

## Purpose

This skill gives Claude Code the ability to **autonomously** capture and analyze
network traffic. Instead of just providing guidance, the AI itself:

1. Starts mitmproxy to intercept traffic
2. Drives Playwright browser through the target site
3. Stops capture and processes the data pipeline
4. Reads and analyzes the structured output
5. Generates comprehensive reports

## Prerequisites

- `mitmproxy` installed (`pip install mitmproxy` or system package)
- `python3` with mitmproxy Python bindings
- Playwright MCP server connected (for browser exploration)
- Bash shell environment

Verify with:
```bash
which mitmdump && mitmdump --version
python3 -c "from mitmproxy import io; print('OK')"
```

## Execution Contract (Task-Adaptive Traffic Generation)

When the user asks to capture live traffic, the AI MUST choose execution mode by task type (not one fixed method):

- **Browser mode**: web page/user-journey exploration via Playwright MCP.
- **Program mode**: run target process with temporary proxy env vars (`HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`).
- **Manual-assist mode**: user drives app manually while capture is running.

Required minimum actions:

1. Start capture (`capture-session.sh start ...`)
2. Choose ONE traffic-generation mode above
3. Ensure at least one network-producing action/request happens
4. Stop capture (`capture-session.sh stop`)
5. Verify artifacts are non-empty (`latest.flow` size > 0, `latest.index.ndjson` lines > 0)

### Capture Decision Gate (Session/Cookie/Header Aware)

Before starting capture, the AI MUST classify the task:

- **No capture needed**: user already has exact request details (URL/method/headers/body/cookies) and only needs direct API replay/response check.
- **Capture required**: request chain/session bootstrap is unknown, or flow depends on dynamic cookies/CSRF/OAuth redirects/browser state.

Rules:
- Do not use curl smoke test as a substitute for real session workflows.
- Use smoke test only to verify proxy connectivity/path.
- For auth/session scenarios, generate traffic from the real client context (browser/app/program), then capture/analyze.

### Browser Mode Reliability Rules (Headless-First)

If browser automation is selected, the AI MUST:

1. Prefer headless execution in non-GUI environments
2. If Playwright fails with XServer/headed error, retry once in headless mode
3. If browser mode is still unavailable, switch to program mode or manual-assist mode
4. Never abort capture workflow after one Playwright launch failure

If selected mode is unavailable, the AI MUST:
- State explicitly which mode is unavailable and why
- Switch to the next-best mode
- Run proxy smoke test when needed (`curl -x http://127.0.0.1:<port> http://example.com/`)
- Continue with analysis and clearly label fallback mode in the report

## Five-Phase Workflow

### Phase 1: RECON (Reconnaissance)

Understand the user's goal before touching anything.

**AI Actions:**
1. Extract target URL from user message
2. Determine analysis focus (performance / security / debugging / general)
3. Choose exploration strategy (see [BROWSER_EXPLORATION.md](references/BROWSER_EXPLORATION.md))
4. Check prerequisites (mitmproxy installed? Playwright available?)

**Decision Matrix:**

| User Says | Focus | Strategy |
|-----------|-------|----------|
| "分析这个网站的性能" | Performance | Full-site crawl, measure timings |
| "看看这个API有什么请求" | API Discovery | Navigate key flows, catalog endpoints |
| "检查安全问题" | Security | Probe forms, check headers, test inputs |
| "调试这个页面的错误" | Debugging | Target specific page, capture errors |
| "对比两次部署的差异" | Comparison | Capture twice, diff results |

### Phase 2: CAPTURE (Start Interception)

**AI executes:**
```bash
capture-session.sh start https://example.com
```

Or with explicit scope control:
```bash
capture-session.sh start https://example.com --allow-hosts "example.com,*.example.com"
```

Key flags:
- `-d, --dir <path>` — output directory for capture files
- `-P, --port <port>` — custom port (default 18080)
- `--allow-hosts <list>` — restrict capture to these hosts (comma-separated, supports *)
- `--deny-hosts <list>` — always ignore these hosts (takes precedence)
- `--policy <file>` — JSON policy file for complex scope rules

Cleanup flags:
- `--keep-days <N>` — keep capture files from recent N days
- `--keep-size <SIZE>` — keep latest captures up to total size
- `--secure` — securely delete old capture files
- `--dry-run` — preview cleanup result without deleting
- `--force-recover` — clean stale state file before start
- `-h, --help` — print CLI help and exit

**Scope Control:**
By default, capture-session.sh auto-generates a scope from the target URL domain.
This prevents capturing traffic from unrelated domains (e.g., analytics, auth providers).

After starting, the proxy is at `127.0.0.1:18080`.

### Phase 3: EXPLORE / DRIVE TRAFFIC (Mode-Based)

Choose the traffic-driving mode based on the target:

- **Browser workflow (web pages/session flows):** use Playwright through proxy.
- **Program workflow (CLI/service/mobile bridge/API clients):** launch program with proxy env vars.

**Browser mode (Playwright):**
- Default to headless in non-GUI environments.
- If you see XServer/headed launch failure, retry once with headless.
- Use `browser_navigate` + `browser_snapshot` + interaction actions to produce traffic.

**Program mode (environment variables):**
Use temporary env vars when starting the target process:

```bash
HTTP_PROXY=http://127.0.0.1:18080 \
HTTPS_PROXY=http://127.0.0.1:18080 \
ALL_PROXY=http://127.0.0.1:18080 \
<your_program_command>
```

Or use helper script:

```bash
./scripts/runWithProxyEnv.sh -P 18080 -- <your_program_command>
```

Use `NO_PROXY` where necessary to bypass local endpoints.

**Exploration/Driving Strategies** (see [BROWSER_EXPLORATION.md](references/BROWSER_EXPLORATION.md)):

| Strategy | When | Actions |
|----------|------|---------|
| `full-crawl` | General analysis | Visit homepage → follow links → interact |
| `targeted-flow` | Specific user journey | Login → navigate → submit form → verify |
| `api-discovery` | API mapping | Visit pages, trigger AJAX, catalog endpoints |
| `performance-probe` | Performance | Rapid navigation, parallel requests |
| `manual-assist` | Complex scenarios | Start capture, let user operate, then analyze |

**Exploration Loop:**
```
1. Navigate to target URL
2. Take snapshot → analyze page structure
3. Identify interactive elements (links, buttons, forms)
4. Click/navigate based on strategy
5. Wait for network activity to settle
6. Repeat 2-5 for depth/breadth coverage
7. Record navigation path for report
```

### Phase 4: HARVEST (Stop & Process)

**AI executes:**
```bash
capture-session.sh stop
```

This triggers the full data pipeline:
```
capture.flow → HAR conversion
             → Index (NDJSON) + Summary (Markdown)
             → AI Brief (JSON + Markdown)
             → latest.* symlinks
```

**Output Files:**

| File | Format | Use |
|------|--------|-----|
| `*.flow` | mitmproxy binary | Raw immutable capture |
| `*.har` | HAR 1.2 JSON | Standard HTTP archive |
| `*.log` | Text log | Capture runtime diagnostics |
| `*.index.ndjson` | NDJSON | Per-request index records |
| `*.summary.md` | Markdown | Quick statistics overview |
| `*.ai.json` | JSON | Structured analysis input |
| `*.ai.md` | Markdown | AI-friendly brief |
| `*.ai.bundle.txt` | Text | Consolidated AI-ready bundle |
| `*.manifest.json` | JSON | Session metadata |
| `*.scope_audit.json` | JSON | Out-of-scope traffic report |
| `*.navigation.ndjson` | NDJSON | Browser navigation timeline/events |

### Phase 5: ANALYZE (Deep Analysis)

**AI reads and analyzes** the output files.

**Analysis Order:**
1. Read `latest.summary.md` — get the big picture
2. Read `latest.ai.json` — structured stats with findings
3. Drill into `latest.har` for specific requests (use Read tool with line offsets)
4. Cross-reference with navigation path from Phase 3

**Analysis Dimensions:**

#### Performance Analysis
- Identify p95/p99 latency outliers
- Group slow requests by endpoint
- Calculate time-to-first-byte patterns
- Identify sequential vs parallel request chains
- Detect unnecessary redirects

#### Security Analysis
- Check for missing security headers (CSP, HSTS, X-Frame-Options)
- Identify sensitive data in URLs (tokens, passwords in query strings)
- Detect mixed content (HTTP resources on HTTPS pages)
- Flag unencrypted API calls
- Identify CORS misconfigurations

#### Traffic Patterns
- Top hosts by request count
- Request method distribution
- Content type breakdown
- Error rate by endpoint
- Request size distribution

#### Debugging
- Isolate failed requests (4xx/5xx)
- Trace request chains (redirects, dependent calls)
- Compare request/response headers
- Identify missing or malformed responses

See [ANALYSIS_PATTERNS.md](references/ANALYSIS_PATTERNS.md) for detailed strategies.

## Quick Commands

### One-shot Analysis
User: "帮我分析 https://example.com 的网络请求"
→ AI runs all 5 phases automatically and selects browser/program/manual mode by task

### Manual Capture Mode
User: "开始抓包，我自己操作浏览器"
→ AI runs Phase 2, waits, then Phase 4-5 when user says "停止"

### Re-analyze Existing Capture
User: "分析 captures/ 目录下的抓包数据"
→ AI skips to Phase 5, reads existing files

### Compare Two Captures
User: "对比这两次抓包的差异"
→ AI reads two sets of data, generates comparison report

```bash
capture-session.sh diff captures/a.index.ndjson captures/b.index.ndjson
```

### Doctor Preflight
```bash
capture-session.sh doctor
```
Verify environment prerequisites before capture.

### Install/Dependency Diagnostics
```bash
./install.sh --check
./install.sh --doctor
```
Use this to diagnose runtime dependencies and current skill installation mode.

### Program Mode Helper
```bash
./scripts/runWithProxyEnv.sh -P 18080 -- <your_program_command>
```
Use this when traffic is produced by CLI/service process rather than browser automation.

### Browser Fallback Helper
```bash
./scripts/driveBrowserTraffic.sh --url https://example.com -P 18080 --mode auto
```
Use this when you want one-shot headed/headless fallback browser traffic generation.

### Localhost Start Example
```bash
capture-session.sh start http://localhost:3000
```
Use this when analyzing local web apps without TLS.

### Analyze Latest Capture
```bash
capture-session.sh analyze
```
Generate AI-ready analysis bundle from latest artifacts.

### Cleanup Command Examples
```bash
capture-session.sh cleanup --keep-days 7
capture-session.sh cleanup --keep-size 1G --dry-run
capture-session.sh cleanup --secure --keep-days 3
```
Use cleanup to control retention after analysis runs.

### Check Status
```bash
capture-session.sh status
```
Check whether capture process is running before stop/analyze.

### Help Command
```bash
capture-session.sh --help
```
Show command list and option reference quickly.

### Check Progress
```bash
capture-session.sh progress
```
Shows: duration, request count, data size

### Record Navigation Events
```bash
capture-session.sh navlog append --action navigate --url "https://example.com"
```
Use navlog during exploration to preserve key browser actions for later analysis.

## Report Template

See [templates/analysis-report.md](templates/analysis-report.md) for the output format.

Reports include:
- Executive summary (1-2 sentences)
- Key findings (prioritized list)
- Performance metrics table
- Security observations
- Detailed request analysis (top issues)
- Recommendations

## File Structure

```
fafafa-skills-capture-analytics/
├── SKILL.md                           # This file
├── skill-rules.json                   # Trigger configuration
├── references/
│   ├── CAPTURE_OPERATIONS.md          # Detailed capture operations
│   ├── ANALYSIS_PATTERNS.md           # Analysis strategies & patterns
│   └── BROWSER_EXPLORATION.md         # Playwright exploration guide
├── scripts/
│   ├── startCaptures.sh               # Start mitmproxy capture
│   ├── stopCaptures.sh                # Stop capture & process pipeline
│   ├── analyzeLatest.sh               # Generate AI analysis bundle
│   ├── ai.sh                          # Quick analysis entry point
│   ├── capture-session.sh             # One-shot capture session
│   ├── flow2har.py                    # Flow → HAR converter
│   ├── flow_report.py                 # Index & summary generator
│   ├── ai_brief.py                    # AI analysis brief builder
│   ├── cleanup.py                     # Cleanup policy helper
│   ├── common.sh                      # Shared shell helper functions
│   ├── doctor.sh                      # Environment diagnostics
│   ├── git-doctor.sh                  # Git environment diagnostics
│   ├── policy.py                      # Scope policy validator
│   ├── proxy_utils.sh                 # Proxy utility helpers
│   ├── release-check.sh               # Release verification helper
│   ├── runWithProxyEnv.sh             # Run command with proxy env (program mode)
│   ├── scope_audit.py                 # Scope audit report generator
│   ├── cleanupCaptures.sh             # Capture retention cleanup
│   ├── navlog.sh                      # Navigation log helper
│   └── diff_captures.py               # Capture index diff tool
└── templates/
    ├── analysis-report.md             # Report output template
    └── exploration-strategies.json    # Pre-built exploration configs
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `mitmdump: command not found` | `pip install mitmproxy` or install via system package manager |
| Port 18080 already in use | Use `-P <other-port>` flag or stop existing process |
| Playwright can't connect through proxy | Ensure mitmproxy CA cert is trusted, or use `--ignore-https-errors` |
| HAR conversion fails | Script falls back to Python converter automatically |
| Empty capture (0 requests) | Check proxy routing — use real browser/program traffic through proxy; smoke curl is connectivity-only |
| Found stale state file | Restart with `capture-session.sh start https://example.com --force-recover` |
| Permission denied on scripts | Run `chmod +x scripts/*.sh` |