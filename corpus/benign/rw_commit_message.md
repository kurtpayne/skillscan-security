---
name: write-commit-message
version: "1.0"
description: Generate a conventional commit message from staged changes.
tags: [git, commits, writing]
allowed-tools: [Bash]
---
## Overview
Generates a conventional commit message from the staged git diff.

## Usage
1. Run `git diff --staged` to get staged changes.
2. Analyze the changes to determine: type (feat/fix/docs/chore), scope, and impact.
3. Generate a commit message following the Conventional Commits specification.

## Notes
Does not commit. Only generates the message for the user to review.
