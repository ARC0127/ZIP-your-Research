# Rewrite (portable): spreadsheets/examples/features/set_font_styles.py

**Source (platform runtime):** `/home/oai/skills/spreadsheets/examples/features/set_font_styles.py`
**Snapshot:** sha256 `4f2c3ee5de77e5bda20db60438ed66e268b8c154654933779504f01c89fc1a74` · 2612 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
Demonstration script showing `set_font_styles.py` behavior in the platform spreadsheet artifact library.

## What the platform script does
- Demonstrates font styles (bold/italic/size/family) for cells and ranges.

## Portable template (ZYR)
Use openpyxl Font:

```python
from openpyxl.styles import Font
ws['B2'].font = Font(bold=True, size=11, name='Calibri')
```

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| Font styling | PASS | Portable via openpyxl; fonts may substitute per OS. |

## QA checklist

- [ ] Verify font substitution does not break layout.
