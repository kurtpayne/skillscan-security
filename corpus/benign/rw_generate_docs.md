---
name: generate-docs
version: "1.1"
description: Generate API documentation from Python docstrings using pdoc.
tags: [documentation, python, pdoc]
allowed-tools: [Bash, Read, Write]
---
## Overview
Generates HTML documentation from Python source files using pdoc.

## Usage
1. Identify the main package directory.
2. Run `pdoc --html --output-dir docs/ <package>`.
3. Report the output path and list of generated files.

## Notes
- Creates `docs/` directory if it does not exist.
- Does not publish or deploy the documentation.
