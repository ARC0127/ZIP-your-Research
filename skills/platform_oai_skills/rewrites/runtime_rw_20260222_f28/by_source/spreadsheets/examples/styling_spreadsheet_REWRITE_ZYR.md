# Rewrite (portable): spreadsheets/examples/styling_spreadsheet.py

**Source (platform runtime):** `/home/oai/skills/spreadsheets/examples/styling_spreadsheet.py`
**Snapshot:** sha256 `970760cf3d819e140d4f863798a717f53b7e36d5ebac85feb0b95229f11d1fcc` · 2435 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
Demonstration script showing `styling_spreadsheet.py` behavior in the platform spreadsheet artifact library.

## What the platform script does
- Creates a workbook, sets column widths, writes a header row, and applies conditional formatting for non-blank headers.
- Fills data rows, merges a bottom range, sets a SUM formula, and applies borders + centered alignment.

## Portable template (ZYR)
Combine openpyxl range writes + styles + merges + borders:

```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
```

```python
thin = Side(style='thin', color='000000')
border = Border(left=thin, right=thin, top=thin, bottom=thin)
ws.merge_cells('B9:E9')
ws['B9'] = '=SUM(E3:E6)'
ws['B9'].font = Font(bold=True)
ws['B9'].border = border
ws['B9'].alignment = Alignment(horizontal='center')
```

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| Conditional formatting and borders | PASS | Portable via openpyxl. |
| Render step | PARTIAL | Use external viewer for final QA. |

## QA checklist

- [ ] Verify merged formula cell displays as expected in the target app.
- [ ] Ensure conditional formatting ranges are correct.
