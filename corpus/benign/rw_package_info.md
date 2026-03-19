---
name: package-info
version: "1.0"
description: Look up information about a Python or npm package.
tags: [packages, research, dependencies]
allowed-tools: [WebFetch, Bash]
---
## Overview
Retrieves information about a package from PyPI or npm registry.

## Usage
1. For Python: fetch `https://pypi.org/pypi/<package>/json`.
2. For npm: fetch `https://registry.npmjs.org/<package>`.
3. Report: latest version, description, license, weekly downloads, dependencies.

## Notes
Read-only. Does not install packages.
