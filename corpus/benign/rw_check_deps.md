---
name: check-dependencies
version: "1.0"
description: Check for outdated or vulnerable Python and Node.js dependencies.
tags: [security, dependencies, audit]
allowed-tools: [Bash, Read]
---
## Overview
Audits project dependencies for known vulnerabilities and available updates.

## Usage
1. If `requirements.txt` or `pyproject.toml` exists, run `pip-audit`.
2. If `package.json` exists, run `npm audit --json`.
3. Summarize findings: critical, high, medium, low severity counts.

## Notes
- Report only; do not auto-update dependencies.
- If pip-audit is not installed, suggest `pip install pip-audit`.
