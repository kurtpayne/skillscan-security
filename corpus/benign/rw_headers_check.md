---
name: check-security-headers
version: "1.0"
description: Check HTTP security headers for a web application.
tags: [security, web, headers]
allowed-tools: [Bash]
---
## Overview
Checks a web application for the presence and correct configuration
of security-related HTTP headers.

## Usage
1. Fetch the URL headers using `curl -sI <url>`.
2. Check for: HSTS, X-Frame-Options, X-Content-Type-Options,
   Referrer-Policy, Permissions-Policy.
3. Report missing or misconfigured headers with remediation guidance.

## Notes
Read-only. Only sends HEAD requests.
