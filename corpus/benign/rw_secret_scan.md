---
name: scan-for-secrets
version: "1.0"
description: Scan the codebase for accidentally committed secrets.
tags: [security, secrets, scanning]
allowed-tools: [Bash, Read]
---
## Overview
Scans the repository for accidentally committed secrets using gitleaks.

## Usage
1. Run `gitleaks detect --source . --report-format json`.
2. Parse the report and summarize findings by type (API key, password, etc.).
3. Report file paths and line numbers for each finding.

## Notes
Read-only. Does not remove secrets or modify files.
Remind the user to rotate any exposed credentials immediately.
