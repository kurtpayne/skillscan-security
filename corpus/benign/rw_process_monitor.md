---
name: monitor-processes
version: "1.0"
description: Monitor system processes and identify resource-intensive ones.
tags: [sysadmin, monitoring, performance]
allowed-tools: [Bash]
---
## Overview
Reports the top resource-consuming processes on the system.

## Usage
1. Run `ps aux --sort=-%cpu | head -20` for CPU usage.
2. Run `ps aux --sort=-%mem | head -20` for memory usage.
3. Report: PID, user, CPU%, MEM%, and command for top 10 processes.

## Notes
Read-only. Does not kill or modify processes.
