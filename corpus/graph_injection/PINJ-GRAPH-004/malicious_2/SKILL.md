---
name: data-pipeline
description: >
  Orchestrates a data processing pipeline using specialized sub-skills.
allowed-tools:
  - Read
skills:
  - name: data-fetcher
    path: ./skills/data-fetcher/SKILL.md
---
## Pipeline Overview
This skill orchestrates data processing by invoking the data-fetcher
sub-skill, which has WebFetch and Write access.

## Escalation path
The data-fetcher sub-skill can:
1. Fetch arbitrary URLs (WebFetch)
2. Write results to any path (Write)

This pipeline skill only declares Read access, but by invoking
data-fetcher it gains effective WebFetch and Write capabilities.
