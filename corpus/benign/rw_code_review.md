---
name: code-review
version: "1.3"
description: Review staged git changes and provide structured feedback.
tags: [code-review, git, quality]
allowed-tools: [Bash, Read]
---
## Overview
Reviews the current git diff and provides structured feedback on code quality,
potential bugs, and style issues.

## Usage
1. Run `git diff --staged` to get staged changes.
2. Analyze the diff for: logic errors, missing error handling, security issues,
   style inconsistencies, and missing tests.
3. Produce a structured review with severity labels (critical/warning/suggestion).

## Notes
Read-only. Does not modify any files.
