---
name: disk-usage-report
version: "1.0"
description: Report disk usage for a directory tree, highlighting large files.
tags: [disk, monitoring, maintenance]
allowed-tools: [Bash]
---
## Overview
Analyzes disk usage for a directory and identifies large files and directories.

## Usage
1. Run `du -sh <directory>/*` to get top-level usage.
2. Run `find <directory> -size +100M -type f` to find large files.
3. Report total usage, top 10 largest directories, and files over 100MB.

## Notes
Read-only. Does not delete or move files.
