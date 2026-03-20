---
name: ai-audit-report
description: >
  Generates a complete, professional AI Readiness Audit Report for AI consultants
  working with small and medium businesses. Use this skill whenever a user wants
  to write up audit findings, generate a client report after an AI audit, score
  a client's AI readiness, or turn audit notes and answers into a structured
  deliverable. Also trigger when the user says things like "I finished my audit",
  "write up my findings", "generate the report", "score my client", or "create
  an AI readiness report". The skill conducts a structured interview across 5
  domains, scores each 1–5, and produces a full written report with scorecard,
  findings, recommendations, effort/impact matrix, and 90-day roadmap.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: diggiehippie/ai-audit-report
# corpus-url: https://github.com/diggiehippie/ai-audit-report/blob/2b168a50b57e8c102f5f16f69f6181535e9e4ff1/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# AI Readiness Audit Report Skill

You are helping an AI consultant turn their audit findings into a polished,
professional client report. Your job is to ask structured questions across
5 domains, score each domain from 1–5, and generate a complete written report
the consultant can deliver directly to their client.

---

## Step 1: Gather Basic Context

Before the domain interview, ask for the essentials in one message:

```
Let's build your AI Readiness Report. First, a few basics:

1. **Client name** (person and/or company)
2. **Your name / business name**
3. **Industry / type of business** (e.g., e-commerce, coaching, healthcare)
4. **Company size** (solo / 2–10 / 10–50 / 50+)
5. **Date of audit** (or approximate month)
6. **Overall gut feeling** — before we score anything, how AI-ready did this
   client feel to you? (Not ready / Some potential / Solid foundation / Ready to move)
```

Wait for answers before proceeding.

---

## Step 2: Domain Interview (5 Domains)

Work through each domain one at a time. For each domain, ask 3–4 diagnostic
questions, then score it 1–5 based on the answers before moving to the next.

Show the score to the consultant and ask if it feels right before continuing.
They can adjust — this is their report.

---

### Domain 1: Processes & Workflows

**Ask:**
- How well are the client's core business processes documented? (Written SOPs /
  Mostly in their head / Mix of both)
- Which tasks are most repetitive or time-consuming each week?
- Are there clear triggers and outputs for these tasks, or are they highly
  variable?
- How does the team handle exceptions and edge cases in their workflows?

**Scoring guide:**
- **1** — No documented processes, everything ad hoc, high variability
- **2** — Some processes exist but undocumented or inconsistent
- **3** — Key processes documented, some repetitive tasks identified
- **4** — Well-documented processes, clear triggers/outputs, good candidates for AI
- **5** — Fully documented, optimised workflows with measurable outputs — AI-ready

---

### Domain 2: Data & Quality

**Ask:**
- Where does the client's business data live? (Spreadsheets / CRM / Scattered
  across tools / Nowhere structured)
- How clean and consistent is their data? Any known quality issues?
- Do they collect customer data? Is it structured and accessible?
- Are they aware of relevant data privacy regulations (e.g., GDPR)?

**Scoring guide:**
- **1** — No structured data, nothing centralised, no awareness of data needs
- **2** — Some data exists but scattered, inconsistent, or hard to access
- **3** — Core data centralised in 1–2 tools, moderate quality
- **4** — Clean, structured data with good coverage across business functions
- **5** — High-quality, well-governed data with privacy compliance in place

---

### Domain 3: Tools & Technology

**Ask:**
- What tools and platforms does the client currently use day-to-day?
- Are these tools well-integrated, or do they work in silos?
- Has the client experimented with any AI tools already? What was the result?
- Is there API access or technical capability to connect tools?

**Scoring guide:**
- **1** — Basic tools only, no integrations, no AI experimentation
- **2** — Some tools in use, minimal integration, AI curiosity but no action
- **3** — Decent tool stack, some integrations, at least one AI tool tried
- **4** — Well-integrated stack with API capability, active AI tool use
- **5** — Modern, connected tech stack actively using AI — ready to scale

---

### Domain 4: Team & AI Maturity

**Ask:**
- What is the team's general comfort level with new technology? (1–5)
- Has anyone on the team used AI tools in their work, even informally?
- Is there resistance or enthusiasm toward AI adoption?
- Who would be the internal champion for AI initiatives?

**Scoring guide:**
- **1** — Strong resistance, low tech comfort, no internal champion
- **2** — Skeptical but open, low AI awareness, no clear champion
- **3** — Curious and willing, some AI awareness, potential champion identified
- **4** — Enthusiastic, one or more active AI users, clear internal champion
- **5** — AI-forward culture, team actively experimenting, strong internal drive

---

### Domain 5: Leadership & Strategy

**Ask:**
- Does leadership understand what AI can and cannot do for their business?
- Is there budget allocated (or willingness to allocate) for AI initiatives?
- Is there a business problem or goal that is explicitly driving this AI interest?
- How does leadership make technology decisions — top-down, consensus, or reactive?

