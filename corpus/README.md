# SkillScan Corpus

The training corpus has moved to the private **[skillscan-corpus](https://github.com/kurtpayne/skillscan-corpus)** repository.

This directory is intentionally empty in `skillscan-security`. The corpus-sync CI workflow clones `skillscan-corpus` at runtime to access labeled training data.

## What lives in skillscan-corpus

| Directory | Contents |
|---|---|
| `training_corpus/` | Labeled SKILL.md examples (benign, malicious, agent_hijacker, etc.) |
| `adversarial/` | Adversarial evasion variants |
| `jailbreak_distillations/` | Jailbreak family distillations |
| `held_out_eval/` | Held-out evaluation set |
| `scripts/` | Fine-tune scripts, corpus expansion tools |
| `docs/` | CORPUS_EXPANSION.md, PROMPT_INJECTION_CORPUS.md |

## Access

Contact @kurtpayne for corpus access. The fine-tune pipeline is fully automated via the `corpus-sync` GitHub Actions workflow.
