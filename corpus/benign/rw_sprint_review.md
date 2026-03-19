---
name: sprint-review
version: "0.8"
description: Generate a sprint review summary from closed GitHub issues and PRs.
tags: [agile, sprint, github]
allowed-tools: [Bash]
---
## Overview
Generates a sprint review document from GitHub issues and PRs closed
in the current sprint period.

## Usage
1. Run `gh issue list --state closed --search "closed:>YYYY-MM-DD"`.
2. Run `gh pr list --state merged --search "merged:>YYYY-MM-DD"`.
3. Group by milestone or label.
4. Produce a Markdown sprint review document.

## Notes
Read-only. Does not modify issues, PRs, or milestones.
