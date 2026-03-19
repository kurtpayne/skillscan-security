---
name: analyze-logs
version: "1.0"
description: Parse application logs and summarize errors, warnings, and patterns.
tags: [logs, analysis, debugging]
allowed-tools: [Read, Bash]
---
## Overview
Reads a log file and produces a summary of error patterns, frequency,
and time distribution.

## Usage
1. Read the log file (supports common formats: nginx, apache, JSON logs).
2. Count occurrences of ERROR, WARN, and INFO levels.
3. Identify the top 5 most frequent error messages.
4. Report the time range covered by the log.

## Notes
Read-only. Does not modify the log file.
