---
name: vibe-code-health-check
description: >
  Scans any codebase and grades it A through F across 6 health dimensions
  (security, error handling, code structure, performance, deployment readiness,
  UX basics). Use when asked to "check my code", "audit my project",
  "is my code ready to ship", "review my codebase", "health check",
  "code quality check", "is my app secure", "vibe check my code",
  "scan my project", or "what is wrong with my code". Takes a codebase
  path and returns a scored report card with plain-English fixes.
license: MIT
metadata:
  author: tomer-ezri
  version: "1.0.0"
  category: development
  tags: [code-quality, security, audit, vibe-coding, health-check]
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: FuzulsFriend/vibe-code-health-check
# corpus-url: https://github.com/FuzulsFriend/vibe-code-health-check/blob/5690ba6a6c137054ab81d16871b4b71018dafad9/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Vibe Code Health Check

Get an honest health check of your codebase — graded A through F with plain-English fixes.

---

## Onboarding

### First-Time Detection

Ask: **"Have you used Vibe Code Health Check before?"**

If new user, show:

```
Welcome to Vibe Code Health Check!

I'll scan your codebase and grade it A through F across 6 dimensions:
security, error handling, code structure, performance, deployment
readiness, and user experience basics.

Everything is explained in plain English — not developer jargon.
You don't need to be a senior developer to understand the report.
```

### Startup Sequence (Tool Detection + Context Questions)

At the start of every run, do these **in parallel**:

**A. Background Tool Detection (run silently while asking questions):**

Search for these tools/MCPs without blocking the user:

| Tool | What it does | How to detect |
|------|-------------|---------------|
| Playwright CLI skill | Tests the app like a real user would | Check if `playwright-cli` commands are available |
| Chrome DevTools MCP | Console errors + page speed metrics | Check if `mcp__chrome-devtools__*` tools are available |

