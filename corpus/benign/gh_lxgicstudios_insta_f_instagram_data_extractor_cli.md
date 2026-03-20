---
name: Instagram Data Extractor CLI
description: Extract Instagram profiles, posts, stories, reels, and followers. Anti-detection features built-in. Free OSINT tool for researchers and marketers.
tags: [instagram, scraper, osint, social-media, data-extraction, cli, marketing]
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: lxgicstudios/insta-fetch
# corpus-url: https://github.com/lxgicstudios/insta-fetch/blob/ff37b83212deaa903aff693d4953747709d8d9f2/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Instagram Data Extractor CLI

Scrape Instagram data without getting blocked. Profiles, posts, stories, reels, hashtags, followers.

**Anti-detection built-in. No API keys required.**

## Quick Start

```bash
npm install -g insta-fetch-cli
```

```bash
# Get profile info
insta-fetch profile username

# Fetch posts
insta-fetch posts username -n 50 -o json

# Search hashtag
insta-fetch hashtag travel --top -n 100
```

## What It Does

- Profile data extraction (bio, stats, links)
- Posts, stories, reels scraping
- Hashtag search with trending filter
- Followers/following lists (auth required)
- Multiple output formats (JSON, CSV, table)

## Anti-Detection Features

- Random delays between requests
- Rotating user agents
- Rate limiting (100 req/min default)
- Session-based authentication

## Commands

```bash
# Fetch stories (requires auth)
insta-fetch stories username --download ./media

# Fetch reels
insta-fetch reels username -n 20

# Get followers (requires auth)
insta-fetch followers username -n 500
```

## Output Options

| Option | Description |
|--------|-------------|
| `-o json` | JSON output |
| `-o jsonl` | JSON Lines (streaming) |
| `-o csv` | CSV export |
| `-o table` | Pretty table view |
| `--save` | Save to file |

## When to Use This

- Social media research and OSINT
- Competitor analysis
- Influencer marketing research
- Content strategy planning
- Data journalism

## Requirements

Node.js 18+. Authentication required for private data.

---

**Built by [LXGIC Studios](https://lxgicstudios.com)**

🔗 [GitHub](https://github.com/lxgicstudios/insta-fetch) · [Twitter](https://x.com/lxgicstudios)