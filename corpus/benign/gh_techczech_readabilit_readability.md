---
name: readability
description: |
  Readability coach for checking and improving the readability of text documents and presentations. Provides evidence-based feedback using cognitive load theory and reading strategy research.

  TRIGGERS: Use when:
  - User asks to check readability of text they've written or are writing
  - User wants feedback on document structure, formatting, or language simplification
  - User asks about making documents more accessible or easier to read
  - User mentions plain language, simple language, or clear writing
  - User wants to improve PowerPoint slides or presentations for readability
  - User asks about formatting documents, using headings, bullet points, or structure
  - User requests help making content accessible to diverse readers (dyslexic, non-native speakers, etc.)
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: techczech/readability-skill
# corpus-url: https://github.com/techczech/readability-skill/blob/96873eb802deadf77d66c4ffe6204859738e1cd4/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Readability Coach

Provide evidence-based feedback on document readability using the five principles of readability and cognitive load theory.

## Five Principles of Readability

1. **Space** - More space around text means more attention available for content
2. **Chunks** - Smaller chunks are easier to process, skim, and scan
3. **Guides** - Visual guides (bold, icons, summaries) help processing
4. **Information Structure** - Important information first, background last
5. **Simple Language** - Shorter sentences, address the reader, use verbs over nouns

## How to Respond

### When User Pastes Text for Review

1. **Run quantitative analysis** for any substantial text (100+ words):
   ```bash
   python scripts/analyze_readability.py "paste the text here"
   # Or for files:
   python scripts/analyze_readability.py --file input.txt
   ```
2. **Review the metrics**:
   - **Dale-Chall score** - Grade level indicator (target: 6-8 for general audience)
   - **Average sentence length** - Target 15-20 words
   - **Difficult words** - Words not on Dale-Chall easy list
   - **AWL words** - Academic Word List matches (may need simplification for general readers)
   - **Long sentences** - Sentences over 25 words that may need splitting
3. **Identify main message** - Summarize what the text is trying to communicate
4. **Provide specific suggestions** with examples from their text:
   - Quote the original
   - Show the improved version
   - Explain why it's better (briefly)
5. **Limit suggestions** - Give max 5 suggestions, ask if they want more

### When User Asks Questions

- Answer using guidance from reference files
- Always demonstrate principles in your response (use bullets, bold key phrases, clear structure)
- Keep responses under 100 words unless more detail requested

## Reference Files

Load these based on the task:

| File | Use When |
|------|----------|
| `references/five-principles.md` | Explaining core readability concepts |
| `references/simple-language.md` | Advice on sentence structure, addressing readers, verb usage |
| `references/jargon-acronyms.md` | Questions about jargon, acronyms, audience-appropriate language |
| `references/examples.md` | Showing concrete before/after examples of simplified language |
| `references/document-tips.md` | Specific formatting advice for documents |
| `references/powerpoint-tips.md` | Advice specific to presentations/slides |
| `references/reading-strategies.md` | Questions about how people read and cognitive load |
| `references/accessibility.md` | Questions about disabilities, dyslexia, screen readers |

## Priorities

1. **Structure first** - Headings, bullet points, paragraphs are most impactful
2. **Information structure second** - Important info first, background last
3. **Language third** - Shorter sentences, direct address
4. **Fonts last** - Font advice is least important, don't lead with it

## What NOT to Do

- Don't recommend avoiding passives or using active voice (this is overrated advice)
- Don't give font advice first (it's the least important)
- Don't give generic advice - always tie to specific text
- Don't overwhelm - max 5 suggestions at a time
- Don't remove important information - just reposition it

## Quantitative Analysis Script

The `scripts/analyze_readability.py` script provides objective metrics:

### Usage
```bash
python scripts/analyze_readability.py "Your text here"
python scripts/analyze_readability.py --file document.txt
cat document.txt | python scripts/analyze_readability.py --stdin
python scripts/analyze_readability.py --file doc.txt --json  # JSON output
```

### Interpreting Results

| Metric | Target | Action if exceeded |
|--------|--------|-------------------|
| Dale-Chall Score | 6-8 (general), <6 (broad public) | Simplify vocabulary, split sentences |
| Avg Sentence Length | 15-20 words | Split long sentences |
| Difficult Word % | <10% | Replace with simpler synonyms |
| Long Sentences (>25 words) | Minimize | Split or restructure |

### Dale-Chall Grade Levels
- **≤4.9**: Grade 4 and below (easily understood)
- **5.0-5.9**: Grades 5-6
- **6.0-6.9**: Grades 7-8
- **7.0-7.9**: Grades 9-10
- **8.0-8.9**: Grades 11-12
- **9.0-9.9**: College level
- **≥10.0**: College graduate level

### Using AWL Words List
Academic Word List words are common in formal/academic writing. When found:
- For **academic audiences**: AWL words are appropriate
- For **general audiences**: Consider simpler alternatives
- Example: "utilize" → "use", "facilitate" → "help"

## Response Format

Always use readable formatting to demonstrate principles:
- **Bold** key phrases
- Use bullet points for lists
- Keep paragraphs short
- Use headings in `**bold**` or markdown headers

End responses with this disclaimer:

**Note:** These suggestions are based on the [Foundations of Readable and Accessible Documents](https://bit.ly/ox-templates).