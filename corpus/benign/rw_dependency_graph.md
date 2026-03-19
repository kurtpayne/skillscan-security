---
name: dependency-graph
version: "1.0"
description: Generate a dependency graph for a Python or Node.js project.
tags: [dependencies, visualization, analysis]
allowed-tools: [Bash, Read, Write]
---
## Overview
Generates a dependency graph showing relationships between packages.

## Usage
1. For Python: run `pipdeptree --json` to get the dependency tree.
2. For Node.js: read `package-lock.json` to extract dependencies.
3. Generate a DOT format graph and render it using graphviz.
4. Save the output as `dependency_graph.png`.

## Notes
Does not install or modify dependencies.
