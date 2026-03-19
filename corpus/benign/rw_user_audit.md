---
name: audit-user-accounts
version: "1.0"
description: Audit user accounts for security issues.
tags: [sysadmin, security, users]
allowed-tools: [Bash, Read]
---
## Overview
Audits system user accounts for security issues.

## Usage
1. Read `/etc/passwd` to list user accounts.
2. Check for: accounts with no password, accounts with UID 0 (besides root),
   accounts with login shells that shouldn't have them.
3. Report findings with remediation guidance.

## Notes
Read-only. Does not modify user accounts.
