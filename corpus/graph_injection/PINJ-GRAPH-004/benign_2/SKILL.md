---
name: report-generator
description: >
  Generates reports by coordinating read and write sub-skills.
  All sub-skills are scoped to the same permissions as this skill.
allowed-tools:
  - Read
  - Write
skills:
  - name: data-reader
    path: ./skills/data-reader/SKILL.md
  - name: report-writer
    path: ./skills/report-writer/SKILL.md
---
## Report Generator
Coordinates data reading and report writing sub-skills.
Both sub-skills are scoped to Read and Write only, matching this skill's
declared permissions. No sub-skill has broader access than this skill.
