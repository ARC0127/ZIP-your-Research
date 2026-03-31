# Rewrite (portable): spreadsheets/examples/create_basic_spreadsheet.py

**Source (platform runtime):** `/home/oai/skills/spreadsheets/examples/create_basic_spreadsheet.py`
**Snapshot:** sha256 `f9f4af1b0a0e753687e1ae101436821f0d6a4f03694ce3075fe59818601a7dab` · 3388 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
Demonstration script showing `create_basic_spreadsheet.py` behavior in the platform spreadsheet artifact library.

## What the platform script does
- Creates a workbook with two sheets and writes values using both cell-level and range-level helpers.
- Adds a SUM formula and triggers recalculation to materialize the computed value.
- Demonstrates editing cells/ranges, adding a boolean column, and exporting/rendering.

## Portable template (ZYR)
Use openpyxl to create workbook structure and formulas. Note: formula results are not evaluated by openpyxl itself.

```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
```

```python
wb = Workbook()
ws_over = wb.active; ws_over.title = 'Overview'
ws_emp = wb.create_sheet('Employees')
ws_over['A1'] = 'Description'
ws_over['A2'] = 'Awesome Company Report'
ws_emp['A1'] = 'Title'; ws_emp['B1'] = 'Name'; ws_emp['C1'] = 'Address'; ws_emp['D1'] = 'Score'
rows = [
    ['Engineer','Vicky','90 50th Street',98],
    ['Manager','Alex','500 Market Street',92],
    ['Designer','Jordan','200 Pine Street',88],
]
for r, row in enumerate(rows, start=2):
    for c, v in enumerate(row, start=1):
        ws_emp.cell(row=r, column=c, value=v)
ws_emp['A6'] = 'Total Score'
ws_emp['D6'] = '=SUM(D2:D4)'
wb.save('basic.xlsx')
```

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| Workbook creation and data writes | PASS | openpyxl covers this directly. |
| Programmatic formula recalculation | PARTIAL | openpyxl does not evaluate; rely on Excel/LibreOffice for final values. |
| Render-to-image QA | PARTIAL | Use viewer-based QA or PDF export if needed. |

## QA checklist

- [ ] Open the workbook in Excel/LibreOffice and verify formula outputs.
- [ ] Confirm all expected sheets, headers, and ranges are present.
- [ ] Spot-check formatting (row heights, column widths) if used.
