---
name: jira-tempo
description: "Parse a Jira activity RSS/Atom feed and estimate hours spent per Jira ticket per day. Use this skill when the user wants to: (1) extract activity events (date, ticket, action, description) from a Jira activity feed file into a structured CSV, (2) estimate time spent per ticket based on activity volume and type, or (3) prepare a time-tracking report from Jira activity for Tempo or similar timesheet tools. Expects activity.txt downloaded from the Jira activity stream API."
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: sanderch/jira-tempo-skill
# corpus-url: https://github.com/sanderch/jira-tempo-skill/blob/4a94b716b585b45ed0c06f244e8a05360a5e28b1/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Jira Tempo

Parse a Jira activity feed into structured CSVs, then estimate hours spent per ticket per day.

## Setup

The input file `activity.txt` is the raw Jira activity RSS/Atom feed. The easiest way to get it is directly from the browser:

1. Log in to Jira in your browser.
2. Open this URL (replace `<your-jira-domain>` and `<username>`):
   ```
   https://<your-jira-domain>/activity?maxResults=500&streams=user+IS+<username>&os_authType=basic
   ```
3. The browser will display raw XML. Save the page as `activity.txt` (File → Save As → All Files / Plain Text) in the repo folder.

Alternatively, use curl:

```bash
curl -u <username>:<password> -o activity.txt \
  "https://<your-jira-domain>/activity?maxResults=500&streams=user+IS+<username>&os_authType=basic"
```


## Workflow

### Step 1 — Parse the feed

```bash
python scripts/parse_activity.py [input] [output]
# Defaults: activity.txt -> activity_parsed.csv
```

Outputs one row per activity event: `date`, `ticket`, `title`, `activity_type`, `description`.

Activity types: `Created`, `Updated`, `Commented`, `Status -> <name>`, `Created / Posted`.

### Step 2 — Estimate hours

```bash
python scripts/estimate_hours.py
# Reads: activity_parsed.csv -> Writes: time_estimates.csv
```

Groups by `(date, ticket)`. Points per event:

| Activity type | Points |
|---|---|
| `Created` | 2.0 |
| `Status -> *` | 1.5 |
| `Commented` | 1.0 |
| `Updated` / `Created / Posted` | 0.5 |

`estimated_hours = clamp(total_points × 0.5, min=0.5, max=4.0)` rounded to nearest 0.5 h.

To tune weights, edit the `WEIGHTS` dict at the top of `scripts/estimate_hours.py`.

## Output columns

`time_estimates.csv`: `date`, `ticket`, `title`, `estimated_hours`, `activity_count`, `activity_breakdown`

`activity_parsed.csv`: `date`, `ticket`, `title`, `activity_type`, `description`