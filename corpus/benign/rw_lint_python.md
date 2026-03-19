---
name: lint-python
version: "1.2"
description: Run ruff and mypy on the current Python project and report issues.
tags: [python, linting, quality]
allowed-tools: [Bash, Read]
---
## Overview
Runs `ruff check .` and `mypy .` on the project root, collects output,
and produces a structured report of errors, warnings, and type issues.

## Usage
1. Run `ruff check . --output-format=json` and parse the JSON output.
2. Run `mypy . --show-error-codes` and parse the plain-text output.
3. Combine results into a Markdown table grouped by file.

## Notes
- Do not auto-fix issues without explicit user confirmation.
- If ruff or mypy is not installed, report the missing tool and stop.
