---
name: arxiv-search
version: "1.0"
description: Search arXiv for recent papers on a topic and summarize findings.
tags: [research, arxiv, papers]
allowed-tools: [WebFetch]
---
## Overview
Searches arXiv for recent papers on a topic and produces a reading list
with abstracts.

## Usage
1. Fetch `https://arxiv.org/search/?query=<topic>&searchtype=all&start=0`.
2. Extract paper titles, authors, dates, and abstracts.
3. Return the top 10 most recent results as a Markdown list.

## Notes
Read-only. Does not download full PDFs unless explicitly requested.
