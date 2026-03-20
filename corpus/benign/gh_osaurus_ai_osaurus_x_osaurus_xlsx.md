---
name: osaurus-xlsx
description: Read, create, and modify Excel (.xlsx) spreadsheets using the Osaurus XLSX plugin. Use when working with .xlsx files, converting between CSV and Excel, or performing batch spreadsheet operations.
metadata:
  author: tpae
  version: "0.1.0"
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: osaurus-ai/osaurus-xlsx
# corpus-url: https://github.com/osaurus-ai/osaurus-xlsx/blob/cf0233eadcf5193d492a4188b7ea1720cdf11945/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Osaurus XLSX

This plugin reads, creates, and modifies Excel (.xlsx) files. It uses a stateful in-memory model — you load or create a workbook, manipulate it, then save it to disk.

## Workflow

Always follow this sequence:

1. **read_xlsx(path)** or **create_xlsx(sheets)** — get a `workbook_id`
2. **write_cells / modify_xlsx** — mutate the workbook in memory (optional, repeat as needed)
3. **save_xlsx(workbook_id, path)** — write the final .xlsx file to disk

For one-shot read operations, `list_sheets` and `xlsx_to_csv` read directly from disk without needing the full workflow.

## Quick Reference

### Reading

| Tool | When to use |
|------|-------------|
| `read_xlsx` | Read all cell data from a file. Returns `workbook_id` + structured JSON. |
| `get_cell_value` | Look up a specific cell or range from an already-loaded workbook. |
| `list_sheets` | Quickly list sheet names without reading all data. |

### Writing

| Tool | When to use |
|------|-------------|
| `create_xlsx` | Start a new workbook from scratch with headers and data rows. |
| `write_cells` | Set individual cell values in a loaded workbook. |
| `save_xlsx` | Write the workbook to a .xlsx file. **Nothing is saved until you call this.** |

### Transformation

| Tool | When to use |
|------|-------------|
| `xlsx_to_csv` | Export a sheet as CSV or TSV text. Reads directly from disk. |
| `csv_to_xlsx` | Parse CSV/TSV text into a new workbook. Call `save_xlsx` after. |
| `modify_xlsx` | Batch operations — set cells, formulas, delete rows/columns, add/rename sheets. |

## Cell References

All cell references use standard Excel notation:

- Single cell: `A1`, `B5`, `Z100`
- Range: `A1:D10`, `B2:B50`
- Column letters: A=1, Z=26, AA=27, AZ=52, etc.

## Value Types

When writing cell values, types are auto-detected from the string value:

| Input | Detected type | Example |
|-------|---------------|---------|
| Starts with `=` | Formula | `=SUM(A1:A10)` |
| Valid number | Number | `42`, `3.14`, `-100` |
| `true` / `false` | Boolean | `true` |
| Everything else | String | `Hello World` |

You can override auto-detection with the `type` parameter in `write_cells`:
- `"string"` — force string
- `"number"` — force number
- `"boolean"` — force boolean
- `"formula"` — force formula (adds `=` prefix if missing)

## Tool Tips

### read_xlsx
- Returns all sheets by default. Use `sheet_name` to read a single sheet.
- Use `range` (e.g. `"A1:D10"`) to limit the data returned — useful for large files.
- The returned `workbook_id` is needed for `write_cells`, `modify_xlsx`, `get_cell_value`, and `save_xlsx`.
- Sheet name matching is case-insensitive.

### get_cell_value
- Requires a `workbook_id` from a prior `read_xlsx` or `create_xlsx` call.
- You must provide **either** `cell` (e.g. `"B5"`) **or** `range` (e.g. `"A1:C3"`) — omitting both returns an error.
- Sheet name matching is case-insensitive.

### list_sheets
- Reads sheet names directly from disk — no `workbook_id` needed.
- Useful for discovering sheet names before calling `read_xlsx` with a specific `sheet_name`.

### create_xlsx
- Pass an array of sheet definitions, each with a `name`, optional `headers`, and optional `rows`.
- `headers` are always stored as strings.
- `rows` values are auto-detected (numbers, booleans, strings).
- Remember to call `save_xlsx` afterwards — nothing is written to disk until you save.

