---
name: check-content-security-policy
version: "1.0"
description: Analyze a Content Security Policy header for security issues.
tags: [security, web, csp]
allowed-tools: [WebFetch]
---
## Overview
Fetches the Content Security Policy header from a URL and analyzes it
for common security misconfigurations.

## Usage
1. Fetch the URL and extract the Content-Security-Policy header.
2. Check for: unsafe-inline, unsafe-eval, wildcard sources, missing directives.
3. Report findings with severity and remediation guidance.

## Notes
Read-only network check. Does not modify the CSP or server configuration.
