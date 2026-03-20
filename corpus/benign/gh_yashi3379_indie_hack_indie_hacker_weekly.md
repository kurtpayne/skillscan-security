---
name: indie-hacker-weekly
description: Weekly collection and translation of overseas indie hacker success stories. Use when user wants to gather, translate, and summarize success stories of individual developers from overseas sources like Indie Hackers, Product Hunt, Hacker News, and X (Twitter). Outputs structured data suitable for Notion pages and slide presentations.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: yashi3379/indie-hacker-weekly-skill
# corpus-url: https://github.com/yashi3379/indie-hacker-weekly-skill/blob/33572fd011fd15731f8d61796f8ed97e3adfc1a2/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Indie Hacker Weekly Report Skill

This skill collects, translates, and summarizes overseas indie hacker success stories on a weekly basis.

## Overview

Collect success stories from overseas indie hacker communities and output structured Japanese summaries. Target sources include Indie Hackers, Product Hunt, Hacker News, Reddit r/indiehackers, and X (Twitter).

## Information to Collect

For each success story, gather:

| Priority | Information | Example |
|----------|-------------|---------|
| ★★★ | Monthly Revenue | $20,000/month (約300万円) |
| ★★★ | Development Period | 3 days, 2 weeks |
| ★★☆ | Tech Stack | Cursor, Claude Code, React Native |
| ★★☆ | Marketing Method | TikTok, Product Hunt, Instagram |
| ★★☆ | Success Factors | Niche market, viral content |
| ★☆☆ | Failure Lessons | What didn't work |

## Data Sources

Search these sources in order:

1. **Indie Hackers** (indiehackers.com) - Revenue milestones, success stories
2. **Product Hunt** (producthunt.com) - Trending products, launch stories
3. **Hacker News** (news.ycombinator.com) - Show HN posts, discussions
4. **Reddit r/indiehackers** - Real success/failure stories
5. **X (Twitter)** - Indie hacker accounts sharing revenue

## Search Queries

Use these search patterns:

```
"indie hacker" "MRR" OR "revenue" site:indiehackers.com
"solo developer" "launched" "$" site:producthunt.com
"Show HN" "revenue" OR "users" site:news.ycombinator.com
```

## Output Format

### For Notion Page

```markdown
# 🚀 海外インディーハッカー週報 [DATE]

## 📊 今週のサマリー

| 開発者 | アプリ名 | 月収 | 開発期間 | 技術 |
|--------|---------|------|---------|------|
| [Name] | [App] | $X,XXX | X days | [Stack] |

## 🎯 ピックアップ #1: [App Name]

### 概要
[One paragraph summary in Japanese]

### なぜ売れた？
- [Reason 1]
- [Reason 2]
- [Reason 3]

### 技術スタック
- [Tech 1]
- [Tech 2]

### マーケティング手法
- [Method 1]
- [Method 2]

### 学び
- [Learning 1]
- [Learning 2]

### ソース
- [URL 1]
- [URL 2]

---

## 🎯 ピックアップ #2: [App Name]
[Same structure as above]

---

## 🔗 今週の注目リンク
- [Link 1]
- [Link 2]
- [Link 3]
```

### For Slide Presentation

Create slides with this structure:

1. **Title Slide**: 海外インディーハッカー週報 + Date
2. **Summary Slide**: Table of all success stories
3. **Deep Dive Slides** (2-3 per story):
   - Story overview + revenue highlight
   - Tech stack + marketing method
   - Key learnings
4. **Closing Slide**: Links and resources

## Workflow

1. Search each data source for recent success stories (past 7 days)
2. Filter for stories with concrete revenue numbers
3. Translate and summarize in Japanese
4. Structure data according to output format
5. Create Notion page using Notion MCP
6. Prepare slide content for presentation

## Quality Checklist

Before delivering:

- [ ] At least 3 success stories collected
- [ ] All revenue numbers converted to JPY (1 USD ≈ 150 JPY)
- [ ] Tech stacks clearly listed
- [ ] Marketing methods documented
- [ ] Source URLs included for verification