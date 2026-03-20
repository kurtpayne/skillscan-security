---
name: citation-assistant
description: Add verified citations to academic papers and proposals. Use when working on LaTeX documents that need citations, finding papers for a specific section, verifying existing citations, or when user mentions "cite", "citation", "references", "bibliography", or asks to find related work. Supports Semantic Scholar API, Exa MCP, and DOI-based BibTeX retrieval. Never hallucinate citations. Invoke with /citation-assistant or /citation-assistant [section].
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: chrisliu298/citation-assistant
# corpus-url: https://github.com/chrisliu298/citation-assistant/blob/84eda81bb13eb53ac4ddbb6eded65d6185c79435/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Citation Assistant

Add verified citations to academic LaTeX documents. Identify citation gaps, search for relevant papers, verify their existence, and add properly formatted BibTeX entries.

## CRITICAL: No Hallucinated Citations

**All citations MUST be real, verified papers.** Hallucinated or fabricated citations are absolutely not tolerated - they constitute academic misconduct and can result in paper rejection or retraction.

- NEVER generate BibTeX from memory
- ALWAYS verify papers exist via API or web search before citing
- If you cannot verify a paper, mark it as `[CITATION NEEDED]` - do NOT guess
- When in doubt, leave it out

## Context

- Bibliography files: !'find . -maxdepth 3 -name "*.bib" 2>/dev/null | head -20 || echo "No .bib files found"'
- LaTeX sections: !'grep -rh "\\\\section{" *.tex 2>/dev/null | head -20 || echo "No .tex files found"'

## Invocation

```
/citation-assistant                     # Ask user which section needs citations
/citation-assistant [section]           # Add citations to specified section (e.g., "introduction", "related work")
/citation-assistant verify              # Verify all existing citations in the document
```

## Workflow

### 1. Identify Target Section

When invoked:
- If section argument provided: Read that section from the LaTeX file
- If no argument: Use AskUserQuestion to ask "Which section needs citations?"
  - Offer sections found in the document (scan for `\section{...}`)

### 2. Identify Citation Gaps

Read the section and identify:
- Claims without citations
- Broad claims with insufficient citations (single citation for major claims)
- Methods/techniques missing original paper references
- Comparisons to prior work without references

**List gaps to user before searching** - Show each claim and why it needs a citation.

### 3. Search for Papers

For each gap, use **multiple search methods** to ensure broad coverage:

1. **Check existing bibliography first** - Search the project's .bib file(s)

2. **Search using ALL available tools** (not just one):
   - Exa MCP (if available) - semantic search, good for conceptual queries
   - Semantic Scholar API - comprehensive academic database
   - Web search - catches recent preprints and non-indexed papers

   **Run searches in parallel when possible.** Different tools have different coverage - a paper missing from one source may appear in another.

3. **Aggregate and deduplicate results** - Merge results from all sources

4. **Verify each paper** exists in 2+ sources before citing

5. **Fetch BibTeX via DOI** - Never generate from memory

### 4. Add Citations

- Append new entries to .bib file
- Insert citation commands matching the document's style (`\cite{}`, `\citep{}`, `\citet{}`, etc.)
- Report what was added

## Citation Rules

| Situation | Action |
|-----------|--------|
| Found paper, got DOI | Fetch BibTeX via DOI, add citation |
| Found paper, no DOI | Use arXiv BibTeX or construct from verified metadata |
| Cannot verify paper | Mark as `[CITATION NEEDED]`, inform user |
| "I think there's a paper about X" | Search first, never guess |

**Never hallucinate citations.** If verification fails at any step, mark the citation as needing manual verification.

## BibTeX Format

```bibtex
@article{author2024keyword,
  title={Title with {Acronyms} Protected},
  author={Last, First and Last2, First2},
  journal={arXiv preprint arXiv:XXXX.XXXXX},
  year={2024}
}

@inproceedings{author2024conf,
  title={Title Here},
  author={Last, First},
  booktitle={Proceedings of NeurIPS},
  year={2024}
}
```

- Key format: `author_year_keyword`
- Protect acronyms with braces: `{LLM}`, `{GPU}`, `{BERT}`
- Use `and` between authors

## Python Environment

When running Python code for citation lookups:

1. Create a virtual environment if needed: `uv venv`
2. Activate it: `source .venv/bin/activate`
3. Install dependencies: `uv add semanticscholar requests`

Never use the system Python directly.

## APIs

See [references/apis.md](references/apis.md) for Semantic Scholar and DOI lookup code.

## Output

For each citation added, report:
1. The claim being supported
2. Paper title and authors
3. Why this paper is relevant
4. The BibTeX key added