---
name: audit-cron-jobs
version: "1.0"
description: List and audit scheduled cron jobs for security issues.
tags: [sysadmin, security, cron]
allowed-tools: [Bash, Read]
---
## Overview
Lists all cron jobs for the current user and system-wide, and flags
potentially dangerous configurations.

## Usage
1. Run `crontab -l` for user cron jobs.
2. Read `/etc/cron*` directories for system cron jobs.
3. Flag: world-writable scripts, scripts in /tmp, missing absolute paths.

## Notes
Read-only. Does not modify cron jobs.
