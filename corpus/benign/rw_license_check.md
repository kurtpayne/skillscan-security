---
name: check-licenses
version: "1.0"
description: Check dependency licenses for compliance with a policy.
tags: [security, licensing, compliance]
allowed-tools: [Bash, Read]
---
## Overview
Checks all project dependencies for license compliance against a
specified policy (e.g., no GPL, only permissive licenses).

## Usage
1. Run `pip-licenses --format=json` for Python dependencies.
2. Run `license-checker --json` for Node.js dependencies.
3. Flag any licenses that violate the specified policy.

## Notes
Read-only. Does not modify dependencies or license files.
