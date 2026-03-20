---
name: dedao-dl
description: Handles interactions with the dedao-dl CLI tool for downloading and managing content from the Dedao (得到) App. Use when the user wants to list bought courses, ebooks, audiobooks, or download them in various formats (PDF, MP3, Markdown, EPUB).
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: ANGJustinl/dedao-dl-skill
# corpus-url: https://github.com/ANGJustinl/dedao-dl-skill/blob/f54131410e817463eae9e7866c228e9706e3c37a/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# dedao-dl

This skill guides the agent in using the `dedao-dl` CLI tool to interact with the Dedao (得到) app content.

## Initialization

**MANDATORY FIRST STEP:** Before using any `dedao-dl` commands for the first time, you MUST run the installation script and verify the CLI is available.

Run the script to download the latest binary for the current OS:
```bash
python scripts/install_dedao_dl.py
```
After installation, you should ALWAYS use the helper script `scripts/run_dedao.py` to execute commands instead of running the raw `dedao-dl` executable. The helper script cleans up the CLI's terminal formatting, making the output directly readable by you without needing to redirect it to text files.
Example: Use `python scripts/run_dedao.py -h` instead of `./dedao-dl -h`.

## Prerequisites & Login

Before downloading any content, ensure the user is logged in:
- Command: `python scripts/run_dedao.py login -q` (QR code login) or `python scripts/run_dedao.py login -c "<cookie_string>"`
- Verify current user: `python scripts/run_dedao.py who`
- List logged-in users: `python scripts/run_dedao.py users`
- Switch user: `python scripts/run_dedao.py su`

Dependencies for specific formats (inform the user if they are missing):
- PDF generation requires `wkhtmltopdf`
- Audio generation requires `ffmpeg`
- Markdown requires no additional dependencies

## General Workflow

For any content download, the typical two-step workflow is:
1. List the specific type of content to find its `ID`.
2. Use the corresponding download command with the `ID` and format flag (`-t`).

## Key Workflows & Commands

### 1. Courses (专栏/课程) & Free Content (免费专区)
- **List purchased courses**: `python scripts/run_dedao.py course`
- **List free courses**: `python scripts/run_dedao.py free` (Returns `EnID` strings instead of integer `ID`s)
- **List articles in a course**: 
  - For purchased courses (using integer ID): `python scripts/run_dedao.py course -i <course_ID>`
  - For free courses (using EnID): `python scripts/run_dedao.py article -c <course_EnID>`
- **Download a single article (RECOMMENDED)**: `python scripts/run_dedao.py dl <course_ID_or_EnID> <article_ID> -t <format>`
- **Download a full course**: `python scripts/run_dedao.py dl <course_ID_or_EnID> -t <format> [options]`
  - **WARNING: NEVER download a full course (only 1 parameter) without explicit user permission. Full downloads can take hours, consume massive disk space, and trigger anti-bot bans.**
  - Formats (`-t`): `1` (MP3), `2` (PDF), `3` (Markdown, **DEFAULT FOR THE AGENT**)
  - Options for Markdown (`-t 3`): `-m` (merge into one file), `-c` (include hot comments)
  - Prefix ordering: `-o` (adds index prefix like `00x.`)
  *Note: When downloading as PDF, be aware of rate limits ("496 NoCertificate"). Add sleep intervals if scripting.*

### 2. E-Books (电子书)
- **List e-books**: `python scripts/run_dedao.py ebook`
- **Download an e-book**: `python scripts/run_dedao.py dle <ebook_ID> -t <format>`
  - Formats (`-t`): `1` (HTML, default), `2` (PDF), `3` (EPUB), `4` (Markdown Notes)
- **View e-book notes**: `python scripts/run_dedao.py ebook notes -i <ebook_ID>`
- **Export e-book notes**: `python scripts/run_dedao.py dle <ebook_ID> -t 4` (Downloads notes as Markdown)

### 3. Audiobooks (每天听本书)
- **List audiobooks**: `python scripts/run_dedao.py odob`
- **Download audiobook audio/text**: `python scripts/run_dedao.py dlo <audiobook_ID> -t <format>`
  - Formats (`-t`): `1` (MP3), `2` (PDF), `3` (Markdown, **DEFAULT FOR THE AGENT**)

### 4. Other Content
- **List all categories & stats**: `python scripts/run_dedao.py cat`
- **List 'JinNang' (锦囊)**: `python scripts/run_dedao.py ace`
- **List recommended topics (知识城邦)**: `python scripts/run_dedao.py topic`

## Execution Guidelines

- Always check `python scripts/run_dedao.py -h` or `python scripts/run_dedao.py <command> -h` if unsure of the exact arguments.
- Always retrieve the correct `ID` first before executing a download command. **Make sure you use the list command corresponding to the content type you want to download (e.g., `course` ID for `dl`, `ebook` ID for `dle`, `odob` ID for `dlo`). Do not mix up IDs across categories.**
- **NEVER download an entire course (e.g. `python scripts/run_dedao.py dl <course_ID_or_EnID>`) unless the user explicitly asks you to.** Many courses have hundreds of articles which can lead to account bans.
- **ALWAYS favor downloading a single article**: First list the course articles using `course -i <course_ID>` or `article -c <course_EnID>`, find the specific article ID, and use `python scripts/run_dedao.py dl <course_ID_or_EnID> <article_ID>`.
- **DEFAULT FORMAT**: Whenever you download content using `dl` or `dlo`, default to using `-t 3` (Markdown) unless the user explicitly asks for MP3 or PDF. Markdown is safer, faster, and easier to read.
- When generating markdown for a whole course (if permitted by the user), consider using `-m` to consolidate files unless the user explicitly asks for individual files.