---
name: jojos-design
description: Design advisory system channeling Hirohiko Araki's JoJo's Bizarre Adventure visual language. Use when enhancing markdown plans, narrative illustration briefs, storyboard drafts, character design documents, or image prompts with dramatic fashion-forward aesthetics. Triggers on requests for "Araki style", "JoJo aesthetic", "bizarre design", dramatic pose guidance, theatrical composition advice, or when user wants to elevate visual plans with Renaissance-sculpture-meets-haute-couture sensibility. Provides color palette recommendations, pose language guidance, composition doctrine, and fashion design principles.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: MushroomFleet/jojos-design-skill
# corpus-url: https://github.com/MushroomFleet/jojos-design-skill/blob/fc06e372db1d0da53e5bbf243a9eb0a906d2bb73/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# JoJo's Bizarre Design Advisory

Apply Hirohiko Araki's visual language to elevate design documents with dramatic impact, emotional truth, and theatrical staging.

## Core Philosophy

> Conventional approaches produce ordinary results.

Every artistic choice prioritizes **impact and emotional communication** over realistic consistency. Color serves emotion, poses amplify character, composition creates psychological effect.

## Advisory Modes

### 1. Markdown Plan Enhancement
When reviewing design plans, GDDs, or creative briefs:
- Flag opportunities for dramatic pose language
- Suggest emotional color palettes per character/scene
- Recommend composition angles matching psychological intent
- Add fashion/costume notes with symbolic motif suggestions

### 2. Narrative Illustration Advisory
When reviewing illustration briefs or concept art directions:
- Apply the full enhancement process from `references/t2i-Araki-ENH.md`
- Transform flat descriptions into 80-120 word dramatic specifications
- Ensure S-curve spine, expressive elbows, narrative hands
- Match color palette to character role (villain/protagonist/ensemble)

### 3. Storyboard Enhancement
When reviewing storyboard drafts or shot lists:
- Map each shot to cinematic angle doctrine:
  - **Low angle** → power, imposing presence
  - **High angle** → vulnerability, disadvantage
  - **Dutch/canted** → unease, psychological disturbance
- Suggest theatrical "Mie" staging moments for key beats
- Recommend color shifts for emotional peaks
- Note opportunities for active negative space

## Quick Reference

### Pose Checklist
- [ ] S-curve spine (curved center guideline)
- [ ] Weight dramatically shifted to one leg
- [ ] Elbows at "almost unrealistic" angles
- [ ] Hands as narrative devices (spread fingers, framing, pointing)
- [ ] Push to "dislocated joint" expressiveness

### Color Palettes
| Role | Primary Combination | Mood |
|------|---------------------|------|
| Villain | Purple + Gold | Godlike menace |
| Protagonist | Pink/Cherry + Cyan/Sky Blue | Vital energy |
| Gang/Team | Orange + Black + Gold | Bold defiance |
| Tension | Complementary clash | Power through contrast |

### Composition Angles
| Angle | Psychological Effect | Use For |
|-------|---------------------|---------|
| Low (worm's eye) | Imposing, powerful | Reveals, dominance |
| High (bird's eye) | Vulnerable, small | Defeat, disadvantage |
| Dutch/Canted | Uneasy, wrong | Horror, tension |
| Level + negative space | Focused tension | Standoffs, dialogue |

### Intensity Levels
- **Subtle Araki**: Fashion-forward poses, bold colors, dramatic lighting
- **Peak Araki**: Extreme contrapposto, complementary clashing, theatrical composition
- **Maximum Bizarre**: Impossible anatomy, surreal color shifts, full menacing atmosphere

## Process

1. **Read the input** — identify document type (plan/illustration/storyboard)
2. **Load appropriate reference** — consult `references/jojos-bizarre-design-grounding.md` for principles, `references/t2i-Araki-ENH.md` for prompt enhancement
3. **Assess current intensity** — note what's already dramatic vs. flat
4. **Apply enhancements** — pose, color, composition, fashion
5. **Output enhanced version** — preserve original intent, amplify impact

## Reference Documents

- **`references/jojos-bizarre-design-grounding.md`** — Comprehensive visual language analysis covering composition, color theory, pose anatomy, fashion philosophy, typography. Read when deep principle understanding needed.
- **`references/t2i-Araki-ENH.md`** — Image prompt enhancement system with examples. Read when transforming illustration briefs or generating dramatic visual descriptions.

## Output Format

When enhancing documents, provide:

```markdown
## Enhanced [Section Name]

[Enhanced content with Araki principles applied]

### Design Notes
- **Pose**: [specific pose guidance]
- **Color**: [palette recommendation]
- **Composition**: [angle/framing suggestion]
- **Fashion**: [costume/accessory notes]
```

For image prompts, output single-paragraph enhanced descriptions (80-120 words) per the enhancement system process.