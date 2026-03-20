---
description: "Run targeted smoke tests. Usage: /smoke-test [scope]. Scope can be: a description of what to test ('the payment system', 'the changes I just made'), a file path, or 'all' for a full suite. If no scope given, asks the user what to test."
name: smoke-test
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: tshades/smoke-test-kit
# corpus-url: https://github.com/tshades/smoke-test-kit/blob/5d0d3d852c3fc622d1338fe88819231746684984/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Smoke Test Skill

You are an autonomous QA testing agent. You run **targeted, scoped tests** — not everything every time.

## Project Config

<!-- ✏️ UPDATE THESE FOR YOUR PROJECT -->
- **Dev server command**: `npm run dev`
- **Dev server port**: `5173`
- **Dev server ready signal**: `"ready"` or `"Local:"`
- **Login required**: yes
- **Login URL**: `/login`
- **Login email field**: `input[type="email"]`
- **Login password field**: `input[type="password"]`
- **Login submit button**: `button[type="submit"]`
- **Test user email**: `test@yourapp.com`
- **Test user password**: `testpass123`
- **App entry point**: `src/App.jsx`
- **Services directory**: `src/services/`
- **Config directory**: `src/config/`

## ⚠️ CRITICAL: Tool Selection — Playwright MCP

Use **Playwright MCP** (`mcp__playwright__*`) for all browser interaction.

### Primary tools (use these for all assertions)

| Action | Tool | Notes |
|--------|------|-------|
| Navigate | `browser_navigate` | Go to URLs |
| Read page structure | `browser_snapshot` | **Accessibility tree** — use for ALL structural/content assertions |
| Click | `browser_click` | Pass `ref` from snapshot. Always include `element` description |
| Type text | `browser_type` | Pass `ref` from snapshot |
| Fill form | `browser_fill_form` | Fill multiple fields at once |
| Run JS in page | `browser_evaluate` | For logic tests via dynamic `import()` |
| Console logs | `browser_console_messages` | Check for runtime errors. Use `level: "error"` to filter |
| Network requests | `browser_network_requests` | **Always save to file** — see network rules below |

### Screenshot rules (visual checks ONLY)

Use `browser_take_screenshot` **only** for these specific cases:
- **Layout/CSS verification** — checking spacing, alignment, overflow, visual regressions
- **Canvas/SVG rendering** — charts, animations that have no accessibility tree representation
- **Asset loading** — confirming images/icons rendered (not broken placeholders)
- **Z-index/overlay issues** — modals, dropdowns visually layered correctly

**After every screenshot:**
1. Analyze it for the visual check you need
2. **Immediately delete the file** using Bash: `rm <filename>`
3. Never accumulate screenshot files

**NEVER use screenshots for structural assertions** (element presence, text content, navigation state). Use `browser_snapshot` for those — it's faster, deterministic, and returns refs you can interact with.

### Network request rules (avoid token overflow)

Dev servers generate thousands of network requests (HMR, module loads, etc.). **Never call `browser_network_requests` without saving to a file** — the raw output will exceed token limits.

**For network health checks**, use `browser_evaluate` instead:
```js
async () => {
  const entries = performance.getEntriesByType('resource');
  const failed = entries.filter(e => e.responseStatus >= 400);
  return { total: entries.length, failed: failed.map(e => ({ url: e.name, status: e.responseStatus })) };
}
```

**If you must use `browser_network_requests`**, always pass `filename` to save to a temp file, then grep for errors, then delete:
```
browser_network_requests(includeStatic: false, filename: "/tmp/smoke-net.txt")
→ Bash: grep -i "error\|fail\|[45][0-9][0-9]" /tmp/smoke-net.txt
→ Bash: rm /tmp/smoke-net.txt
```

## Step 1: Determine Scope

Parse the user's command for a testing scope:

- **No scope** (`/smoke-test` alone) → Ask the user: "What should I test? Options: a specific area (e.g., 'billing', 'navigation'), recent changes, or 'all' for the full suite."
- **Specific area** (`/smoke-test the payment system`) → Focus on files and UI related to that area
- **Recent changes** (`/smoke-test the changes you just made`) → Use `git diff --name-only HEAD~1` and `git diff --name-only` to find changed files, test only those and their related UI
- **File path** (`/smoke-test src/utils/calculator.js`) → Test that specific file's exports
- **`all`** (`/smoke-test all`) → Full suite: all UI views + all discoverable logic + console/network

## Step 2: Start Dev Server & Authenticate

### Start the dev server

Run the dev server in the background using Bash (use the command from **Project Config** above):
```bash
npm run dev &
```
Wait a few seconds for the server to be ready (check output for the ready signal from config).

### Authenticate (if login required)

Check the **Project Config** above. If `Login required: no`, skip this section.

If login is required:

1. `browser_navigate` to `http://localhost:{port}{login URL}` (use port and login URL from config)
2. `browser_snapshot` — confirm you see the login form
3. `browser_fill_form` with the email and password fields (use selectors and credentials from config)
4. `browser_click` the submit button (find its `ref` in the snapshot)
5. Wait briefly, then `browser_snapshot` — confirm you see the app's main UI, NOT the login form
6. If login fails, `browser_console_messages` to check for errors and report the issue

**Do NOT skip authentication if it's required.** UI tests will not work without logging in first.

## Step 3: Load Test Specs

Read `tests/smoke-tests.md` — this is the **registry** (index of all spec files). It maps spec files to source files/areas.

For the current scope:
1. Read the registry to find which spec file(s) match your scope
2. Read only the matching `tests/specs/*.md` file(s) — don't read them all
3. If the registry has specs covering your scope, run those tests first before discovering new ones

## Step 4: Discover & Generate Tests (for scope)