**B. Context Questions (ask immediately, don't wait for tool detection):**

1. **What does your app do?** (1 sentence)
2. **Is it deployed somewhere?** (URL, so I can test it live)
3. **Are you planning to launch this, or is it a side project?**

**Skip any question** where the answer is already known from Claude's memory, prior conversations, or information the user provided in their initial message. If ALL answers are already known, confirm them briefly and proceed.

**Wait for the user to answer all remaining questions before starting any analysis.**

These answers affect scoring — a side project and a production app have different readiness standards.

### Tool Detection Results (after background check completes)

Once background detection finishes AND user has answered context questions:

1. **If all recommended tools are available** → Announce tools and proceed to analysis.
2. **If some tools are missing** → Tell the user which tools are missing, what they enable, and ask:
   "Would you like help installing the missing tools? Or should I continue without them?"
   - **If yes** → Provide install commands one by one and guide them through setup:
     - Playwright CLI: `npx skills add lackeyjb/playwright-skill --skill playwright-skill`
     - Chrome DevTools: `claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest`
   - **If no** → Continue, but announce: "Proceeding without [tool]. The report may not cover [what's missing — e.g., 'live user testing' without Playwright]."

### Announce to User

```
Tools available: [list what was found]
Analysis mode: [full with live testing / code-only]
```

---

## Stack Auto-Detection

Before running any analysis, auto-detect the tech stack from config files:

| File | Stack Signal |
|------|-------------|
| package.json | Node.js / JavaScript project |
| next.config.* | Next.js |
| tsconfig.json | TypeScript |
| requirements.txt / pyproject.toml | Python |
| Gemfile | Ruby on Rails |
| go.mod | Go |
| Cargo.toml | Rust |
| .env / .env.example | Environment variables in use |
| supabase/ / firebase.json | BaaS integration |
| docker-compose.yml | Docker deployment |
| vercel.json / netlify.toml | Cloud deployment |

Report the detected stack to the user before starting analysis.

---

## Agent Teams Roles

When Agent Teams is enabled, run all 6 analyses in parallel:

| Role | Agent Name | Dimension |
|------|-----------|-----------|
| Orchestrator | main | Coordinates all agents, assembles final report, talks to user |
| Security Inspector | audit-security | Exposed secrets, unprotected routes, injection vulnerabilities |
| Error Handling Reviewer | audit-errors | Missing try/catch, unhandled promises, crash-prone code |
| Code Structure Analyst | audit-structure | File size, duplication, naming, organization |
| Performance Analyst | audit-performance | Bundle size, waterfall fetches, unoptimized assets |
| Deployment Checker | audit-deploy | Build pass/fail, env config, .gitignore coverage |
| UX Basics Reviewer | audit-ux | Loading states, error messages, mobile responsiveness |

**When Agent Teams is NOT available:** Run all 6 analyses sequentially in the main session. Same depth, just slower.

---

## The 6 Health Dimensions

| Dimension | Weight | What it checks (plain English) |
|-----------|--------|-------------------------------|
| Security | 25% | Are passwords/keys exposed? Can strangers access private data? Are there common attack holes? |
| Error Handling | 20% | What happens when something goes wrong? Does the app crash, or handle it gracefully? |
| Code Structure | 15% | Is the code organized? Are files too long? Is there copy-pasted code? |
| Performance | 15% | Does the app load fast? Are there unnecessary slowdowns? |
| Deployment Readiness | 15% | Can this actually be deployed? Does the build pass? Are settings configured? |
| UX Basics | 10% | Does the app show loading indicators? Error messages? Work on mobile? |

Scoring criteria: `references/scoring-rubric.md`

Stack-specific checks:
- React/Next.js: `references/react-nextjs-checks.md`
- Python/Flask/FastAPI: `references/python-flask-checks.md`
- Supabase/Firebase: `references/supabase-firebase-checks.md`
- Security patterns: `references/security-patterns.md`
- Error handling: `references/error-handling-rules.md`
- Performance: `references/performance-rules.md`

---

## Analysis Flow

### Phase 1: CODEBASE SCAN (automatic, always runs)

1. Auto-detect stack from config files (see table above)
2. Map file structure and entry points
3. Count: total files, lines of code, dependencies
4. Identify: framework, language, deployment target
5. Report findings to user before deep analysis
6. Check for project-level config/rules files (CLAUDE.md, .eslintrc, AGENTS.md, CONTRIBUTING.md, .cursorrules). If they define rules or bans (e.g., 'never use transition-all', 'always use date-fns alternative'), add these as custom checkpoints. Compliance with the project's OWN rules is a free quality signal.

### Phase 2: DIMENSION ANALYSIS

Run all 6 dimension analyses (parallel if Agent Teams, sequential otherwise).

Each dimension analysis must:
1. Score 0-100 based on checkpoints in `references/scoring-rubric.md`
2. Apply stack-specific checks from the relevant reference file
3. Record specific findings in this format:

```
FINDING: [what's wrong — plain English, no jargon]
IMPACT: [why this matters for users/business]
FIX:    [specific action to take, with file path and line if possible]
EFFORT: [quick fix (under 30 min) / few hours / redesign needed]
```

### Phase 3: BUILD VERIFICATION (always runs if build tool detected)

1. Run actual build command (npm run build, python -m py_compile, etc.)
2. Run type checker (npx tsc --noEmit if TypeScript)
3. Run npm audit / pip audit for known vulnerable packages
4. Report build errors in plain English
5. Flag warnings that should be fixed before launch

### Phase 4: LIVE TESTING (if Playwright available AND URL provided)

1. Open the app in a browser
2. Try the main user flow (signup/login/main action)
3. Test on mobile viewport (375px)
4. Check for console errors
5. Screenshot key pages
6. Report: "As a real user, here's what I experienced..."

### Phase 5: GRADE AND REPORT

1. Collect all 6 dimension scores
2. Apply weights to calculate total score (0-100)
3. Assign letter grade using the scale below
4. Rank findings by severity: Critical, Warning, Suggestion
5. Generate report in plain English
6. Output using the format in `assets/report-template.md`

---

## Grading Scale

| Grade | Score | What it means |
|-------|-------|--------------|
| A | 90-100 | Production-ready. Ship it. |
| B | 80-89 | Almost there. Fix the warnings and you're good. |
| C | 70-79 | Functional but risky. Fix critical issues before users see it. |
| D | 60-69 | Significant problems. Needs work before it's safe to deploy. |
| F | Below 60 | Not ready. Major security or stability issues. |

See `references/grade-thresholds.md` for detailed grade descriptions.

---

## Output Format

```
VIBE CODE HEALTH CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Project: [PROJECT_NAME]
Stack: [DETECTED_STACK]
Files: [COUNT] | Lines: [COUNT] | Dependencies: [COUNT]

Overall Grade: [GRADE] ([SCORE]/100)

BREAKDOWN:
  Security:            [BAR]  [SCORE]/100  [!! if critical]
  Error Handling:      [BAR]  [SCORE]/100  [!! if critical]
  Code Structure:      [BAR]  [SCORE]/100
  Performance:         [BAR]  [SCORE]/100
  Deploy Readiness:    [BAR]  [SCORE]/100
  UX Basics:           [BAR]  [SCORE]/100

CRITICAL — Fix these before anyone uses your app:

1. "[ISSUE — plain English]"
   Fix: [SPECIFIC_ACTION with file path]
   Effort: [TIME]

WARNINGS — Fix these soon:

2. "[ISSUE — plain English]"
   Fix: [SPECIFIC_ACTION]
   Effort: [TIME]

SUGGESTIONS — Nice to have:

3. ...

YOUR PATH FROM [CURRENT] TO [NEXT_GRADE]:
1. [STEP] ([DIMENSION]: [CURRENT] -> [PROJECTED])
2. [STEP] ([DIMENSION]: [CURRENT] -> [PROJECTED])
3. [STEP] ([DIMENSION]: [CURRENT] -> [PROJECTED])
Estimated time: [TOTAL]
Expected new grade: [PROJECTED] ([SCORE]/100)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Checked by Vibe Code Health Check — By Tomer & Guy
github.com/FuzulsFriend
```

See `assets/report-template.md` for the full template with all fields.

### Phase 5.5: USER REVIEW (before visual report)

After completing the text report (Phase 5), present it to the user and ask:

**"Here's the full health check. Would you like to change anything, or should I generate the visual report?"**

Wait for the user's response:
- **If user requests changes** → Apply the changes to scores/findings/recommendations, update the text report, and ask again.
- **If user approves** → Proceed to Phase 6 (visual report generation).
- **If user says nothing specific** → Treat as approval and proceed to Phase 6.

### Phase 6: VISUAL REPORT (browser preview)

Generate a self-contained HTML report and open it in the user's browser.

1. Create a JSON object with all health check data (see schema below)
2. Read the HTML template from `assets/report-ui.html`
3. Replace `{{REPORT_DATA}}` with the JSON string
4. Save to `./code-health-check-[project-name]-[date].html`
5. Open in browser: `open` (macOS), `xdg-open` (Linux), `start` (Windows)
6. Tell the user: "Visual report saved to [path] and opened in your browser."

JSON schema for the report:
```json
{
  "meta": {
    "projectName": "string",
    "stack": ["string"],
    "files": 0,
    "lines": 0,
    "dependencies": 0,
    "date": "YYYY-MM-DD",
    "mode": "full with live testing|code-only",
    "toolsUsed": ["string"],
    "isProduction": true
  },
  "overall": {
    "score": 0,
    "grade": "string"
  },
  "dimensions": [
    { "name": "Security", "score": 0, "weight": 0.25, "critical": false },
    { "name": "Error Handling", "score": 0, "weight": 0.20, "critical": false },
    { "name": "Code Structure", "score": 0, "weight": 0.15, "critical": false },
    { "name": "Performance", "score": 0, "weight": 0.15, "critical": false },
    { "name": "Deploy Readiness", "score": 0, "weight": 0.15, "critical": false },
    { "name": "UX Basics", "score": 0, "weight": 0.10, "critical": false }
  ],
  "build": {
    "passed": true,
    "command": "string",
    "errors": ["string"],
    "warnings": ["string"]
  },
  "findings": {
    "critical": [
      { "title": "string", "description": "string", "fix": "string", "file": "string", "effort": "string" }
    ],
    "warnings": [
      { "title": "string", "description": "string", "fix": "string", "file": "string", "effort": "string" }
    ],
    "suggestions": [
      { "title": "string", "description": "string", "fix": "string", "file": "string", "effort": "string" }
    ]
  },
  "stats": {
    "consoleLogCount": 0,
    "oversizedFiles": [{ "path": "string", "lines": 0 }],
    "selectStarCount": 0,
    "rawImgCount": 0,
    "todoCount": 0
  },
  "improvement": {
    "currentGrade": "string",
    "nextGrade": "string",
    "steps": [
      { "action": "string", "dimension": "string", "currentScore": 0, "projectedScore": 0, "time": "string" }
    ],
    "estimatedTime": "string",
    "projectedScore": 0,
    "projectedGrade": "string"
  },
  "liveTest": {
    "performed": false,
    "url": "string",
    "observations": ["string"],
    "consoleErrors": ["string"]
  }
}
```

---

## Report Language Rules

Write every finding in simple English. The user may not be a developer.

**DO:**
- "Your database password is written directly in the code — anyone who sees the code gets full access"
- "12 places in your code fetch data but don't handle what happens if the server is down"
- "On phones, the text is too small to read without zooming in"

**DON'T:**
- "Database credentials are hardcoded in plaintext without environment variable abstraction"
- "12 async functions lack try/catch blocks for error propagation"
- "Font-size below 16px on mobile viewport causes accessibility violations"

Tone: Like a senior dev friend reviewing your code — honest and direct, but always helpful.

---

## Severity Classification

| Severity | When to use | Examples |
|----------|-------------|---------|
| CRITICAL | Security holes, data exposure, crashes | Exposed API keys, SQL injection, unprotected admin routes |
| WARNING | Bugs waiting to happen, poor UX | No error handling on API calls, no loading states, large bundle |
| SUGGESTION | Code quality improvements | Long files, unused imports, inconsistent naming |

---

## Troubleshooting

**"Skill can't read my files"**
Make sure the skill has access to the project directory. If using a remote repo, clone it locally first.

**"Build failed"**
That's actually a finding — the report will include the build errors as critical issues with fixes.

**"Score seems too low"**
The audit is strict on purpose — especially for security. A score of 70 means the app works but has real risks. Fix the critical issues and the score jumps significantly.

**"Score seems too high"**
The audit checks what's IN the code, not what's missing from the business logic. Clean code with wrong business logic will still score well on code health.

**"I don't understand a finding"**
Every finding should be in plain English. If one slips through with jargon, ask for clarification and the skill will rephrase it.