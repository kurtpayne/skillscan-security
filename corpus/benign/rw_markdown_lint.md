---
name: lint-markdown
version: "0.6"
description: Lint Markdown files for style and formatting issues.
tags: [markdown, linting, documentation]
allowed-tools: [Read, Bash]
---
## Overview
Runs markdownlint on all .md files in the project and reports issues.

## Usage
1. Run `markdownlint "**/*.md" --json` to get structured output.
2. Group issues by rule and file.
3. Report a summary with issue counts per rule.

## Notes
Report only. Does not auto-fix issues.
