---
name: count-tokens
version: "1.0"
description: Count tokens in a text file for LLM context planning.
tags: [ai, tokens, planning]
allowed-tools: [Read, Bash]
---
## Overview
Counts the number of tokens in a text file using tiktoken
for accurate LLM context planning.

## Usage
1. Read the input file.
2. Count tokens using tiktoken with the specified model encoding.
3. Report: token count, character count, estimated cost at current pricing.

## Notes
Uses tiktoken for accurate token counting. Supports cl100k_base (GPT-4)
and p50k_base (GPT-3.5) encodings.
