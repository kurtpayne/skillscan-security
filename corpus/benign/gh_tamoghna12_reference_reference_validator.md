---
name: reference-validator
description: Validate and correct DOIs in academic references, check citation accuracy, verify reference lists, and identify fake or incorrect DOIs. Use this skill whenever the user mentions validating references, checking DOIs, correcting citations, verifying bibliographies, reviewing reference lists for publication, identifying citation errors, or needs to ensure reference accuracy before submitting manuscripts. Also trigger when users have reference files with potential DOI issues, need to verify DOIs in papers, or want to check if their references are real and correctly formatted.
compatibility: python3, requests library
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Tamoghna12/reference-validator-skill
# corpus-url: https://github.com/Tamoghna12/reference-validator-skill/blob/faab78ad642c6fb5f2e05b76371d12d95e069683/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Reference Validator

Validate and correct DOIs in academic reference lists. This skill helps researchers, students, and academics ensure their references are accurate and publication-ready.

## When to Use This Skill

Use this skill when:
- Validating DOIs in reference lists before manuscript submission
- Checking if references in a paper are real and correctly formatted
- Correcting incorrect DOIs in bibliographies
- Verifying citation accuracy for literature reviews
- Identifying fake or suspicious references
- Preparing reference lists for publication
- Checking reference quality for systematic reviews
- Validating DOIs in grant applications or theses

## Core Workflow

### 1. Assess the Input

First, examine the reference file:
- **Format**: Identify if it's markdown (.md), BibTeX (.bib), RIS (.ris), or plain text (.txt)
- **Structure**: Check how references are formatted (numbered, bulleted, etc.)
- **DOI format**: Look for DOI patterns (10.xxxx/xxxxx)
- **File size**: Large files (>100 references) may need batching

### 2. Extract and Validate DOIs

For each reference in the file:

1. **Extract the DOI** using regex pattern: `10\.\d{4,}/[^\s\]\'">\}]+`
2. **Clean the DOI** by removing trailing punctuation and whitespace
3. **Validate via Crossref API**:
   ```python
   import requests
   doi = "10.1038/nature12345"  # Example
   url = f"https://api.crossref.org/works/{doi}"
   response = requests.get(url, timeout=10)
   is_valid = response.status_code == 200
   ```

4. **Extract metadata** if valid:
   - Title
   - Journal name
   - Publication year
   - Authors

### 3. Identify Problematic DOIs

Flag DOIs that are:
- **Not found** in Crossref (404 response)
- **Annotation DOIs**: contain "annotation" in the DOI
- **Masthead DOIs**: contain "masthead" in the DOI
- **Preprints vs published**: Check if preprint DOI when published version exists

### 4. Correct Invalid DOIs (Optional)

For invalid or suspicious DOIs, attempt correction:

1. **Extract citation context** (title, authors, journal, year)
2. **Search Crossref** by title and first author
3. **Match with confidence scoring**:
   - Score > 90: High confidence (safe to correct)
   - Score 70-90: Medium confidence (flag for review)
   - Score < 70: Low confidence (keep original)

4. **Apply corrections** only for high-confidence matches

### 5. Generate Reports

Create a comprehensive validation report with:

**Summary Statistics:**
- Total references processed
- Valid DOIs (count and percentage)
- Invalid DOIs (count and percentage)
- Problematic DOIs requiring manual review

**Detailed Results:**
For each reference, include:
- Line number or reference ID
- Original DOI
- Validation status (valid/invalid/excluded)
- Corrected DOI (if applicable)
- Confidence score
- Title and journal (if found)

**Recommendations:**
- References needing immediate correction
- References requiring manual verification
- Suspicious patterns (e.g., multiple invalid DOIs from same journal)

## Output Format

### Corrected Reference File

Generate a new file with corrected DOIs while preserving the original format:

```markdown
# References

1. **Smith, J. et al. (2023).** Correct paper title. *Journal Name*, 12(3): 123-145. DOI: 10.1234/correct-doi

2. **Jones, A. et al. (2022).** Another paper. *Different Journal*, 45(2): 67-89. DOI: 10.5678/also-correct
```

### Validation Report

Create a detailed report (`validation_report.txt`) with:

```
====================================================================================================
DOI VALIDATION REPORT
====================================================================================================

SUMMARY:
Total references: 28
Valid DOIs: 24 (85.7%)
Invalid DOIs: 4 (14.3%)

====================================================================================================
INVALID REFERENCES REQUIRING ATTENTION:
====================================================================================================

Reference #4:
  Citation: Skarin, H. & Segerman, B. (2011). Horizontal gene transfer...
  DOI: 10.4161/mge.1.3.17714
  Status: NOT FOUND
  Action: Verify manually or remove from reference list

Reference #7:
  Citation: Smith, T. J. et al. (2021). The Distinctive Evolution...
  DOI: 10.3389/fmicb.2021.630537
  Status: ANNOTATION DOI
  Action: Replace with main paper DOI if available

====================================================================================================
CORRECTIONS APPLIED:
====================================================================================================

Reference #2:
  Original DOI: 10.1016/j.bbrc.2007.07.010
  Corrected DOI: 10.1016/j.bbrc.2007.06.166
  Confidence: High (score: 102.4)
  Action: Corrected automatically

[... more corrections ...]
```

