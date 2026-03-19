---
name: json-transform
version: "0.7"
description: Apply a jq transformation to a JSON file and write the result.
tags: [json, transformation, jq]
allowed-tools: [Read, Write, Bash]
---
## Overview
Applies a user-specified jq expression to a JSON input file and writes
the transformed output to a new file.

## Usage
1. Read the input JSON file.
2. Apply the jq expression: `jq '<expression>' input.json > output.json`.
3. Validate the output is valid JSON.
4. Report the output file path and record count.

## Notes
Does not modify the input file. Creates a new output file.
