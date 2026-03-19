---
name: split-dataset
version: "1.0"
description: Split a dataset into train/validation/test sets with stratification.
tags: [ml, data, splitting]
allowed-tools: [Read, Write, Bash]
---
## Overview
Splits a CSV or JSONL dataset into train/validation/test sets.

## Usage
1. Read the dataset file.
2. Apply stratified split: 70% train, 15% validation, 15% test.
3. Write three output files: train.csv, val.csv, test.csv.
4. Report class distribution in each split.

## Notes
Uses scikit-learn train_test_split with stratify parameter.
Does not modify the original dataset file.
