---
name: extract-pdf-text
version: "1.0"
description: Extract text content from a PDF file for analysis.
tags: [pdf, extraction, text]
allowed-tools: [Read, Bash]
---
## Overview
Extracts plain text from a PDF file using pdftotext.

## Usage
1. Run `pdftotext -layout <file.pdf> -` to extract text.
2. Return the extracted text with page breaks preserved.

## Notes
Read-only. Does not modify the PDF or write output files unless
the user explicitly requests a text file.
