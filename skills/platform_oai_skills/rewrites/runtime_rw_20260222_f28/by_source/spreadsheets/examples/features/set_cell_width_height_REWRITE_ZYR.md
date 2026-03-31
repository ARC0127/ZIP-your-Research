# Rewrite (portable): spreadsheets/examples/features/set_cell_width_height.py

**Source (platform runtime):** `/home/oai/skills/spreadsheets/examples/features/set_cell_width_height.py`
**Snapshot:** sha256 `c35b8d4af394589a7a738486af13bf1cb7f4fe26bc397bc41e8e57b3ea0f196a` · 1664 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
Demonstration script showing `set_cell_width_height.py` behavior in the platform spreadsheet artifact library.

## What the platform script does
- Demonstrates setting column widths and row heights for readability and layout control.

## Portable template (ZYR)
Use `ws.column_dimensions[col].width` and `ws.row_dimensions[row].height`:

```python
ws.column_dimensions['B'].width = 24
ws.row_dimensions[2].height = 28
```

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| Sizing | PASS | Portable via openpyxl. |

## QA checklist

- [ ] Spot-check that widths/heights look correct in Excel/LibreOffice.
