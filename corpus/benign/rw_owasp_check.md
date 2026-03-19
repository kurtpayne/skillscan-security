---
name: owasp-top10-check
version: "1.0"
description: Check a web application for OWASP Top 10 vulnerabilities.
tags: [security, owasp, web]
allowed-tools: [Read, Bash]
---
## Overview
Reviews source code and configuration for common OWASP Top 10 vulnerabilities.

## Usage
1. Check for SQL injection: look for string concatenation in queries.
2. Check for XSS: look for unescaped user input in templates.
3. Check for insecure deserialization, hardcoded credentials, and missing auth.
4. Report findings with file, line, and remediation guidance.

## Notes
Static analysis only. Does not send requests to the application.
