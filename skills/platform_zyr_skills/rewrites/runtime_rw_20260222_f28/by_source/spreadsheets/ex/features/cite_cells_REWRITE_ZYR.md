# Rewrite (portable): spreadsheets/examples/features/cite_cells.py

**Source (platform runtime):** `zyr_runtime_skills/spreadsheets/examples/features/cite_cells.py`
**Snapshot:** sha256 `3c36e6d30e7214f4ee24778847982e4bdbbfa783db53e59f2ef573c41f485ac0` · 1181 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
Demonstration script showing `cite_cells.py` behavior in the platform spreadsheet artifact library.

## What the platform script does
- Attaches 'citation' metadata to a range and a cell via a platform-specific `cite(...)` API (tether id + line range).

## Portable template (ZYR)
Spreadsheet apps do not have a native, interoperable 'citation tether' primitive. Use one of:
- A dedicated 'Source' column with plain-text URLs or identifiers.
- Cell comments/notes (`openpyxl.comments.Comment`) for lightweight provenance.

```python
from openpyxl.comments import Comment
ws['A4'].comment = Comment('Source: doc XYZ, lines 23-46', 'zyr')
```

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| Provenance support | PARTIAL | Portable via columns/comments, not via platform tethers. |
| Exact cite/tether semantics | GAP | Platform-only feature. |

## QA checklist

- [ ] Ensure sources are human-readable in the workbook (URLs or bibliographic strings).
- [ ] Avoid relying on platform-specific tether ids outside the platform runtime.
