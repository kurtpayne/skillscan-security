# Policy Guide

SkillScan ships with built-in profiles:

1. `strict` (default)
2. `balanced`
3. `permissive`

Custom policy files can override thresholds, rule weights, and local domain allow/block controls.

Minimal custom policy example:

```yaml
name: strict-custom
description: Example
thresholds:
  warn: 40
  block: 90
weights:
  malware_pattern: 3
  instruction_abuse: 2
  exfiltration: 3
  dependency_vulnerability: 2
  threat_intel: 3
  binary_artifact: 1
hard_block_rules:
  - MAL-001
  - IOC-001
allow_domains:
  - trusted.internal.example
block_domains:
  - blocked.example
limits:
  max_files: 4000
  max_depth: 8
  max_bytes: 200000000
  timeout_seconds: 60
```

Use a custom policy:

```bash
skillscan scan ./target --policy ./my_policy.yaml
```
