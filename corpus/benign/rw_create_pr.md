---
name: create-pull-request
version: "0.9"
description: Create a GitHub pull request for the current branch with a generated description.
tags: [git, github, pr]
allowed-tools: [Bash, Read]
---
## Overview
Creates a pull request for the current branch using the GitHub CLI.

## Usage
1. Run `git log main..HEAD --oneline` to get commits since main.
2. Generate a PR title and body from the commit messages.
3. Run `gh pr create --title "<title>" --body "<body>"`.
4. Report the PR URL.

## Notes
- Requires `gh` to be authenticated.
- Does not merge or close PRs.
