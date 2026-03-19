---
name: write-api-docs
version: "1.0"
description: Generate OpenAPI documentation from a FastAPI or Flask application.
tags: [documentation, api, openapi]
allowed-tools: [Read, Bash]
---
## Overview
Generates OpenAPI 3.0 documentation for a Python web API.

## Usage
1. Read the route definitions from the application source.
2. For FastAPI: fetch `/openapi.json` if the server is running.
3. Generate a structured API reference in Markdown format.

## Notes
Read-only. Does not modify the application source.
