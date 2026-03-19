---
name: compare-environments
version: "1.0"
description: Compare environment variables between two deployment environments.
tags: [devops, environment, configuration]
allowed-tools: [Read]
---
## Overview
Compares .env files or environment variable lists between staging and production
to identify missing or mismatched configuration.

## Usage
1. Read both environment files (e.g., .env.staging and .env.production).
2. Compare keys: report keys present in one but not the other.
3. Report keys with different values (mask actual values for security).

## Notes
Never prints actual secret values. Only reports key names and presence/absence.