## Best Practices

### Validation Strategy

1. **Start with validation** before attempting corrections
2. **Use conservative thresholds** for automatic corrections (confidence > 80)
3. **Flag suspicious patterns** like:
   - Multiple DOIs from same journal failing
   - DOIs with unusual formats
   - References without DOIs in otherwise complete list

### Correction Guidelines

- **Only apply high-confidence corrections** (score > 90)
- **Preserve original formatting** of the reference file
- **Always create a backup** before making corrections
- **Generate detailed reports** for manual review

### Quality Assurance

- **Double-check corrections** against the actual paper
- **Verify journal names** and publication years
- **Check for duplicate entries** with different DOIs
- **Ensure consistency** in DOI formatting

## Common Issues

### Issue: DOI Not Found in Crossref

**Possible causes:**
- Typo in DOI (wrong digit, missing character)
- DOI from predatory journal
- Reference to non-existent paper
- DOI format error (missing prefix/suffix)

**Action:**
1. Verify the DOI character by character
2. Search for the paper title in Crossref/PubMed
3. Check if the journal is legitimate
4. Consider removing the reference if verification fails

### Issue: Annotation DOI Found

**Example:** `10.1371/annotation/b482f80f-c5b6-4b9c-8e9b-8b7139dc37f1`

**Action:**
- These are usually corrections/addendums, not the main paper
- Search for the main paper DOI instead
- Verify which DOI is appropriate for citation

### Issue: Multiple DOI Formats

**Examples:**
- `10.1016/j.bbrc.2007.07.010` vs `10.1016/j.bbrc.2007.06.166`
- Same paper, different version (e.g., corrected article)

**Action:**
- Use the most recent/corrected version
- Verify which version matches the cited content
- Check journal's versioning policy

## Advanced Features

### Batch Processing

For large reference files (>100 references):
1. Process in batches of 50 to avoid rate limiting
2. Add delays between API calls (1-2 seconds)
3. Save intermediate results for recovery
4. Generate summary statistics after each batch

### Confidence Scoring

Use Crossref's relevance score to assess correction confidence:
- **Score > 100**: Exact match (very high confidence)
- **Score 80-100**: Strong match (high confidence)
- **Score 60-80**: Probable match (medium confidence)
- **Score < 60**: Weak match (low confidence - do not auto-correct)

### Exclusion Patterns

Automatically exclude certain DOI types from corrections:
- Annotation DOIs (contain "annotation")
- Masthead DOIs (contain "masthead")
- Component DOIs (contain "component")
- Dataset DOIs (unless citing datasets)

## Troubleshooting

### API Rate Limiting

If you get rate limited:
- Add delays between requests (1-2 seconds)
- Process in smaller batches
- Use exponential backoff for retries

### Network Errors

For connection issues:
- Increase timeout values (10-30 seconds)
- Implement retry logic with backoff
- Check internet connectivity
- Use proxy if needed for institutional access

### File Format Issues

If file parsing fails:
- Check file encoding (UTF-8 vs Latin-1)
- Verify DOI pattern matching
- Manually inspect problematic lines
- Consider pre-processing the file

## Integration with Citation Styles

This skill works with various citation styles:
- **Numbered**: `[1]`, `1.`, etc.
- **Author-date**: `(Smith, 2023)`
- **Markdown**: `**Smith et al. (2023)**`
- **BibTeX**: `@article{...}`

The key is extracting DOIs regardless of surrounding format.

## Example Use Cases

### Use Case 1: Pre-Submission Validation

**User:** "I'm submitting a paper to Nature and need to verify all my references are correct"

**Action:**
1. Validate all DOIs in the reference list
2. Flag any invalid or suspicious DOIs
3. Attempt corrections for high-confidence matches
4. Generate detailed report for final review

### Use Case 2: Literature Review Quality Check

**User:** "I've compiled 200 references for my systematic review, want to make sure they're all real papers"

**Action:**
1. Batch process all references
2. Identify any fake or predatory journal papers
3. Check for duplicate entries
4. Generate quality report with statistics

### Use Case 3: DOI Correction

**User:** "My supervisor said some of my DOIs are wrong, can you fix them?"

**Action:**
1. Extract all DOIs from the reference file
2. Validate each DOI via Crossref
3. Find correct DOIs for invalid entries
4. Apply corrections with confidence scoring
5. Generate before/after comparison

## Important Notes

- **Always preserve the original file** - create corrected copies
- **Use conservative correction thresholds** to avoid false positives
- **Manual verification is recommended** for high-stakes submissions
- **Keep detailed logs** of all corrections made
- **Consider the context** - some fields have different DOI practices

## Limitations

- Cannot verify references without DOIs (need additional verification methods)
- Dependent on Crossref API availability and accuracy
- May not detect all predatory journals
- Cannot verify paywalled content without access
- May have false positives for very recent publications

## When to Escalate

Consider manual verification for:
- References to non-English journals
- Very recent publications (not yet in Crossref)
- References from obscure or predatory journals
- Government reports or technical documents
- Books and book chapters (may use different DOI systems)
- Conference proceedings with complex numbering