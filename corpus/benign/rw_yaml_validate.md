---
name: validate-yaml
version: "1.0"
description: Validate YAML files against a JSON Schema or check for syntax errors.
tags: [yaml, validation, schema]
allowed-tools: [Read, Bash]
---
## Overview
Validates YAML files for syntax errors and optionally checks them
against a JSON Schema.

## Usage
1. Parse each YAML file to check for syntax errors.
2. If a schema file is provided, validate against it using jsonschema.
3. Report validation errors with file, line, and error message.

## Notes
Read-only. Does not modify YAML files.
