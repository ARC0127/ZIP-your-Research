# Rewrite (portable): spreadsheets/examples/features/create_tables.py

**Source (platform runtime):** `/home/oai/skills/spreadsheets/examples/features/create_tables.py`
**Snapshot:** sha256 `07a8e02a990c9b0e42395f155840ecbf9b82f27d010037f8105fa9a5f9505916` · 1517 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
Demonstration script showing `create_tables.py` behavior in the platform spreadsheet artifact library.

## What the platform script does
- Seeds tabular data and creates an Excel-style table with a predefined style.
- Adjusts column widths and row heights, then renders for inspection.

## Portable template (ZYR)
Use openpyxl Table + TableStyleInfo:

```python
from openpyxl.worksheet.table import Table, TableStyleInfo

# Assume data range is A1:C5
tab = Table(displayName="ScoresTable", ref="A1:C5")
style = TableStyleInfo(
    name="TableStyleMedium2",
    showFirstColumn=False,
    showLastColumn=False,
    showRowStripes=True,
    showColumnStripes=False,
)
tab.tableStyleInfo = style
ws.add_table(tab)
```

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| Table creation and styling | PASS | Portable via openpyxl. |
| Row/column sizing | PASS | Portable (width/height settings). |

## QA checklist

- [ ] Verify table style and stripes render correctly in Excel/LibreOffice.
- [ ] Confirm the table ref range matches the data bounds.
