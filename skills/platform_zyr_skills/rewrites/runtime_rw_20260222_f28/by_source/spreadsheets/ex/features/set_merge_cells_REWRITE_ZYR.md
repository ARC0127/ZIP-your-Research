# Rewrite (portable): spreadsheets/examples/features/set_merge_cells.py

**Source (platform runtime):** `zyr_runtime_skills/spreadsheets/examples/features/set_merge_cells.py`
**Snapshot:** sha256 `ff4be68b2b2048bc29612b29ab10e1e6ddec6bc1aecf6f02805620fb229d3565` · 1356 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
Demonstration script showing `set_merge_cells.py` behavior in the platform spreadsheet artifact library.

## What the platform script does
- Demonstrates merging and unmerging cell ranges.

## Portable template (ZYR)
Use `ws.merge_cells()` / `ws.unmerge_cells()`:

```python
ws.merge_cells('C7:D7')
# ws.unmerge_cells('C7:D7')
```

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| Merging | PASS | Portable via openpyxl. |

## QA checklist

- [ ] Check merged cell alignment and borders visually.
