---
name: nexus-bdr-agent
description: >
  Full-cycle BDR prospecting agent for B2B terpene and botanical extract sales.
  Handles ICP-based lead discovery via Apollo.io, email enrichment via Hunter.io,
  AI-powered lead scoring and qualification, personalized multi-channel outreach
  generation, HubSpot CRM pipeline management, and automated follow-up scheduling.
  Use when the user asks to prospect, find leads, build lead lists, generate outreach,
  manage sales pipeline, qualify prospects, research companies, or automate BDR tasks.
version: 1.0.0
emoji: "🔬"
homepage: https://github.com/growthlegend/nexus-bdr-agent
metadata:
  openclaw:
    requires:
      env:
        - APOLLO_API_KEY
        - HUNTER_API_KEY
        - HUBSPOT_API_KEY
      bins:
        - python3
        - curl
      oneOf:
        - jq
    primaryEnv: APOLLO_API_KEY
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: LauchnerMedia/nexus-bdr
# corpus-url: https://github.com/LauchnerMedia/nexus-bdr/blob/252cd2181443c64592e45990096f7d1da9284bbf/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Nexus BDR Agent

Full-cycle Business Development Representative automation for Nexus Agriscience's two brands: **Terpene Belt Farms** (B2B premium botanical terpenes) and **Duty Free Terpenes** (edgy, anti-establishment terpene brand for extract artists and small producers).

This skill automates the entire BDR workflow: prospect research → lead discovery → enrichment → qualification → personalized outreach → CRM logging → follow-up orchestration.

## Brand Context

Load brand context from [references/brand-context.md](references/brand-context.md) before generating any outreach or qualifying any lead. The two brands serve different market segments and require different messaging tones.

### Terpene Belt Farms (TBF)
- **Positioning**: Premium, science-forward B2B botanical terpene supplier
- **Target**: Licensed cannabis manufacturers, CPG brands, food & beverage companies, cosmetics/skincare formulators, pharmaceutical R&D
- **Tone**: Professional, consultative, education-led
- **Key differentiators**: Livermore CA cultivation facility, organic practices, full-spectrum botanical profiles, compliance documentation, COAs on every batch

### Duty Free Terpenes (DFT)
- **Positioning**: Rebellious, direct-to-producer terpene brand for extract artists
- **Target**: Small-batch cannabis extractors, home processors, concentrate brands, vape manufacturers, hemp product makers
- **Tone**: Irreverent, anti-establishment, creator-to-creator
- **Key differentiators**: Same source material as TBF (premium quality), priced for small operators, strain-specific profiles, no minimums, fast shipping

## Trigger Phrases

Activate this skill when the user says any of the following (or similar):
- "prospect for [brand]" or "find leads for TBF/Duty Free"
- "build a lead list for [vertical/geography]"
- "research [company name] as a prospect"
- "generate outreach for [lead/company]"
- "qualify this lead" or "score these leads"
- "update the pipeline" or "log this to HubSpot"
- "what's the pipeline status" or "show me follow-ups"
- "run a prospecting cycle" or "daily prospecting"
- "break into [new market/vertical]"

## Core Workflows

### 1. Prospect Discovery (Apollo.io)

When the user asks to find leads or build a list:

1. Determine which brand the leads are for (TBF or DFT). If unclear, ask.
2. Load the appropriate ICP from [config/icp-profiles.json](config/icp-profiles.json).
3. Execute the Apollo search using [scripts/apollo_search.py](scripts/apollo_search.py):

```bash
python3 scripts/apollo_search.py \
  --icp "tbf_cannabis_manufacturers" \
  --max-leads 50 \
  --output "outputs/leads_$(date +%Y%m%d_%H%M).json"
```

4. Present results as a summary table: Company | Contact | Title | Location | Score
5. Ask user which leads to enrich and pursue.

**ICP Profiles Available** (see config/icp-profiles.json for full definitions):

