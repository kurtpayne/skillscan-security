# SkillScan Security — Corpus Card

This document describes the training corpus used to fine-tune the
`kurtpayne/skillscan-deberta-adapter` prompt-injection detection model.
It is updated automatically by `scripts/finetune_modal.py` on each fine-tune run.

---

## Corpus Structure

```
corpus/
  benign/           ← Legitimate skill files (label: 0)
  prompt_injection/ ← Prompt-injection attack examples (label: 1)
  malicious/        ← Malware / supply-chain attack examples (label: 1)
  manifest.json     ← SHA-256 fingerprints of every file + fine-tune history
  CORPUS_CARD.md    ← This file
```

## Current Snapshot

| Field | Value |
|-------|-------|
| Total examples | 111 |
| Benign (label 0) | 54 |
| Injection + Malicious (label 1) | 57 |
| Corpus SHA-256 | `c68ec511fbd186b07b3c4b440dca61c6c30f33b746457d464e0f173d93e61a15` |
| Git commit | [`29b05e5`](https://github.com/kurtpayne/skillscan-security/commit/29b05e5594fbe8fd3bb249ceca490da760548583) |
| Last updated | 2026-03-18 |

## Source Breakdown

| Source | Category | Count | Notes |
|--------|----------|-------|-------|
| Hand-crafted | benign | 4 | Curated by maintainers |
| Synthetic (seed_corpus.py) | benign | 50 | Generated across 15 skill domains |
| Hand-crafted | prompt_injection | 43 | Full SKILL.md format, diverse attack vectors |
| Adversarial test suite | malicious | 14 | From `tests/adversarial/cases/` |
| **Total** | | **111** | ~1:1 benign/injection balance |

## Attack Vectors Covered

The 43 hand-crafted injection examples cover:

- Role/persona override (description, notes, metadata fields)
- Context extraction and prompt leakage
- Fake tool output / fake system headers
- Indirect injection via external data (RSS, calendar, email)
- Credential and data exfiltration (env vars, SSH keys, DNS)
- Supply chain and dependency abuse
- Social engineering via prerequisites
- Obfuscation (Unicode homoglyphs, zero-width chars, base64)
- Malware patterns (reverse shell, crypto drainer, AMOS-style stealer)
- Metadata field injection (version, author, tags, license)
- YAML/Markdown structure abuse (block scalars, fake XML tags)
- Permission escalation
- Context flooding (token limit exhaustion)
- Backdoor via update mechanism
- DAN-style jailbreak in notes

## Reproducibility

Every fine-tune run records:
- Git commit SHA of `skillscan-security` at training time
- SHA-256 of the full corpus directory
- Label distribution
- Training hyperparameters

To reproduce any fine-tune:
```bash
git checkout <commit-sha>
pip install 'skillscan-security[ml]'
python scripts/finetune_modal.py --force
```

The corpus manifest (`manifest.json`) contains the SHA-256 fingerprint of every
file at the time of the last sync. The model card on HuggingFace Hub links back
to the specific git commit used for training.

## Fine-Tune History

| Date | Corpus Size | Benign | Injection | Corpus SHA (first 16) | Model Version | Commit |
|------|-------------|--------|-----------|----------------------|---------------|--------|
| 2026-03-18 | 113 | 54 | 57 | `60f3a2d3e77a5d2e` | 113-3ep | [`d644f44`](https://github.com/kurtpayne/skillscan-security/commit/d644f44974f79887f66fe75577ee9637adb0d898) |
| 2026-03-18 | 119 | 54 | 57 | `bac8b25df7d89ac0` | 119-3ep | [`73d5ca4`](https://github.com/kurtpayne/skillscan-security/commit/73d5ca41f1a7ecdf091679cd93fe2c762c78135e) |

---

## Scheduled Updates

The corpus grows automatically via the `corpus-sync.yml` GitHub Actions workflow
which runs twice daily (06:00 and 18:00 UTC). On each run it:

1. Scrapes `openclaw/skills` for newly flagged malicious skills
2. Searches security news for new prompt-injection patterns
3. Adds new examples to `corpus/prompt_injection/` or `corpus/malicious/`
4. Opens a PR with a summary of what was added

A fine-tune is dispatched to Modal when the corpus delta threshold is crossed
(≥50 new examples **and** ≥10% growth, at most once per 7 days).

## License

All hand-crafted examples are original works by the SkillScan maintainers and
are released under the same license as the `skillscan-security` repository.
Scraped examples from ClawHub retain their original licenses; see individual
file headers for attribution.
