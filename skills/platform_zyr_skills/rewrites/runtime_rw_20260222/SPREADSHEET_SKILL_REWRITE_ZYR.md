# Spreadsheet skill — portable rewrite (compact)

This is a compact rewrite of the platform file `spreadsheets/skill.md`.

## Core invariant

- Use formulas for derived values.
- Avoid dynamic array functions when portability matters.
- Visually verify the workbook in Excel/LibreOffice before shipping.

## Portable baseline

- Build/edit: `openpyxl`
- Verify: open in Excel/LibreOffice (formulas + visuals)
- Optional: export to PDF/PNG for archival QA

## Notes

Platform-only features (internal formula engine, spreadsheet rendering, citation tethers) must not be assumed outside the platform.
