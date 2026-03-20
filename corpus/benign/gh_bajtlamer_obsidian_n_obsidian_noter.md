---
name: obsidian-noter
description: Copy documents or folders into the Obsidian vault. Operates only on Markdown and plain text files. Text files (.txt, .text) are renamed and reformatted to .md. Non-text files are skipped. Folder structure is preserved.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Glob, Grep
argument-hint: [source-path]
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Bajtlamer/obsidian-noter
# corpus-url: https://github.com/Bajtlamer/obsidian-noter/blob/c61684a644c9ebab148f2f116e45aa2528e7aab0/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Obsidian Noter

Copy Markdown and plain text files into the Obsidian vault at `~/Obsidian-vault-01`, preserving folder structure. Source files are never deleted or modified.

## Settings

- **Vault path:** `~/Obsidian-vault-01`
- **Target folder:** `90-Migrated`

All migrated files are placed under the target folder inside the vault. For example, with the defaults above the destination root is `~/Obsidian-vault-01/90-Migrated/`. To change the subfolder, edit the value next to "Target folder" above.

## Rules

1. **Only operate on Markdown and plain text files.** Accepted extensions: `.md`, `.markdown`, `.txt`, `.text`
2. **Skip all other file types** (images, PDFs, Office documents, HTML, etc.). Report skipped files to the user.
3. **Rename and reformat text files to Markdown.** Any `.txt` or `.text` file must be renamed to `.md`. Review the content and ensure it uses valid Markdown formatting (headings, lists, paragraphs). Do not invent content, only adjust formatting where needed.
4. **Preserve the source directory as a folder in the vault.** When copying a directory, use its basename (last path component) as the top-level folder in the vault, then recreate the internal hierarchy under it. For example, `/obsidian-noter ~/projects/notes` creates `<vault>/notes/...`.
5. **Do not overwrite existing files.** If a file with the same name already exists in the vault, ask the user how to proceed (skip, rename, or overwrite).
6. **Report results.** After processing, print a summary: files copied, files renamed (.txt to .md), files skipped.

## Workflow

Given `$ARGUMENTS` as the source path:

### Step 1: Validate source

- Verify the source path exists.
- Determine if it is a file or a directory.

### Step 2: Discover files

- If the source is a single file, process that file.
- If the source is a directory, recursively find all files within it.
- Classify each file as accepted (`.md`, `.markdown`, `.txt`, `.text`) or skipped (everything else).

### Step 3: Process each accepted file

For each accepted file:

1. Read the file content.
2. If the extension is `.txt`, `.text`, or `.markdown`:
   - Change the target extension to `.md`.
   - Review the content for basic Markdown formatting. Fix obvious issues (e.g., add blank lines before headings, ensure list markers are consistent). Do not alter the meaning or add new content.
3. Determine the target path inside the vault. The base destination is `<vault>/<target-folder>` (by default `~/Obsidian-vault-01/90-Migrated`). Read the current "Target folder" value from the Settings section above. When the source is a directory, use its basename (the last path component) as a subfolder under the target folder. For example, if the source is `~/test/folder`, the target root is `~/Obsidian-vault-01/90-Migrated/folder/`. Preserve the internal folder structure relative to the source directory under that target root. When the source is a single file, place it directly in the target folder.
4. Check if the target path already exists. If so, ask the user before proceeding.
5. Create any necessary parent directories in the vault.
6. Write the file to the target location.

### Step 4: Summary

Print a summary table:

```
Copied:   X files
Renamed:  Y files (.txt/.text/.markdown -> .md)
Skipped:  Z files (list filenames)
```