| Profile ID | Brand | Target |
|---|---|---|
| `tbf_cannabis_manufacturers` | TBF | Licensed cannabis product manufacturers |
| `tbf_cpg_food_bev` | TBF | Food, beverage, and flavor companies |
| `tbf_cosmetics_pharma` | TBF | Cosmetics, skincare, and pharma R&D |
| `tbf_enterprise` | TBF | Large MSOs and national brands |
| `dft_extract_artists` | DFT | Small-batch extractors and concentrate makers |
| `dft_vape_manufacturers` | DFT | Vape cartridge and hardware brands |
| `dft_hemp_producers` | DFT | Hemp-derived product companies |
| `new_market_expansion` | Both | Non-cannabis verticals (aromatherapy, pet, wellness) |

### 2. Lead Enrichment (Hunter.io)

After Apollo returns leads:

1. For any lead missing a verified email, run Hunter enrichment:

```bash
python3 scripts/hunter_enrich.py \
  --input "outputs/leads_YYYYMMDD_HHMM.json" \
  --output "outputs/enriched_YYYYMMDD_HHMM.json"
```

2. Hunter will attempt email-finder for each contact using first_name + last_name + domain.
3. Confidence scores below 70% are flagged as "unverified" — do NOT include in outreach sequences.
4. Update the lead record with: hunter_email, confidence_score, email_verified (boolean).

### 3. Lead Qualification & Scoring

Score each lead 0-100 based on these weighted criteria:

| Signal | Weight | How to Assess |
|---|---|---|
| Title/seniority match | 25 | VP+, Director, Head of = high; Manager = medium; Coordinator = low |
| Company size fit | 20 | TBF: 50-5000 employees ideal. DFT: 1-100 employees ideal |
| Industry alignment | 20 | Cannabis, food & bev, cosmetics = high; adjacent = medium; unrelated = low |
| Geography | 15 | States with legal cannabis = high; emerging markets = medium; prohibited = low |
| Tech stack signals | 10 | Uses extraction equipment, has manufacturing facility = high |
| Engagement signals | 10 | Recent funding, hiring for R&D/production, new product launches = high |

**Scoring tiers:**
- **Hot (80-100)**: Immediate outreach. Route to Account Executive if they respond.
- **Warm (60-79)**: Include in outreach sequence. Nurture with educational content.
- **Cool (40-59)**: Add to long-term drip. Monitor for trigger events.
- **Cold (0-39)**: Do not pursue. Archive for future market expansion.

When scoring, use the LLM to analyze any available company context (website, LinkedIn, recent news) to assess fit. Use [scripts/company_research.py](scripts/company_research.py) for automated research:

```bash
python3 scripts/company_research.py \
  --company "Cookies" \
  --domain "cookiescalifornia.com"
```

### 4. Outreach Generation

Generate personalized outreach sequences using brand-specific templates from [references/outreach-templates.md](references/outreach-templates.md).

**Rules for outreach generation:**
- ALWAYS personalize based on company research. Never send generic templates.
- Reference something specific: recent product launch, funding round, job posting, industry challenge.
- TBF outreach leads with education and consultative value (send a relevant whitepaper, COA, or case study).
- DFT outreach leads with community and creator identity (reference their work, compliment their extracts).
- Keep initial email under 150 words. Subject lines under 8 words.
- Include ONE clear CTA: book a call, request samples, reply with questions.
- Never mention competitors by name in outreach.

**Sequence structure (per lead):**
1. **Day 0**: Personalized intro email
2. **Day 3**: LinkedIn connection request with note (if LinkedIn URL available)
3. **Day 7**: Follow-up email with value-add (article, resource, sample offer)
4. **Day 14**: Break-up email ("Closing the loop — is terpene sourcing on your radar?")
5. **Day 21**: Final touch — social engagement (like/comment on their content)

Generate all sequence steps at once. Store in [outputs/sequences/](outputs/sequences/) as individual markdown files per lead.

### 5. HubSpot CRM Management

Log all activity to HubSpot using [scripts/hubspot_sync.py](scripts/hubspot_sync.py).

**On lead discovery:**
```bash
python3 scripts/hubspot_sync.py create-contact \
  --first-name "Jane" \
  --last-name "Smith" \
  --email "jane@example.com" \
  --company "Cookies" \
  --title "VP of Manufacturing" \
  --source "apollo_outbound" \
  --lead-score 85 \
  --brand "tbf"
```

