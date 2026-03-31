# 03 — QA loops (non-negotiable invariants)

The platform skills emphasize a strict "render → inspect → fix → repeat" loop. The same invariant is portable.

## DOCX QA loop

1) Convert DOCX → PDF (LibreOffice headless with unique user profile)
2) Convert PDF → PNG pages
3) Inspect every page at 100% zoom
4) Fix and repeat until zero visible defects

## PDF QA loop

1) Render PDF → PNG pages
2) Inspect every page
3) Fix and repeat until zero visible defects

## Spreadsheet QA loop

1) Build/edit workbook (`openpyxl`)
2) Open in Excel/LibreOffice and:
   - confirm formulas compute as intended,
   - confirm charts/tables/conditional formatting look correct,
   - confirm formatting matches expectations
3) If needed, export PDF/PNG for archival QA

## Citation hygiene invariant

In final deliverables, citations must be human-readable and never contain tool-internal tokens.
