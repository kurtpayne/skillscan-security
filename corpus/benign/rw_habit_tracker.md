---
name: habit-tracker
version: "1.0"
description: Track daily habits and report streaks and completion rates.
tags: [productivity, habits, tracking]
allowed-tools: [Read, Write]
---
## Overview
Reads a habit tracking log and reports current streaks and completion rates.

## Usage
1. Read the habit log file (CSV or Markdown table).
2. Calculate: current streak, longest streak, 7-day completion rate per habit.
3. Report a summary table and motivational message.

## Notes
Only reads and writes the habit log file. Does not access external services.
