# Rewrite (portable): spreadsheets/examples/features/set_cell_fills.py

**Source (platform runtime):** `zyr_runtime_skills/spreadsheets/examples/features/set_cell_fills.py`
**Snapshot:** sha256 `c53f0d45b0112c8e252f0857ee0c7fa108c0adaa3334f714b8616e9f35a50990` · 2823 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
Demonstration script showing `set_cell_fills.py` behavior in the platform spreadsheet artifact library.

## What the platform script does
- Demonstrates setting cell fills (solid colors, patterns) for specific cells/ranges.

## Portable template (ZYR)
Use openpyxl PatternFill:

```python
from openpyxl.styles import PatternFill
fill = PatternFill('solid', fgColor='FFF2CC')
ws['B2'].fill = fill
```

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| Fills | PASS | Portable via openpyxl. |

## QA checklist

- [ ] Verify colors/patterns in the target spreadsheet app.
