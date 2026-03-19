---
name: extract-todos
version: "1.0"
description: Find all TODO, FIXME, and HACK comments in a codebase.
tags: [code-quality, todos, maintenance]
allowed-tools: [Bash, Read]
---
## Overview
Scans the codebase for TODO, FIXME, HACK, and XXX comments and
produces a prioritized list.

## Usage
1. Run `grep -rn "TODO\|FIXME\|HACK\|XXX" --include="*.py" --include="*.ts"`.
2. Group by file and sort by type (FIXME > TODO > HACK > XXX).
3. Produce a Markdown table with file, line, type, and comment text.

## Notes
Read-only. Does not modify any files.
