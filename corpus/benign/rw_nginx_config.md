---
name: validate-nginx-config
version: "1.0"
description: Validate an nginx configuration file for syntax errors.
tags: [nginx, configuration, validation]
allowed-tools: [Read, Bash]
---
## Overview
Validates an nginx configuration file using `nginx -t`.

## Usage
1. Read the nginx configuration file.
2. Run `nginx -t -c <config-file>` to check for syntax errors.
3. Report any errors with file and line number.

## Notes
Read-only. Does not restart nginx or apply configuration changes.
