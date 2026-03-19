---
name: check-cors-policy
version: "1.0"
description: Test CORS configuration for an API endpoint.
tags: [security, web, cors]
allowed-tools: [Bash]
---
## Overview
Tests the CORS configuration of an API endpoint by sending preflight
requests and analyzing the response headers.

## Usage
1. Send an OPTIONS request with Origin and Access-Control-Request-Method headers.
2. Check the response for: Access-Control-Allow-Origin, credentials, methods.
3. Flag overly permissive configurations (wildcard origin with credentials).

## Notes
Read-only. Only sends OPTIONS requests.
