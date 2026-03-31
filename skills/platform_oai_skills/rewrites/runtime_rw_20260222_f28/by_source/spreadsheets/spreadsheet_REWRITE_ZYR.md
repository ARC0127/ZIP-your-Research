# Rewrite (portable): spreadsheets/spreadsheet.md

**Source (platform runtime):** `/home/oai/skills/spreadsheets/spreadsheet.md`
**Snapshot:** sha256 `e953dc28faf645ba2972c590d2cb7d7585e1112cf48c7d5b741292093ccd982f` · 18421 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
A conceptual guide to a spreadsheet artifact model: workbook → sheets → cells/ranges, plus formatting, charts, tables, and rendering.

## What the platform file provides (conceptual)
- A workbook abstraction with sheet management.
- Cell/range APIs for values and formulas.
- Formatting primitives (fills, fonts, borders, alignment).
- Rendering/export hooks and summary/introspection helpers.

## Portable template (ZYR)
Map the concepts to `openpyxl`:
- Workbook: `openpyxl.Workbook` / `load_workbook`
- Sheet: `wb[sheet_name]` / `wb.create_sheet()`
- Cell: `ws['A1']`, Range: iterate over `ws['A1:C3']` for bulk ops
- Charts: `openpyxl.chart.*`
- Tables: `openpyxl.worksheet.table.*`

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| Concept mapping to openpyxl | PASS | All core primitives have portable equivalents. |
| Rendering | PARTIAL | Portable rendering depends on external viewers (Excel/LibreOffice) or PDF export workflows. |

## QA checklist

- [ ] Treat 'render' as a QA step; do not assume programmatic style serialization equals visual correctness.
- [ ] Keep bulk edits range-based to reduce human error.
