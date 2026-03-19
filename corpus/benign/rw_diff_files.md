---
name: diff-files
version: "1.0"
description: Compare two files or directories and summarize the differences.
tags: [diff, comparison, files]
allowed-tools: [Read, Bash]
---
## Overview
Compares two files or directory trees and produces a structured diff summary.

## Usage
1. Run `diff -u <file1> <file2>` for files, or `diff -rq <dir1> <dir2>` for dirs.
2. Parse the output and summarize: lines added, removed, changed.
3. For directories, list files that differ, are new, or are missing.

## Notes
Read-only. Does not modify any files.