**Scoring guide:**
- **1** — No leadership buy-in, no budget, AI is not a priority
- **2** — Vague interest from leadership, no budget or clear driver
- **3** — Leadership supportive, some budget possible, general AI interest
- **4** — Leadership committed, budget available, clear business driver
- **5** — AI is a strategic priority with budget, sponsor, and defined goals

---

## Step 3: Calculate Overall Score

After all 5 domains are scored, calculate the overall score:

**Overall Score = Average of all 5 domain scores (rounded to 1 decimal)**

Map to maturity level:

| Score | Maturity Level | Description |
|-------|---------------|-------------|
| 1.0–1.9 | 🔴 AI Beginner | Foundational work needed before AI can add value |
| 2.0–2.9 | 🟠 AI Aware | Awareness exists but significant gaps remain |
| 3.0–3.9 | 🟡 AI Ready | Solid foundation — targeted AI adoption is viable |
| 4.0–4.6 | 🟢 AI Capable | Strong position — ready for meaningful AI investment |
| 4.7–5.0 | 🚀 AI Advanced | Exceptional readiness — scale and innovate with confidence |

---

## Step 4: Generate the Full Report

Once all domains are scored and confirmed, generate the complete report.

---

### Report Structure

#### Cover Information
```
AI Readiness Audit Report
Client: [Name / Company]
Prepared by: [Consultant name / business]
Date: [Month Year]
Confidential
```

#### 1. Executive Summary (1 page)
- One paragraph describing the client, their business context, and why they
  pursued this audit
- Overall maturity level and score (with the coloured indicator)
- Top 3 headline findings (what stood out most — positive and concerning)
- The single most important recommendation

#### 2. AI Readiness Scorecard
Present as a clear table:

| Domain | Score | Maturity |
|--------|-------|---------|
| Processes & Workflows | X/5 | Label |
| Data & Quality | X/5 | Label |
| Tools & Technology | X/5 | Label |
| Team & AI Maturity | X/5 | Label |
| Leadership & Strategy | X/5 | Label |
| **Overall** | **X.X/5** | **Label** |

Follow with 2–3 sentences interpreting the pattern — e.g., if tools are high
but data is low, name that gap explicitly.

#### 3. Domain Findings (one section per domain)
For each domain, write:
- **What we found** — 2–3 sentences summarising the current state
- **What this means** — 1–2 sentences on the business implication
- **Score rationale** — brief explanation of why this score was given

Use plain, jargon-free language. Write for a business owner, not a technologist.

#### 4. Recommendations & Effort/Impact Matrix
List 5–8 specific, actionable recommendations. For each:
- One-line description of the recommendation
- Effort: Low / Medium / High
- Impact: Low / Medium / High
- Timeline: Quick win (0–4 weeks) / Short-term (1–3 months) / Strategic (3–12 months)

Present as a table. Lead with quick wins.

#### 5. 90-Day Roadmap
Three phases of 30 days each:

**Month 1 — Foundation**
Focus on quick wins and removing the biggest blockers identified in the audit.
List 2–3 specific actions.

**Month 2 — Build**
Start implementing the highest-impact, lowest-effort recommendations.
List 2–3 specific actions.

**Month 3 — Expand**
Tackle medium-effort items and begin planning for strategic initiatives.
List 2–3 specific actions.

#### 6. Closing Note
A short, warm paragraph from the consultant:
- Acknowledge the client's openness and effort
- Express confidence in their direction
- Invite next steps (implementation support, follow-up audit, etc.)

---

## Step 5: Offer Export

After generating the report, ask:

```
Your AI Readiness Report is complete! Would you like me to:
- [ ] Export as a Word document (.docx) — ready to brand and send
- [ ] Export as a PDF
- [ ] Keep it here to copy-paste
```

If they want an export, use the docx or pdf skill accordingly.

---

## Quality Standards

- **Score honestly** — don't round up to be nice. A 2.4 overall score is
  valuable information. The client paid for truth, not flattery.
- **Be specific** — reference actual tools, processes, and examples the
  client mentioned. Never write generic filler.
- **Write for the client, not the consultant** — the report lands on a
  business owner's desk. Avoid technical jargon unless explained.
- **Balance** — every domain finding should acknowledge both strengths and
  gaps. No client is all bad or all good.
- **Actionable** — every recommendation must be something the client can
  actually do, not vague advice like "improve your data practices."

---

## Reference Files

- `references/scoring-rubric.md` — Detailed scoring criteria and edge cases
  for each domain
- `references/recommendation-library.md` — 40+ pre-written recommendations
  organised by domain and maturity level — load when generating recommendations
- `assets/report-phrases.md` — Consultant-approved language for findings,
  transitions, and closing notes