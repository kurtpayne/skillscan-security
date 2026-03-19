---
name: news-summary
version: "1.0"
description: Fetch and summarize recent news on a topic from RSS feeds.
tags: [news, rss, summarization]
allowed-tools: [WebFetch]
---
## Overview
Fetches recent news articles on a topic from RSS feeds and produces
a concise summary.

## Usage
1. Fetch RSS feeds from relevant sources (e.g., Hacker News, TechCrunch).
2. Filter articles from the past 24 hours.
3. Summarize the top 5 stories with title, source, and 2-sentence summary.

## Notes
Only fetches publicly accessible RSS feeds. Does not log in to any service.
