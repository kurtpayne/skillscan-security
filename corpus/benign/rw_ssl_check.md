---
name: check-ssl-certificate
version: "1.0"
description: Check SSL certificate expiry and configuration for a domain.
tags: [ssl, security, monitoring]
allowed-tools: [Bash]
---
## Overview
Checks the SSL certificate for a domain and reports expiry date,
issuer, and any configuration issues.

## Usage
1. Run `echo | openssl s_client -connect <domain>:443 2>/dev/null | openssl x509 -noout -dates -subject -issuer`.
2. Calculate days until expiry.
3. Warn if expiry is within 30 days.

## Notes
Read-only network check. Does not modify certificates or DNS.
