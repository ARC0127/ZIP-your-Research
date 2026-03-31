# 02 — Portable template library

This library defines portable baselines for common tasks. Use these in user-facing deliverables.

## T-DOCX-1: DOCX edit + visual QA loop

- Edit with `python-docx`
- Verify with LibreOffice headless conversion + PNG rendering

```bash
OUTDIR=/tmp/docx_render
mkdir -p "$OUTDIR"
soffice -env:UserInstallation=file:///tmp/lo_profile_$$ --headless --convert-to pdf --outdir "$OUTDIR" input.docx
pdftoppm -png "$OUTDIR/input.pdf" "$OUTDIR/input"
```

## T-PDF-1: PDF generate + visual QA loop

- Generate with `reportlab`
- Verify with `pdftoppm`

```bash
pdftoppm -png input.pdf /tmp/input_page
```

## T-XLSX-1: Spreadsheet creation/editing (portable baseline)

- Implement with `openpyxl` (values, formulas, styles, tables, charts)
- Verify by opening in Excel/LibreOffice (formula calculation + visual layout)

```python
from openpyxl import Workbook
wb = Workbook()
ws = wb.active
ws.title = "Sheet1"
ws["A1"] = "Hello"
ws["B1"] = 3
ws["C1"] = "=B1*2"
wb.save("out.xlsx")
```

### Notes

- `openpyxl` does **not** evaluate formulas. Always verify computed values in a real spreadsheet app for final delivery.
- Avoid dynamic-array-only formulas unless your target environment is guaranteed.

## T-XLSX-2: Conditional formatting (portable)

Use `openpyxl.formatting.rule` and validate in a viewer.

## T-XLSX-3: Charts/Tables (portable)

Use `openpyxl.chart.*` and `openpyxl.worksheet.table.*`.
