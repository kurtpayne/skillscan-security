---
name: verify-backup
version: "1.0"
description: Verify the integrity of a backup archive.
tags: [backup, integrity, devops]
allowed-tools: [Bash, Read]
---
## Overview
Verifies that a backup archive is intact and readable.

## Usage
1. For .tar.gz: run `tar -tzf <archive>` to list contents without extracting.
2. For .zip: run `unzip -t <archive>` to test integrity.
3. Compare file count against an expected manifest if provided.
4. Report: archive size, file count, and any corruption errors.

## Notes
Does not extract or modify the archive.