Only scan files relevant to the scope:

### For UI scopes
- Read the app entry point (from config) for views/routes matching the scope
- Read the relevant component files
- Test: navigation to the view, snapshot assertions, console error check

### For logic scopes
- Read the relevant files in the services/config directories (from config)
- Find `export function` and `export const` — testable public APIs
- Generate test cases: normal input, edge cases (empty/null/undefined), boundary conditions
- Skip functions needing WebSocket, mic, or API keys — note as skipped

### For "recent changes" scope
- Get changed files from git diff
- For each changed `.js`/`.jsx`/`.ts`/`.tsx` file:
  - If it's a service/config/util: test its exports
  - If it's a component: navigate to its view, check rendering + console
  - If it's a hook: check if it's used in a component, test that component's view

## Step 5: Run Tests → Fix → Retest (The Loop)

**This is the core behavior. You ALWAYS loop until all tests pass or you hit the attempt limit. You never just report failures and stop.**

### How the loop works

```
┌─────────────────────────────────┐
│  Run all tests for scope        │
└──────────────┬──────────────────┘
               │
       ┌───────▼───────┐
       │ All passed?    │──── YES ──→ Save to library, report success
       └───────┬────────┘
               │ NO
       ┌───────▼───────────────────┐
       │ Attempt < 5?              │──── NO ──→ Report remaining failures
       └───────┬───────────────────┘
               │ YES
       ┌───────▼───────────────────┐
       │ Read the error/failure    │
       │ Diagnose root cause       │
       │ Edit the source code fix  │
       │ Wait for hot-reload       │
       │ Re-run ONLY failed tests  │
       └───────┬───────────────────┘
               │
               └──→ (back to "All passed?")
```

### Running tests

**UI Tests**: `browser_snapshot` → find ref → `browser_click` → `browser_snapshot` → `browser_console_messages`

**Visual Tests** (layout, canvas, assets): `browser_take_screenshot` → analyze → `rm` the file immediately

**Logic Tests**: `browser_evaluate` to import and call functions in the page context:
```js
async () => {
  const mod = await import('/src/services/fileName.js');
  const results = {};
  results.test1 = { passed: mod.fn('input') === 'expected', actual: mod.fn('input'), expected: 'expected' };
  return results;
}
```
Note: The function receives no arguments. Access the page via the global scope.

**Console & Network**: `browser_console_messages` with `level: "error"` + `browser_evaluate` with Performance API (see network rules above)

### Fixing failures

When a test fails:
1. **Read the error** — what's the actual vs expected? Any console errors?
2. **Read the source file** — understand the code that's broken
3. **Check docs if needed** — if the fix involves a third-party library or API call (not plain JS logic), look up correct usage via Context7 MCP (`resolve-library-id` → `query-docs`) or web search before editing. Skip this for simple logic fixes.
4. **Fix it** — edit the source file directly
5. **Wait for hot-reload** — pause briefly for the dev server to rebuild, then re-snapshot
6. **Re-run only the failed test** — don't re-run passing tests

### Attempt limits
- **5 fix attempts max** per test. If a single test still fails after 5 tries, mark it as unresolved and move on.
- **Do not loop infinitely.** If the same fix keeps failing, it likely needs human judgment — report what you tried and why it's still failing.

## Step 6: Save New Tests to Spec Files

**After the loop completes, save any NEW passing tests to the appropriate spec file in `tests/specs/`.**

### If a spec file exists for the source
Append new test sections to the existing `tests/specs/<name>.md` file. Add `(auto-generated YYYY-MM-DD)` to the section heading.

### If no spec file exists
1. Create a new `tests/specs/<sourceFileName>.md` (e.g., `tests/specs/calculator.md`)
2. Add a row to the registry table in `tests/smoke-tests.md`

### Format
```markdown
## Section Name (auto-generated YYYY-MM-DD)
\`\`\`js
// Description of what's being tested
functionName(input) === expectedOutput
\`\`\`
```

Do NOT duplicate tests already in the spec file. Do NOT save tests that failed and were never fixed.

## Step 7: Clean Up & Report Results

### Clean up
- Delete any remaining screenshot files: `rm -f *.png *.jpeg` in the project root
- Stop the dev server if you started one: kill the background process

### Report
```
SMOKE TEST RESULTS
================================
Scope: [what was tested]
Tests: [N from library, M newly generated]
Fix cycles: [how many loops it took]

  [PASS] calculator.add — 4/4 cases
  [PASS] Navigation to Settings view — renders, no errors
  [FIXED] validator.isEmail — false positive on "foo@" (fixed in cycle 2: added domain check)
  [SKIP] apiClient.fetchUser — requires API key
  [UNRESOLVED] someFunction — failed after 5 attempts (needs human review)

SUMMARY: X passed, Y fixed, Z skipped, W unresolved
```

For fixed tests: what was wrong and what the fix was.
For unresolved: what was tried and why it didn't work.

## Rules

- **`browser_snapshot` for ALL structural assertions** — element presence, text content, navigation state. Never screenshots for these.
- **Screenshots for visual checks only** — layout, canvas, assets, z-index. Delete immediately after use.
- **ALWAYS loop until passing** — finding failures and stopping is not acceptable. Fix them.
- **Always ask for scope** if none given — never run the full suite unprompted
- **Check console after every navigation** — error-level = failure
- **Reuse library tests** before generating new ones — avoid duplicate work
- **Save passing tests** to the spec files — the library grows smarter over time
- **Skip gracefully** — auth/WebSocket/mic-dependent = skip with note
- **Be efficient** — test what's in scope, nothing more
- **Know when to stop** — 5 attempts on one test, then report and move on
- **Clean up** — no leftover screenshot files, no orphaned dev server processes