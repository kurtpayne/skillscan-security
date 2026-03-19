---
name: test-regex
version: "1.0"
description: Test a regular expression against sample inputs and explain its behavior.
tags: [regex, testing, development]
allowed-tools: [Bash]
---
## Overview
Tests a regular expression against provided sample inputs and explains
what it matches.

## Usage
1. Run `python3 -c "import re; ..."` to test the regex against samples.
2. Report: which samples match, which do not, and capture group values.
3. Explain the regex in plain language.

## Notes
Does not modify any files. Only evaluates the regex against provided samples.
