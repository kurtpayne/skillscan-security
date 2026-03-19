---
name: check-memory-usage
version: "1.0"
description: Report memory usage and identify memory-intensive processes.
tags: [sysadmin, monitoring, memory]
allowed-tools: [Bash]
---
## Overview
Reports system memory usage and identifies processes consuming the most memory.

## Usage
1. Run `free -h` to get total, used, and available memory.
2. Run `ps aux --sort=-%mem | head -10` for top memory consumers.
3. Check for memory leaks: processes with growing RSS over time.
4. Report: total/used/available, swap usage, and top 10 consumers.

## Notes
Read-only. Does not kill processes or modify memory settings.
