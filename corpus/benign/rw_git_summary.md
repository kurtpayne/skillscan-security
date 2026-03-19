---
name: git-summary
version: "1.0"
description: Summarize recent git activity — commits, branches, and open PRs.
tags: [git, summary, productivity]
allowed-tools: [Bash, Read]
---
## Overview
Produces a concise summary of recent repository activity.

## Usage
1. Run `git log --oneline --since=7days` to get recent commits.
2. Run `git branch -a` to list branches.
3. If `gh` is available, run `gh pr list --state open` to list open PRs.
4. Format as a Markdown report.

## Notes
Read-only. Does not commit, push, or modify any files.
