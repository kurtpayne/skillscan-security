---
name: audit-ssh-config
version: "1.0"
description: Audit SSH server configuration for security best practices.
tags: [sysadmin, security, ssh]
allowed-tools: [Read]
---
## Overview
Reviews the SSH server configuration for security issues.

## Usage
1. Read `/etc/ssh/sshd_config`.
2. Check for: PasswordAuthentication yes, PermitRootLogin yes,
   weak ciphers, missing AllowUsers/AllowGroups.
3. Report findings with severity and remediation guidance.

## Notes
Read-only. Does not modify the SSH configuration.