### write_cells
- If the specified `sheet_name` doesn't exist, a new sheet is created automatically.
- Each cell in the `cells` array needs a `ref` (e.g. `"B5"`) and a `value`.
- Use `type` to force a specific value type if auto-detection isn't what you want.

### save_xlsx
- The `.xlsx` extension is added automatically if missing.
- Always call this when you're done. The workbook only exists in memory until saved.

### xlsx_to_csv
- Reads directly from a file on disk — no need to `read_xlsx` first.
- Defaults to the first sheet. Use `sheet_name` to specify a different one.
- Set `format` to `"tsv"` for tab-separated output.

### csv_to_xlsx
- Accepts raw CSV/TSV text in the `csv_data` parameter.
- Set `has_header: true` to keep the first row as strings (prevents number detection on headers).
- Set `delimiter` to `"tab"` or `"\t"` for TSV input.
- Returns a `workbook_id` — call `save_xlsx` to write to disk.

### modify_xlsx
- Batch multiple operations in a single call for efficiency.
- If `sheet_name` is omitted, operations target the first sheet in the workbook.
- Available operations:
  - `set_cell` — set a cell value (`ref` + `value`)
  - `set_formula` — set a formula (`ref` + `formula`)
  - `delete_row` — delete a row by number and shift rows up (`row`)
  - `delete_column` — delete a column by letter and shift columns left (`column`)
  - `rename_sheet` — rename the target sheet (`new_name`)
  - `add_sheet` — add a new empty sheet (`name`)

## Limitations

1. **No cell formatting.** The plugin reads and writes cell values only. Fonts, colors, borders, and other formatting from existing files are not preserved.

2. **No images or charts.** Embedded objects in existing files are not read or preserved.

3. **Formulas are stored, not evaluated.** When you write `=SUM(A1:A10)`, the formula text is saved. Excel will evaluate it when the file is opened.

4. **Large files.** Reading very large spreadsheets (100k+ rows) loads all data into memory. Use the `range` parameter with `read_xlsx` to limit data.

5. **Round-trip fidelity.** Reading an existing .xlsx and saving it back will preserve cell values but may lose formatting, charts, images, and other advanced features.

## Example: Read and Summarize

```
1. read_xlsx(path="sales.xlsx")
   → workbook_id, sheets with cell data

2. Agent analyzes the data and responds with a summary
```

## Example: Create a New Spreadsheet

```
1. create_xlsx(sheets=[
     {name: "Employees", headers: ["Name", "Department", "Salary"],
      rows: [["Alice", "Engineering", "120000"],
             ["Bob", "Marketing", "95000"]]}
   ])
   → workbook_id

2. save_xlsx(workbook_id, path="employees.xlsx")
   → file written to disk
```

## Example: Read, Modify, and Save

```
1. read_xlsx(path="budget.xlsx")
   → workbook_id

2. write_cells(workbook_id, sheet_name="Q4",
     cells=[{ref: "B10", value: "=SUM(B1:B9)", type: "formula"}])
   → cell written

3. save_xlsx(workbook_id, path="budget_updated.xlsx")
   → file written to disk
```

## Example: CSV to Excel

```
1. csv_to_xlsx(csv_data="Name,Age\nAlice,30\nBob,25", has_header=true)
   → workbook_id

2. save_xlsx(workbook_id, path="people.xlsx")
   → file written to disk
```

## Example: Batch Modifications

```
1. read_xlsx(path="data.xlsx")
   → workbook_id

2. modify_xlsx(workbook_id, sheet_name="Sheet1", operations=[
     {type: "set_cell", ref: "A1", value: "Updated Title"},
     {type: "set_formula", ref: "D10", formula: "=AVERAGE(D1:D9)"},
     {type: "delete_row", row: 5},
     {type: "add_sheet", name: "Summary"},
     {type: "rename_sheet", new_name: "Data"}
   ])
   → 5 operations applied

3. save_xlsx(workbook_id, path="data_modified.xlsx")
   → file written to disk
```