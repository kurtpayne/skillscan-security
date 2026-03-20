---
name: gt-people-tags-by-sector
description: extract and verify gilbert + tobin people tagged to a specific sector from user-uploaded pdf exports (e.g., our people search results filtered by sector). use when the user uploads a pdf listing people for a sector and needs an ordered table of names and titles (partner, lawyer, etc.) and optional verification against the published profiles csv.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: gryan-gtlaw/gt-people-tags-by-sector
# corpus-url: https://github.com/gryan-gtlaw/gt-people-tags-by-sector/blob/01104a1e9adecd221c40511290c631616c0ad4f7/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# GT website people tags by sector (PDF-first)

## Purpose
Produce a reliable, reviewable list of **all people tagged to a sector** based on a user-supplied PDF export of GT website people search results.

This workflow is designed for situations where the live “Our people” directory page cannot be reliably scraped, and the user instead provides a PDF export.

## Required inputs
- One or more **uploaded PDFs** (each PDF usually represents one sector filter result).
- The canonical verification CSV: `Published profiles-Fri13March2026.csv` (bundled with this skill).

## Accepted inputs
- A single PDF for one sector.
- Multiple PDFs for multiple sectors.
- Optional: a sector name and/or the source directory URL used to generate the PDF.

## PDF-first extraction rules
For each supplied PDF:

1. Treat the PDF as the primary source.
2. Identify the **sector** represented by the PDF:
   - Prefer an explicit sector label in the PDF if present.
   - Otherwise, infer it from the filename (e.g., `Agribusiness.pdf`) and mark as inferred.
3. Extract the ordered list of people exactly as shown in the PDF results.
4. For each person, extract:
   - Full name
   - Title (e.g., Partner, Special Counsel, Lawyer, Consultant)
   - Location (if present)
5. Preserve ordering exactly as displayed.
6. Do not infer or add people not shown in the results.
7. If the PDF appears to include pagination, ensure the extracted list includes all pages.

## Multi-sector workflow
When multiple PDFs are provided:
1. Process all PDFs.
2. Combine all extracted rows into **one consolidated inline review table**.
3. Group rows by sector and preserve the sector order supplied by the user.
4. Within each sector, preserve the exact ordering from the PDF.

## Verification rules (Published Profiles CSV)
Verify each extracted person name against `Published profiles-Fri13March2026.csv`.

1. Build the canonical comparison name from CSV columns:
   - `First name` + `Last name`
2. Match using **exact full-name comparison** first.
3. If not found:
   - Do not silently normalise or auto-correct.
   - Mark as `Unverified` and add a brief note (e.g., spelling differs, suffix, hyphenation).

## Inline review output
After processing all PDFs, provide one combined inline table with these columns:

- Sector
- Person Order
- Extracted Name
- Title
- Location
- Verified Name (CSV)
- Verified in Published Profiles CSV
- Verification Notes
- Source (PDF filename)
- Source URL (only if user supplied)

### Notes guidance
Use concise notes such as:
- Exact match in CSV
- Unverified – no exact CSV match
- Sector inferred from filename
- Needs manual review (layout ambiguity)

## Final Excel output rule
Do not create an Excel workbook unless the user explicitly requests it.

When the user explicitly requests the spreadsheet:
1. Create **one workbook** containing all processed sectors.
2. Create a **separate worksheet tab for each sector**.
3. Each worksheet must include only these columns:
   - Sector
   - Person Order
   - Name (use verified canonical name where available)
   - Title
   - Location
   - Source (PDF filename)
   - Source URL (only if available)
4. If a sheet name exceeds Excel’s 31 character limit, shorten it and report the change.

## Quality controls
Before presenting results:
1. Check for duplicated names caused by extraction error.
2. Check that ordering is sequential and complete within each sector.
3. Confirm the sector label is correct (or explicitly marked as inferred).
4. Be explicit about uncertainty.

## Consolidation behaviour
Maintain a running consolidated dataset across the conversation for all sectors processed for this task.
If the user adds more sector PDFs later in the same task, append them unless the user asks to start again.