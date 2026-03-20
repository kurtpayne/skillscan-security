---
name: ux-case-study
description: Transforms raw UX project notes into structured case study narratives optimized for senior product design interviews and stakeholder presentations. Builds the story using a 6-beat structure, then applies a persuasion layer — calibrating language to the audience, weaving in preemptive answers to likely objections, and verifying the narrative can hold up across multiple interview rounds. Use when the user provides project notes or asks to build a case study story. The output is a spoken narrative — not a slide deck or written report.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: gattoa/ux-writer
# corpus-url: https://github.com/gattoa/ux-writer/blob/5acc3823042f4f32f24acea107d1c4251acfbd40/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# UX Case Study Narrative Builder

## Workflow

1. **Ingest and clean the notes.** The user's raw notes may contain placeholder instructions or coaching prompts they used to populate the data (e.g., "add a note about stakeholder alignment here"). Strip these out. Extract only factual project content: what happened, who was involved, what the constraints were, what evidence exists.

2. **Confirm the audience context.** Ask which level they are interviewing for: Senior, Lead, Staff, or Principal Product Designer. Design stakeholders (senior designers, design directors) are assumed to be present in the panel concurrently — their quality criteria run alongside the level-specific criteria and both must be satisfied. See `references/audience_persuasion.md` for how this works.

3. **Read both references.** Load `references/narrative_framework.md` (story structure, seniority calibration, metrics gap handling, tone rules, annotated example) and `references/audience_persuasion.md` (audience language mapping, preemption check, weave techniques, multi-round durability).

4. **Build the narrative skeleton.** Produce the narrative following the 6-beat structure from narrative_framework.md. Apply the correct seniority calibration. Follow tone and language rules. This is the structural layer.

5. **Apply the persuasion layer.** Using audience_persuasion.md: (a) Translate key phrases into the audience's vocabulary — their words, not yours. (b) Run the preemption check — go through the likely objections for this audience and verify each one is quietly answered somewhere in the narrative. Where it isn't, weave in a preemptive answer using the technique guide. Every weave must sound like natural storytelling, not a defensive insertion. (c) Run the multi-round durability check — verify the four depth threads (decision, people, constraint, outcome) are supported by the source material. Flag any thread that is thin or missing; the user will be vulnerable there in later rounds.

6. **Deliver.** Output the narrative as plain text. No headers, no bullet points, no section labels. Just the story, the way it would be spoken. After the narrative, include a brief flagged list of any depth threads that need attention for later rounds — but keep this separate and clearly marked as a prep note, not part of the narrative itself.

## Key rules

- Business problem must come before any design work is mentioned.
- If the notes lack production analytics, handle it using beat 5 of the framework — do not skip it or bury it.
- If the notes lack a clear business problem, ask the user before proceeding. Do not invent one.
- If the notes are thin on organizational complexity, flag it. At Lead level and above, this is the centerpiece of the story.
- Never fabricate data. If a number isn't in the notes, say so and ask whether to estimate or leave it out.
- The narrative must use vocabulary that matches the audience. If the audience is a PM, "retention risk" not "user frustration." If an engineering lead, "implementation constraint" not "it was complicated." See audience_persuasion.md for full mapping.
- Preemptive answers must sound natural. If a weave sounds defensive or out of place, it is wrong. Find a different insertion point or technique.
- For multi-round interviews: flag any depth thread missing from the source material. The user needs to know what they'll be vulnerable on before the next round.
- The narrative should make the solution feel inevitable — by the time the design is described, the listener should already understand why that was the right move.
- Output length should feel like a 3–5 minute spoken narrative. Not longer.