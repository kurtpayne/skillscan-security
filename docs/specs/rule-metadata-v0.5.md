# Spec: Rule Metadata Schema (v0.5-compatible)

## Goal
Add optional metadata to rules without breaking existing rule IDs or YAML format.

## Compatibility contract
- Existing rules remain valid with no changes.
- New metadata fields are optional in v0.5.
- Parser ignores unknown metadata keys in v0.5 (forward compatible).

## Proposed rule shape (additive)

```yaml
- id: OBF-003
  category: instruction_abuse
  severity: high
  confidence: 0.87
  title: Unicode PUA obfuscation near dynamic execution sink
  pattern: '...'
  mitigation: '...'

  metadata:
    version: 1.0.0
    status: active                  # active|deprecated|experimental

    techniques:
      - id: EVASION-001
        name: Invisible Unicode obfuscation

    tags: [unicode, obfuscation, dynamic-exec]

    applies_to:
      languages: [javascript, typescript, python]
      file_types: [.js, .ts, .py, .md, .yml]
      contexts: [source, workflow, prompt]

    lifecycle:
      introduced: "2026-03-16"
      last_modified: "2026-03-16"
      deprecates: []
      superseded_by: []

    quality:
      precision_estimate: 0.90
      recall_estimate: 0.70
      benchmark_set: adversarial-v3
      false_positive_notes: May trigger when eval appears in non-executing demos.

    references:
      - https://example.org/campaign-report
```

## Minimal required in v0.5 (for new rules)
- `metadata.version`
- `metadata.status`
- `metadata.techniques[]`
- `metadata.tags[]`

Everything else is optional.

## Migration plan

### Phase 1 (v0.5)
- Add parser support for `metadata` object.
- Backfill metadata only for newly added rules.
- Emit metadata in JSON/SARIF outputs when present.

### Phase 2 (v0.6)
- Backfill top ~30 high-signal rules.
- Add filtering by technique/tag (`--technique`, `--tag`).

### Phase 3 (v0.7)
- Technique coverage reporting (`skillscan report coverage`).
- Deprecation/supersession warnings in CLI output.

## Scoring/usage behavior
- Scoring stays rule-based in v0.5 (no behavior change).
- Technique metadata is for reporting/filtering/policy grouping.
- For overlap, allow many-to-many mappings and dedupe per finding per technique in dashboards.
