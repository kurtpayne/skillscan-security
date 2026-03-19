---
name: write-pr-description
version: "1.0"
description: Generate a pull request description from branch commits and diff.
tags: [git, github, writing]
allowed-tools: [Bash]
---
## Overview
Generates a structured pull request description from branch commits and diff.

## Usage
1. Run `git log main..HEAD --oneline` to get commits.
2. Run `git diff main...HEAD --stat` to get changed files.
3. Generate a PR description with: Summary, Changes, Testing, Screenshots (if UI).

## Notes
Does not create the PR. Only generates the description.
