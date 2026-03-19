---
name: github-search
version: "1.0"
description: Search GitHub for repositories, issues, or code matching a query.
tags: [github, search, research]
allowed-tools: [Bash]
---
## Overview
Searches GitHub for repositories or code matching a query using the GitHub CLI.

## Usage
1. Run `gh search repos <query> --limit 10` for repository search.
2. Run `gh search issues <query> --limit 10` for issue search.
3. Format results as a Markdown table with name, stars, and description.

## Notes
Read-only. Does not fork, star, or modify repositories.
