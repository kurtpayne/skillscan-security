---
name: evaluate-prompt
version: "1.0"
description: Evaluate a prompt template against test cases and report quality metrics.
tags: [ai, prompts, evaluation]
---
## Overview
Evaluates a prompt template against a set of test cases and reports
quality metrics: accuracy, consistency, and format compliance.

## Usage
Provide: prompt template, test cases (input/expected output pairs).
The skill will run each test case and report pass/fail with explanations.

## Notes
Does not call external APIs. Uses the current model context only.
