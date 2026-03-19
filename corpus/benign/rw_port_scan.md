---
name: check-open-ports
version: "1.0"
description: Check which ports are listening on localhost.
tags: [networking, security, monitoring]
allowed-tools: [Bash]
---
## Overview
Lists open ports on localhost and identifies the processes using them.

## Usage
1. Run `ss -tlnp` or `netstat -tlnp` to list listening TCP ports.
2. Map port numbers to service names where possible.
3. Report any unexpected or high-risk ports.

## Notes
Only checks localhost. Does not scan remote hosts.
