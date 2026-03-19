---
name: check-services
version: "1.0"
description: Check the status of systemd services and report failures.
tags: [sysadmin, systemd, monitoring]
allowed-tools: [Bash]
---
## Overview
Reports the status of systemd services and identifies failed or degraded ones.

## Usage
1. Run `systemctl list-units --state=failed` to find failed services.
2. Run `systemctl status <service>` for each failed service to get details.
3. Report: service name, status, last error message, and restart count.

## Notes
Read-only. Does not restart or modify services.
