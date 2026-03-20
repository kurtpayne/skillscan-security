---
name: paper-presentation
description: Generate rigorous mathematical HTML presentations from academic papers. Use when the user wants to create a presentation from a paper, convert arXiv LaTeX to slides, build educational content from research papers, or asks to explain a paper with full mathematical rigor. Triggers on requests involving paper explanation, arXiv presentation, theorem exposition, or mathematical pedagogy from research.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: rnkarmakar/rnkarmakar.github.io
# corpus-url: https://github.com/rnkarmakar/rnkarmakar.github.io/blob/279876c0b646045cc9de69d3f47279ee0bbe08c3/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Paper Presentation Generator

Transform academic paper LaTeX source into comprehensive, mathematically rigorous HTML presentations suitable for audiences with no assumed domain knowledge.

## Inputs Required

1. **Paper source**: LaTeX source from arXiv (URL or pasted content)
2. **HTML template**: Optional custom template, or use [assets/presentation-template.html](assets/presentation-template.html)

## Workflow Overview

Execute phases sequentially. For detailed instructions on each phase, see [references/workflow-phases.md](references/workflow-phases.md).

### Phase 1: Input Collection

Collect and validate inputs:
- If arXiv URL provided, fetch LaTeX source via web
- If template not provided, use default from assets/
- Extract paper title, authors, abstract for context

### Phase 2: Paper Analysis

Extract mathematical structure:
- List all theorems, propositions, lemmas, corollaries
- List all definitions
- Identify the main results (typically 1-3 key theorems)
- Map concept dependencies (which definitions feed into which theorems)

### Phase 3: Literature Research

For each core concept in the paper:
- Search for the concept's origin in mathematical literature
- Identify seminal papers introducing the concept
- Trace evolution through key milestones to the form used in this paper
- Collect citations for the timeline

### Phase 4: First-Principles Evolution

Build concept chains from basics to paper's formulation:
- Start from undergraduate-level foundations (analysis, probability, linear algebra, etc.)
- Define each intermediate concept rigorously
- Show how concepts compose to reach paper's definitions
- Ensure zero assumed domain knowledge

### Phase 5: Main Results Compilation

For each main result:
- State the theorem with ALL hypotheses explicitly listed
- Number conditions (C1), (C2), etc. for reference
- Explain what each condition means intuitively
- Highlight which conditions are typically hardest to verify

### Phase 6: Example Applications

If the paper has applications:
- List concrete example scenarios
- For each example, work through completely:
  - Define the example setup
  - Verify condition (C1) explicitly with computation
  - Verify condition (C2) explicitly with computation
  - (Continue for all conditions)
  - Apply the theorem
  - State the conclusion

### Phase 7: Key Technical Ideas Extraction

Before writing proof sketches:
- Scan all proofs for repeated lemmas, inequalities, or techniques
- Gather these "workhorse" results into a Key Technical Tools section
- State each tool rigorously with its conditions
- See [references/proof-sketch-guide.md](references/proof-sketch-guide.md)

### Phase 8: Proof Sketch Generation

For each proof:
- Decompose into principled steps (each step natural from previous)
- Classify each step: **technical** or **routine**
- For **routine** steps:
  - State only the result derived (equation/inequality/expression)
  - Mark as "routine computation" or "standard estimate"
  - Do NOT include the computation
- For **technical** steps:
  - Explain the key insight or principle
  - Cite the mathematical principle used (even from other branches)
  - Reference Key Technical Tools when applicable

See [references/proof-sketch-guide.md](references/proof-sketch-guide.md) for classification criteria.

### Phase 9: HTML Generation

Generate single self-contained HTML file:
- Use template structure from assets/
- Add MathJax macros for all custom LaTeX commands from paper
- Apply notation management rules from [references/notation-management.md](references/notation-management.md)
- Structure: Summary → Concept Evolution → Main Results → Examples → Key Tools → Proof Sketches

### Phase 10: Verification Loop

Execute iterative refinement:

```
success_count = 0
while success_count < 3:
    # Spawn verifier subagent
    verification = verify_output(html_output, criteria_from_references)
    
    if verification.all_pass:
        success_count += 1
    else:
        success_count = 0
        refinement_prompt = verification.suggested_refinements
        # Spawn refiner subagent
        html_output = refine_output(html_output, refinement_prompt)

return html_output
```

See [references/verification-criteria.md](references/verification-criteria.md) for the complete checklist.

## Output Format

Single HTML file containing:
- All CSS inline in `<style>` tags
- All JavaScript (MathJax config) inline in `<script>` tags
- Complete mathematical content with proper MathJax rendering
- Sections clearly delineated with headers

## Critical Rules

1. **No assumed knowledge**: Define everything from first principles
2. **Notation accessibility**: Never use a symbol >2 sections after definition without reminder
3. **Explicit conditions**: Every theorem must list ALL conditions numbered
4. **Rigorous examples**: Every example must verify ALL theorem conditions
5. **Principled proofs**: Every proof step must be natural from the previous
6. **Technical honesty**: Mark routine steps as routine, but state results precisely

## Additional Resources

- [references/workflow-phases.md](references/workflow-phases.md) - Detailed phase instructions
- [references/verification-criteria.md](references/verification-criteria.md) - Verifier checklist
- [references/proof-sketch-guide.md](references/proof-sketch-guide.md) - Proof classification guide
- [references/notation-management.md](references/notation-management.md) - Symbol accessibility rules
- [assets/presentation-template.html](assets/presentation-template.html) - Base HTML template