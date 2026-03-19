---
name: prepare-fine-tune-data
version: "1.0"
description: Prepare and validate a fine-tuning dataset in JSONL format.
tags: [ml, fine-tuning, data]
allowed-tools: [Read, Write, Bash]
---
## Overview
Validates and formats a dataset for fine-tuning an LLM.

## Usage
1. Read the input dataset (CSV or JSONL).
2. Validate: required fields present, no empty examples, token count within limits.
3. Convert to the target format (OpenAI JSONL or HuggingFace format).
4. Report: example count, average token length, and any validation errors.

## Notes
Does not upload data to any API. Only local file operations.
