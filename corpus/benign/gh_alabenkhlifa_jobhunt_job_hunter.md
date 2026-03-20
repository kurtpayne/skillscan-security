---
name: job-hunter
description: Automated job search agent for Gulf market (UAE/KSA).
  Scrapes LinkedIn and Foundit Gulf, scores matches against a
  Software Architect / Tech Lead profile, and notifies via Telegram.
triggers:
  - job search
  - find jobs
  - job hunt
  - new jobs
  - interested in job
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: alabenkhlifa/JobHunter
# corpus-url: https://github.com/alabenkhlifa/JobHunter/blob/4cbe3eb5fa6c3f6a057556d0d5fc6b971d93fe47/job-hunter.skill.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Job Hunter Skill

## Overview
This skill automates job searching for Software Architect / Cloud Architect /
Tech Lead roles in UAE and Saudi Arabia. It scrapes LinkedIn (guest API) and
Foundit Gulf (JSON API), scores matches using a weighted keyword system, and
sends notifications via Telegram.

## Architecture
- **Scraper**: `scraper.py` — scraping + CLI utilities (get-job, send-doc, send-msg, mark-interested)
- **Renderer**: `render_pdf.py` — dumb PDF renderer for resume and cover letter
- **Profile**: `data/master-profile.json` — master resume data (never fabricated)
- **Sources**: LinkedIn (guest HTML API), Foundit Gulf (JSON middleware API)
- **Storage**: SQLite for deduplication and history (with `status` column)
- **Notifications**: Telegram Bot API (HTML parse mode)
- **Designed for**: Raspberry Pi via cron (lightweight, no headless browser)

## Scraping Strategy
The scraper uses **breadth-first round-robin** across 4 buckets:
- LinkedIn/UAE, LinkedIn/Saudi, Foundit/UAE, Foundit/Saudi
- Collects **2 matching jobs per bucket** (12 total)
- Fetches page 1 of every keyword before going to page 2
- Evaluates jobs after each page fetch to stop early
- Scrapers are generators that yield one page at a time

### Search Keywords
- software architect, cloud architect, tech lead
- lead software engineer, platform architect, solutions architect

### Regions
- **UAE**: searches "UAE" and "Dubai"
- **Saudi**: searches "Saudi Arabia" and "Riyadh"

## Scoring System
Jobs are scored by matching keywords in title + company + full description:
- **High (+3)**: architect, aws, azure, spring boot, microservices, tech lead,
  team lead, java, kotlin, backend
- **Medium (+1)**: docker, ci/cd, kubernetes, terraform, cloud, .net,
  typescript, devops, infrastructure
- **Threshold**: score >= 13 to qualify as a match

## Filters (applied before scoring)
1. **Excluded titles**: test engineer, qa, staff software engineer, sdet,
   machine learning, ml engineer, ml architect
2. **Job age**: posted within last 7 days only
3. **Local presence**: skips jobs requiring existing UAE/Saudi residency or
   that won't sponsor visas
4. **Experience**: skips jobs requiring more than 8 years

## Job Enrichment
For each candidate job, the scraper fetches the full description and extracts:
- **Tech stack**: split into required vs nice-to-have (parsed from section headers)
- **Min experience**: regex extraction from description
- **Salary**: regex extraction (AED/USD/SAR amounts)
- **Work model**: remote / hybrid / on-site (signal phrase matching)
- **Score breakdown**: lists each matched term with its weight

## Workflow

### When triggered by cron (scheduled):
1. Run the scraper: `.venv/bin/python3 scraper.py`
2. Scraper iterates all 4 buckets breadth-first
3. For each new job passing all filters with score >= 13:
   - Saves to SQLite database
   - Sends Telegram notification with:
     - Job title (bold), company, country
     - Work model badge, score with stars
     - Posted age, experience requirement, salary
     - Score breakdown (matched terms)
     - Tech stacks (required vs nice-to-have)
     - Clickable "View Job" link and source
4. Messages are batched under 4000 chars, sorted by score descending

### When user replies "interested" for a job:
Openclaw (AI) handles the intelligent tailoring; scripts handle rendering and sending.

1. Get job details:
   ```bash
   python3 scraper.py --get-job <job_id>
   ```
   This prints the full job JSON (title, company, description, tech stacks, etc.)

2. Send progress message:
   ```bash
   python3 scraper.py --send-msg "<b>📝 Generating tailored resume and cover letter for:</b>
   <b><job_title></b> @ <company>

   ⏳ Analyzing job requirements..."
   ```

3. Read `data/master-profile.json` to get the full master profile

