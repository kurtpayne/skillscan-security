---
name: check-environment
version: "1.0"
description: Verify that required environment variables and tools are present.
tags: [environment, setup, validation]
allowed-tools: [Bash, Read]
---
## Overview
Checks that all required environment variables and CLI tools are available
before running a workflow.

## Usage
1. Check for required environment variables (names provided by user).
2. Check for required CLI tools using `which <tool>`.
3. Report missing variables and tools with setup instructions.

## Notes
Does not read or print the values of environment variables.
Only checks for their presence.
