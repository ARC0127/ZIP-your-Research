# Rewrite (portable): spreadsheets/examples/create_spreadsheet_with_styling.py

**Source (platform runtime):** `/home/oai/skills/spreadsheets/examples/create_spreadsheet_with_styling.py`
**Snapshot:** sha256 `7f0428c3cf395ff95a727faa616709847c1d9495f2f59f830ef5c188f8e96c69` · 6386 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
Demonstration script showing `create_spreadsheet_with_styling.py` behavior in the platform spreadsheet artifact library.

## What the platform script does
- Builds a two-sheet scoreboard-style workbook.
- Defines reusable styles (fills, fonts, alignment) and applies them to header/highlight ranges.
- Adds formulas (SUM, INDEX/MATCH) and merges cells.
- Adds conditional formatting rules (not-blank checks).

## Portable template (ZYR)
Replicate with openpyxl styles, merges, and conditional formatting:

```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
```

```python
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles.differential import DifferentialStyle

# Example: header fill + bold font
header_fill = PatternFill('solid', fgColor='B7E1CD')
header_font = Font(bold=True)
for cell in ws['A2:G2'][0]:
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal='center', vertical='center')

# Merge C7:D7
ws.merge_cells('C7:D7')

# Conditional formatting example (non-blank)
dxf = DifferentialStyle(fill=PatternFill('solid', fgColor='B7E1CD'))
rule = FormulaRule(formula=['LEN(A2)>0'], dxf=dxf)
ws.conditional_formatting.add('A2:G2', rule)
```

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| Styling primitives | PASS | openpyxl supports fonts/fills/alignment/borders. |
| Conditional formatting | PASS | FormulaRule is portable; validate in target app. |
| Complex formulas (INDEX/MATCH) | PASS | Supported by Excel/LibreOffice; avoid XLOOKUP/FILTER for portability. |

## QA checklist

- [ ] Verify conditional formatting triggers correctly in Excel/LibreOffice.
- [ ] Check merged cells and alignment in a real viewer.
- [ ] Confirm formulas reference the intended ranges (no off-by-one).
