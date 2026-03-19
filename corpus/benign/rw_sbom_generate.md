---
name: generate-sbom
version: "1.0"
description: Generate a Software Bill of Materials for a Python or Node.js project.
tags: [security, sbom, compliance]
allowed-tools: [Bash, Read]
---
## Overview
Generates an SBOM in CycloneDX or SPDX format for a project.

## Usage
1. For Python: run `cyclonedx-py requirements -o sbom.json`.
2. For Node.js: run `cyclonedx-npm --output-file sbom.json`.
3. Report: total components, license distribution, and any unknown licenses.

## Notes
Read-only. Does not install or modify dependencies.
