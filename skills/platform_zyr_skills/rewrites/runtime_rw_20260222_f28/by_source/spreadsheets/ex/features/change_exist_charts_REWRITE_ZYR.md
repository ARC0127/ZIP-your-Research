# Rewrite (portable): spreadsheets/examples/features/change_existing_charts.py

**Source (platform runtime):** `zyr_runtime_skills/spreadsheets/examples/features/change_existing_charts.py`
**Snapshot:** sha256 `9431a3594a80df040b493e2ac0616dbef4c5b0d8bcb76d9797268a24c29b31b8` · 711 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
Demonstration script showing `change_existing_charts.py` behavior in the platform spreadsheet artifact library.

## What the platform script does
- Loads an existing workbook, prints chart titles, deletes the first chart from a sheet.

## Portable template (ZYR)
In openpyxl, charts are stored on the worksheet and can be deleted, but APIs may be version-sensitive. Verify in Excel/LibreOffice.

```python
from openpyxl import load_workbook
wb = load_workbook('input.xlsx')
ws = wb['Dashboard']
print(len(ws._charts))
del ws._charts[0]
wb.save('output.xlsx')
```

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| Chart deletion | PARTIAL | Supported, but version-sensitive; verify carefully. |

## QA checklist

- [ ] Open the output workbook and confirm the intended chart is removed.
- [ ] Ensure other charts and references remain intact.
