---
name: benchmark
version: "0.5"
description: Run Python benchmarks using pytest-benchmark and report results.
tags: [performance, benchmarking, python]
allowed-tools: [Bash, Read]
---
## Overview
Runs performance benchmarks and compares results against a stored baseline.

## Usage
1. Run `pytest --benchmark-only --benchmark-json=benchmark.json`.
2. If a baseline exists, compare and report regressions (>10% slower).
3. Save results as the new baseline if no regressions are found.

## Notes
Does not modify source code. Only writes benchmark result files.
