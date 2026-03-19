---
name: format-code
version: "0.8"
description: Format Python, JavaScript, and TypeScript files using black and prettier.
tags: [formatting, python, javascript]
allowed-tools: [Bash, Read]
---
## Overview
Formats source files in the current directory using black (Python) and
prettier (JS/TS). Only modifies files; does not commit changes.

## Usage
1. Detect file types present in the project.
2. Run `black .` for Python files.
3. Run `prettier --write "**/*.{js,ts,jsx,tsx}"` for JS/TS files.
4. Report the number of files reformatted.

## Safety
Only operates on the current working directory. Does not touch files
outside the project root.
