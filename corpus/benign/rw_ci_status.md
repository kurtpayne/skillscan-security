---
name: check-ci-status
version: "1.0"
description: Check the status of GitHub Actions workflows for the current branch.
tags: [ci, github-actions, devops]
allowed-tools: [Bash]
---
## Overview
Reports the status of recent CI workflow runs for the current branch.

## Usage
1. Run `gh run list --branch <current-branch> --limit 10`.
2. For any failed runs, run `gh run view <run-id> --log-failed` to get error details.
3. Report: run status, workflow name, duration, and failure summary.

## Notes
Read-only. Does not re-run or cancel workflows.
