---
name: update-readme
version: "1.0"
description: Update the README.md with current project structure and usage.
tags: [documentation, readme, markdown]
allowed-tools: [Read, Write, Bash]
---
## Overview
Refreshes the README.md with an up-to-date project structure, installation
instructions, and usage examples.

## Usage
1. Read the current README.md.
2. Run `find . -type f -name "*.py" | head -20` to get project structure.
3. Update the Installation, Usage, and Project Structure sections.
4. Preserve any sections marked with <!-- DO NOT EDIT -->.

## Notes
Only modifies README.md. Does not change source code.
