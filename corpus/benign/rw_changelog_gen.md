---
name: generate-changelog
version: "1.0"
description: Generate a CHANGELOG entry from git commits since the last tag.
tags: [git, changelog, release]
allowed-tools: [Bash, Read, Write]
---
## Overview
Generates a CHANGELOG.md entry for the current release based on
conventional commit messages since the last git tag.

## Usage
1. Run `git log <last-tag>..HEAD --oneline` to get commits.
2. Group by type: feat, fix, docs, chore, breaking.
3. Generate a Markdown section with the new version and date.
4. Prepend to CHANGELOG.md.

## Notes
Follows Keep a Changelog format. Only writes to CHANGELOG.md.
