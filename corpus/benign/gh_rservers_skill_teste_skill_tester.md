---
name: skill-tester
description: "Skill vetting workflow. Each model provider separately vets skills and produces independent reports. Use when: (1) vetting skills from GitHub repos, (2) having each model independently evaluate a skill, (3) generating per-model vetting reports, (4) comparing model interpretations."
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
      },
  }
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: rservers/skill-tester
# corpus-url: https://github.com/rservers/skill-tester/blob/d29e1529f74469d25acfa7287b2c0a5e50a46e0e/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Skill Vetting Workflow

Each model independently vets skills and produces its own detailed report. No cross-model comparison.

## Model Providers

```json
{
  "minimax-portal": "MiniMax-M2.5",
  "openai-codex": "gpt-5.3-codex"
}
```

## Workflow

### For Each Model:

1. **Spawn subagent** with that model's config
2. **Run vetting process** - validate skill structure, quality, content
3. **Generate independent report** - model's own assessment

### Vetting Criteria (Per Model)

| Area | Description |
|------|-------------|
| **Structure** | Valid YAML, required fields present |
| **Completeness** | All sections included, well-documented |
| **Quality** | Clear instructions, actionable steps |
| **Safety** | No dangerous commands or patterns |
| **Usability** | Clear examples, proper formatting |

### Per-Model Report Template

```markdown
# Skill Vetting Report
**Model:** [Model Name]
**Skill:** [Skill Name]
**Date:** [Date]

---

## Validation

| Check | Status |
|-------|---------|
| YAML Frontmatter | ✅/❌ |
| Name Field | ✅/❌ |
| Description | ✅/❌ |
| Tool References | ✅/❌ |
| Dangerous Patterns | ✅/❌ |

---

## Quality Assessment

### Strengths
- [Model's assessment]

### Weaknesses  
- [Model's assessment]

### Recommendations
- [Model's suggestions]

---

## Verdict

**Vetting Status:** APPROVED / NEEDS REVISION / REJECTED

[Model's final verdict and reasoning]
```

### Example Output

```markdown
# Skill Vetting Report
**Model:** MiniMax-M2.5
**Skill:** opportunity-solution-tree
**Date:** 2026-03-16

---

## Validation

| Check | Status |
|-------|---------|
| YAML Frontmatter | ✅ |
| Name Field | ✅ |
| Description | ✅ |
| Tool References | ⚠️ None (documentation only) |
| Dangerous Patterns | ✅ None found |

---

## Quality Assessment

### Strengths
- Excellent framework alignment with Teresa Torres methodology
- Clear 4-level structure
- Practical experiment suggestions
- Good customer-centric language

### Weaknesses
- Could use more tool references for automation
- Some sections could have more examples

### Recommendations
- Add code examples for implementation
- Include common pitfalls section

---

## Verdict

**Vetting Status:** APPROVED ✅

Strong skill, production-ready with minor improvements possible.
```

## Process

1. For each skill to vet:
   - Spawn subagent with Model A → Generate Report A
   - Spawn subagent with Model B → Generate Report B
2. Store each report independently
3. Present each model's findings separately

## Usage

1. **"Vet skill opportunity-solution-tree with all models"**
   - Each model produces independent report

2. **"Vet all discovery skills with MiniMax"**
   - MiniMax vets each discovery skill

3. **"Show me GPT-5.3's vetting report for brainstorm-ideas"**
   - Show specific model's assessment