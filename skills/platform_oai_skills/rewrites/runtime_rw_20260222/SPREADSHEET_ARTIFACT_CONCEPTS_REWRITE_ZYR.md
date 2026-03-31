# Spreadsheet artifact concepts — portable rewrite (compact)

This is a compact rewrite of `spreadsheets/spreadsheet.md`.

Map concepts to openpyxl:
- workbook → `Workbook` / `load_workbook`
- sheet → worksheet object
- cell/range → `ws['A1']` / iterate over ranges
- charts/tables → openpyxl chart/table modules
