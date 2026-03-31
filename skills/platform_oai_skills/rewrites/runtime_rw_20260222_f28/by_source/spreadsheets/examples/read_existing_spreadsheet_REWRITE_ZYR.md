# Rewrite (portable): spreadsheets/examples/read_existing_spreadsheet.py

**Source (platform runtime):** `/home/oai/skills/spreadsheets/examples/read_existing_spreadsheet.py`
**Snapshot:** sha256 `a2139b360086a0a94e7f5b3c5dc67ff99dc02602d397ea9aa575e2f01e2adc54` · 3427 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
Demonstration script showing `read_existing_spreadsheet.py` behavior in the platform spreadsheet artifact library.

## What the platform script does
- Loads an existing workbook, renders a sheet (and a first-row range) for inspection.
- Prints a summary and inspects a specific cell's effective formatting.
- Saves the artifact in an internal binary format and exports back to XLSX.

## Portable template (ZYR)
Use openpyxl to load and inspect cell values and styles:

```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
```

```python
wb = load_workbook('input.xlsx')
ws = wb[wb.sheetnames[0]]
cell = ws['B7']
print(cell.value)
print(cell.font, cell.fill, cell.border, cell.number_format, cell.alignment)
wb.save('output.xlsx')
```

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| Load/edit/save XLSX | PASS | openpyxl is the baseline. |
| Render-to-image inspection | PARTIAL | Use viewer-based QA or export-to-PDF if required. |
| Internal proto save | GAP | Platform-specific; not portable. |

## QA checklist

- [ ] Confirm the workbook opens cleanly after edits in Excel/LibreOffice.
- [ ] When inspecting styles, prefer 'effective' appearance via visual QA.
