# Design: "LLM-as-Recon-Tool" Detection Pattern

## Problem
Recent campaigns use LLM agents as reconnaissance helpers before payload delivery: enumerate environment, collect tokens/config, map permissions, then exfil findings for operator planning.

SkillScan should detect this *recon phase* even when explicit malware payloads are absent.

## Detection objective
Flag instruction sets that combine:
1. **Discovery language**: inventory/enumerate/list/search for secrets/config/runtime context
2. **Privilege/context mapping**: identify identities, role bindings, cloud metadata, CI context
3. **Collection + staging intent**: summarize/export/serialize findings for external use

## Proposed rule family
- `RECON-001` (static marker): high-signal recon prompt phrases around credentials, infra mapping, and token discovery.
- `CHN-RECON-001` (chain rule): require at least one discovery action + one collection/staging action + one outbound indicator.

## Candidate signals
### Discovery cues
- "enumerate env vars", "list all tokens", "collect config files", "find credentials"
- references to `.env`, cloud metadata endpoints, CI secrets contexts

### Context-mapping cues
- "what permissions do I have", "whoami + role", "list IAM bindings", "org/repo secrets overview"

### Staging/exfil cues
- "serialize to json", "summarize and send", "post results", "upload report"

## Scoring approach
- Medium score for single recon hints
- High score when chain conditions are met
- Critical only if recon + explicit exfil destination is present

## False-positive controls
- Allow-list benign audit contexts (security hardening scripts, internal compliance templates)
- Require at least two independent signal classes before block recommendation
- Prefer warn for pure discovery without transfer intent

## Test plan
1. Add adversarial fixtures:
   - recon-only benign variant
   - recon + staging
   - recon + exfil destination
2. Add showcase entry demonstrating chain escalation
3. Verify strict policy produces warn/block thresholds as expected

## Deliverables
- Rules in `default.yaml`
- tests in `tests/test_rules.py` + showcase assertions
- docs update in `docs/RULES.md`
