---
name: hyperparameter-search
version: "1.0"
description: Run a grid search over hyperparameters and report the best configuration.
tags: [ml, hyperparameters, optimization]
allowed-tools: [Bash, Read]
---
## Overview
Runs a grid search over specified hyperparameters using scikit-learn
GridSearchCV and reports the best configuration.

## Usage
1. Read the training data and model configuration.
2. Run GridSearchCV with the specified parameter grid.
3. Report: best parameters, best score, and cross-validation results.

## Notes
Uses cross-validation. Does not train the final model.
