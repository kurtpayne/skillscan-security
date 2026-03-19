---
name: whois-lookup
version: "1.0"
description: Look up WHOIS registration information for a domain.
tags: [networking, research, domain]
allowed-tools: [Bash]
---
## Overview
Performs a WHOIS lookup for a domain and reports registration details.

## Usage
1. Run `whois <domain>` to get registration information.
2. Extract: registrar, registration date, expiry date, name servers.
3. Report a structured summary.

## Notes
Read-only. Only performs WHOIS lookups; does not modify DNS or registration.