**On deal creation (when lead responds positively):**
```bash
python3 scripts/hubspot_sync.py create-deal \
  --contact-email "jane@example.com" \
  --deal-name "Cookies - TBF Terpene Supply" \
  --stage "introductory_meeting" \
  --pipeline "default"
```

**On deal stage update:**
```bash
python3 scripts/hubspot_sync.py update-deal \
  --deal-id 12345 \
  --stage "campaign_assessment"
```

**Pipeline stages** (mapped to HubSpot deal stages):
1. Introductory Meeting (first contact made)
2. Campaign Assessment (needs analysis)
3. Strategy Proposal (proposal/samples sent)
4. Strategy Presentation (presented to decision makers)
5. Objection Handling (negotiating terms)
6. Finalizing Terms (contract/PO stage)
7. Closed Won
8. Closed Lost

### 6. Follow-Up Orchestration

Track all pending follow-ups. When the user asks for follow-up status:

1. Read the follow-up schedule from [outputs/follow-ups.json](outputs/follow-ups.json)
2. Present overdue and today's follow-ups in priority order (Hot leads first)
3. For each follow-up due, draft the next touch in the sequence
4. After user approves, log the activity to HubSpot

**Daily briefing** (trigger: "daily prospecting" or via cron heartbeat):
```
📊 Pipeline Snapshot:
- X new leads discovered this week
- X leads in active sequences
- X follow-ups due today
- X follow-ups overdue

🔥 Hot Actions:
1. [Lead Name] — [Company] — [Next step] — Due [Date]
2. ...

📈 Weekly Metrics:
- Leads discovered: X
- Emails sent: X
- Reply rate: X%
- Meetings booked: X
- Deals created: X
```

### 7. Market Expansion Research

When the user asks to "break into" a new market or vertical:

1. Use the LLM + web research to identify:
   - Top 20 companies in the target vertical that could use botanical terpenes
   - Key decision-maker titles for that vertical
   - Common use cases for terpenes in that industry
   - Regulatory considerations
   - Messaging angle that resonates with that vertical
2. Create a new ICP profile and save to config/icp-profiles.json
3. Run the discovery workflow against the new ICP

## Rules

- **Never send outreach without user approval.** Always present drafts first.
- **Never delete or overwrite HubSpot data** without explicit confirmation.
- **Always check for existing contacts in HubSpot** before creating duplicates.
- **Respect rate limits**: Apollo (100 req/min), Hunter (15 req/sec), HubSpot (100 req/10sec).
- **Log every action** to outputs/activity-log.json with timestamp, action type, and result.
- **Cannabis compliance**: Never make health claims. Never reference THC content in outreach. Never target states where cannabis is fully prohibited for outreach about cannabis products (DFT hemp products are 50-state legal).
- **Data privacy**: Never share lead contact information outside of authorized CRM systems.
- If a lead has "Do Not Contact" or "Opted Out" status in HubSpot, NEVER include them in outreach.
- When in doubt about brand assignment, ask the user. Never guess.

## File Structure

```
nexus-bdr-agent/
├── SKILL.md                          # This file
├── config/
│   └── icp-profiles.json             # ICP definitions for Apollo queries
├── scripts/
│   ├── apollo_search.py              # Apollo.io lead discovery
│   ├── hunter_enrich.py              # Hunter.io email enrichment
│   ├── company_research.py           # Web research for lead qualification
│   └── hubspot_sync.py               # HubSpot CRM read/write
├── references/
│   ├── brand-context.md              # Full brand positioning for TBF + DFT
│   ├── outreach-templates.md         # Email/LinkedIn templates by brand + vertical
│   └── legal-states.md               # Cannabis legality by state (for targeting)
├── commands/
│   ├── prospect.md                   # /prospect slash command
│   ├── pipeline.md                   # /pipeline slash command
│   └── followups.md                  # /followups slash command
└── outputs/                          # Generated leads, sequences, reports
    ├── sequences/
    ├── follow-ups.json
    └── activity-log.json
```