---
name: check-system-updates
version: "1.0"
description: Check for available system package updates.
tags: [sysadmin, updates, maintenance]
allowed-tools: [Bash]
---
## Overview
Checks for available system package updates without installing them.

## Usage
1. For Debian/Ubuntu: run `apt list --upgradable 2>/dev/null`.
2. For RHEL/CentOS: run `yum check-update` or `dnf check-update`.
3. Report: number of available updates, security updates, and critical packages.

## Notes
Read-only. Does not install updates.
