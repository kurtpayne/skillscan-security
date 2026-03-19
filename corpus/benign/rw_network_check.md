---
name: check-network-connectivity
version: "1.0"
description: Check network connectivity and DNS resolution.
tags: [networking, sysadmin, diagnostics]
allowed-tools: [Bash]
---
## Overview
Checks network connectivity and DNS resolution for a list of hosts.

## Usage
1. Ping each host to check connectivity.
2. Run `nslookup` or `dig` to verify DNS resolution.
3. Check HTTP/HTTPS connectivity with `curl -sI`.
4. Report: latency, packet loss, and DNS resolution results.

## Notes
Read-only network diagnostics. Does not modify network configuration.
