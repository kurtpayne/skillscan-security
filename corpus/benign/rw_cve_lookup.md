---
name: cve-lookup
version: "1.0"
description: Look up CVE details for a given CVE ID or package name.
tags: [security, cve, vulnerability]
allowed-tools: [WebFetch]
---
## Overview
Fetches CVE details from the NVD API and produces a structured summary.

## Usage
1. Fetch `https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=<CVE-ID>`.
2. Extract: CVSS score, severity, description, affected products, references.
3. Report a structured summary with remediation guidance if available.

## Notes
Read-only. Uses the public NVD API (no authentication required).
