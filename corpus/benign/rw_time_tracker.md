---
name: time-tracker
version: "1.0"
description: Analyze time tracking logs and produce a weekly report.
tags: [productivity, time-tracking, reporting]
allowed-tools: [Read]
---
## Overview
Reads a time tracking log and produces a weekly summary by project and task.

## Usage
1. Read the time log file (CSV or Toggl export format).
2. Group entries by project and task.
3. Report: total hours per project, daily distribution, and overtime.

## Notes
Read-only. Does not modify the time log.
