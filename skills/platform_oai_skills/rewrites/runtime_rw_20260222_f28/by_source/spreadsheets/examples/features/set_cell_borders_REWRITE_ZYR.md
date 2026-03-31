# Rewrite (portable): spreadsheets/examples/features/set_cell_borders.py

**Source (platform runtime):** `/home/oai/skills/spreadsheets/examples/features/set_cell_borders.py`
**Snapshot:** sha256 `43fcc0f89ef9b31f0fb9f45cd3019273446720754f7e6c903079bdbe7f018b00` · 4266 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
Demonstration script showing `set_cell_borders.py` behavior in the platform spreadsheet artifact library.

## What the platform script does
- Demonstrates setting different border sides/styles (thin, thick, double, dashed, diagonal) and colors.

## Portable template (ZYR)
Use openpyxl Border/Side:

```python
from openpyxl.styles import Border, Side
thin = Side(style='thin')
ws['B2'].border = Border(bottom=thin)
ws['B10'].border = Border(left=thin, right=thin, top=thin, bottom=thin)
```

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| Borders | PASS | Portable via openpyxl. |
| Diagonal borders | PARTIAL | Supported but viewer-dependent; verify visually. |

## QA checklist

- [ ] Check borders visually in Excel/LibreOffice (some styles render differently).
