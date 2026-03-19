---
name: check-firewall-rules
version: "1.0"
description: List and analyze firewall rules for security issues.
tags: [sysadmin, security, firewall]
allowed-tools: [Bash]
---
## Overview
Lists firewall rules and identifies overly permissive configurations.

## Usage
1. Run `iptables -L -n -v` or `ufw status verbose` to list rules.
2. Flag: rules that allow all traffic (0.0.0.0/0), missing default deny.
3. Report a summary of allowed and denied traffic patterns.

## Notes
Read-only. Does not modify firewall rules.
