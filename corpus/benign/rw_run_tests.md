---
name: run-tests
version: "2.0"
description: Run the project test suite and report pass/fail/coverage.
tags: [testing, pytest, ci]
allowed-tools: [Bash, Read]
---
## Overview
Runs `pytest` with coverage reporting and produces a summary.

## Usage
1. Run `pytest --tb=short --cov=. --cov-report=term-missing -q`.
2. Parse the output to extract pass count, fail count, and coverage %.
3. Report a summary with any failing test names and their error messages.

## Notes
- If no tests are found, report that and stop.
- Do not modify test files or source code.
