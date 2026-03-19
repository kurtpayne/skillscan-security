---
name: test-api-endpoint
version: "1.0"
description: Test a REST API endpoint and validate the response.
tags: [api, testing, http]
allowed-tools: [Bash]
---
## Overview
Sends HTTP requests to an API endpoint and validates the response
against expected status codes and schema.

## Usage
1. Run `curl -s -w "\n%{http_code}" <url>` to get response and status.
2. Validate the status code matches the expected value.
3. If a JSON schema is provided, validate the response body.
4. Report: status code, response time, and validation result.

## Notes
Only sends GET requests by default. POST/PUT/DELETE require explicit
user confirmation.
