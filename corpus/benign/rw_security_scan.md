---
name: security-scan
version: "1.0"
description: Run bandit static security analysis on Python source code.
tags: [security, python, bandit]
allowed-tools: [Bash, Read]
---
## Overview
Runs bandit to identify common security issues in Python code.

## Usage
1. Run `bandit -r . -f json -o bandit_report.json`.
2. Parse the JSON report and summarize HIGH and MEDIUM severity findings.
3. List each finding with file, line, issue type, and severity.

## Notes
Report only. Does not modify source code or auto-fix issues.