4. **AI tailoring** (this is the intelligent part openclaw does):

   **CRITICAL: The master-profile.json contains REAL data. Every company name, job title, date range, education entry, and certification is factual and must be preserved EXACTLY. You are tailoring, NOT rewriting.**

   What you MUST keep unchanged (copy verbatim from master profile):
   - All `company` names exactly as written
   - All `title` values exactly as written
   - All `dates` and `location` values exactly as written
   - All `education` entries exactly as written
   - All `certifications` exactly as written
   - The `name`, `email`, `phone`, `linkedin` fields exactly as written
   - The number of experience entries (keep ALL of them, never drop any)

   What you CAN adjust (minor refinements only):
   - **Skills ordering**: reorder the skill categories so the most relevant one for this job appears first
   - **Summary paragraph**: rewrite to emphasize aspects relevant to this job, but keep it grounded in the real experience from the master profile
   - **Experience bullets**: reword existing bullets to emphasize relevant keywords, but the core facts (what was built, what tech was used, what results were achieved) must stay truthful
   - **Experience order**: optionally reorder experience entries to lead with the most relevant one

   What you MUST NOT do:
   - Do NOT invent new companies, roles, or experiences
   - Do NOT change dates, titles, company names, or locations
   - Do NOT add skills or certifications not in the master profile
   - Do NOT remove any experience entries or education
   - Do NOT change the person's name, contact info, or education history

5. Write tailored resume JSON to a temp file (same structure as master-profile.json, but with reordered/adjusted content). **Start by copying the master profile JSON, then make only the adjustments above.**

6. Render resume PDF:
   ```bash
   python3 render_pdf.py resume <tailored_resume.json> data/Resume_Ala_BenKhalifa_<Company>.pdf
   ```

7. Write cover letter JSON to a temp file with this structure:
   ```json
   {
     "name": "Ala Ben Khalifa",
     "contact": "ala.khliifa@gmail.com | +216 56 829 196",
     "date": "<today's date>",
     "recipient": "Hiring Manager, <Company>",
     "subject": "Application for <Job Title>",
     "paragraphs": ["Dear Hiring Manager,\n\n...", "...", "Sincerely,\nAla Ben Khalifa"]
   }
   ```

8. Render cover letter PDF:
   ```bash
   python3 render_pdf.py cover <cover_letter.json> data/CoverLetter_Ala_BenKhalifa_<Company>.pdf
   ```

9. Send both PDFs:
   ```bash
   python3 scraper.py --send-doc data/Resume_Ala_BenKhalifa_<Company>.pdf
   python3 scraper.py --send-doc data/CoverLetter_Ala_BenKhalifa_<Company>.pdf
   ```

10. Send completion message:
    ```bash
    python3 scraper.py --send-msg "✅ Done! Here are your tailored documents:
    📄 Resume_Ala_BenKhalifa_<Company>.pdf
    📄 CoverLetter_Ala_BenKhalifa_<Company>.pdf

    Key adjustments made:
    - <list what was emphasized/reordered>
    - <which skills matched>
    - <what was highlighted in cover letter>

    Good luck! 🚀"
    ```

11. Mark job as interested:
    ```bash
    python3 scraper.py --mark-interested <job_id>
    ```

### When user asks "job stats" or "search status":
- Query SQLite database at `data/jobs.db`
- Report: total jobs found, new today, applied count,
  top matches pending review

## CLI Reference
```bash
# Normal scraping (cron mode)
python3 scraper.py

# Get job as JSON
python3 scraper.py --get-job <job_id>

# Send message via Telegram
python3 scraper.py --send-msg "<html message>"

# Send document via Telegram
python3 scraper.py --send-doc <file_path> [caption]

# Mark job as interested
python3 scraper.py --mark-interested <job_id>

# Render resume PDF
python3 render_pdf.py resume <input.json> <output.pdf>

# Render cover letter PDF
python3 render_pdf.py cover <input.json> <output.pdf>
```

## File Locations
- Scraper: `scraper.py`
- PDF renderer: `render_pdf.py`
- Master profile: `data/master-profile.json`
- Database: `data/jobs.db`
- Logs: `data/scraper.log`
- Config: `.env` (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
- Dependencies: `requirements.txt` (requests, beautifulsoup4, python-dotenv, lxml, fpdf2)

## Cron Setup (Raspberry Pi)
```bash
# One-time setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Edit with real values

# Daily at 8 AM
0 8 * * * cd /home/pi/JobScrapper && .venv/bin/python3 scraper.py >> data/cron.log 2>&1
```

## Resume Tailoring Rules (MANDATORY)
These rules are NON-NEGOTIABLE. Violating them produces a fraudulent resume.
- **NEVER fabricate** companies, job titles, dates, education, certifications, or skills
- **NEVER change** company names, job titles, date ranges, locations, or education entries — copy them verbatim from master-profile.json
- **NEVER drop** experience entries — all entries from the master profile must appear in the tailored version
- **ONLY adjust**: summary paragraph wording, skills category ordering, experience bullet emphasis/rewording, experience entry ordering
- **Bullet rewording** means highlighting relevant keywords that are already truthful — NOT inventing new accomplishments
- The tailored JSON must have the exact same structure as master-profile.json
- When in doubt, keep the original text unchanged