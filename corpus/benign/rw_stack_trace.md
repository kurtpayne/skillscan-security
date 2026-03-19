---
name: analyze-stack-trace
version: "1.0"
description: Parse a stack trace and identify the root cause of an error.
tags: [debugging, errors, analysis]
allowed-tools: [Read]
---
## Overview
Analyzes a stack trace and provides a structured diagnosis of the error.

## Usage
Provide the stack trace text. The skill will:
1. Identify the exception type and message.
2. Trace the call stack to the originating line.
3. Suggest likely root causes and remediation steps.

## Notes
Analysis only. Does not modify source code.
