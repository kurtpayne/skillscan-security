---
name: write-model-card
version: "1.0"
description: Generate a HuggingFace model card from training metadata.
tags: [ml, documentation, huggingface]
allowed-tools: [Read]
---
## Overview
Generates a model card following the HuggingFace model card template.

## Output sections
- **Model description**: architecture, training data, intended use
- **Training details**: dataset, hyperparameters, hardware
- **Evaluation results**: metrics on evaluation sets
- **Limitations**: known failure modes and biases
- **Citation**: how to cite the model
