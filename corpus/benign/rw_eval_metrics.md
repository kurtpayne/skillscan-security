---
name: compute-eval-metrics
version: "1.0"
description: Compute precision, recall, F1, and confusion matrix for a classifier.
tags: [ml, evaluation, metrics]
allowed-tools: [Read, Bash]
---
## Overview
Computes classification metrics from a predictions file and ground truth labels.

## Usage
1. Read predictions file (CSV with columns: id, predicted_label, true_label).
2. Compute: precision, recall, F1 (macro and per-class), accuracy, confusion matrix.
3. Report as a Markdown table with per-class breakdown.

## Notes
Read-only. Does not modify the predictions file.
