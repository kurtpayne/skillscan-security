---
name: create-ticket
version: "0.9"
description: Create a GitHub issue from a bug report or feature request description.
tags: [github, issues, productivity]
allowed-tools: [Bash]
---
## Overview
Creates a GitHub issue with a structured title, body, and labels.

## Usage
1. Parse the user's description to extract: title, type (bug/feature), priority.
2. Generate a structured issue body with: Summary, Steps to Reproduce (bugs),
   Acceptance Criteria (features), and Environment.
3. Run `gh issue create --title "<title>" --body "<body>" --label "<label>"`.
4. Report the issue URL.

## Notes
Requires `gh` to be authenticated. Does not close or modify existing issues.
