# Rewrite (portable): spreadsheets/examples/features/set_text_alignment.py

**Source (platform runtime):** `/home/oai/skills/spreadsheets/examples/features/set_text_alignment.py`
**Snapshot:** sha256 `5c9aab970b4403e3ad93fd5070670234acbd8bf645b1492ccdc2f3e1ee2e9518` · 2831 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
Demonstration script showing `set_text_alignment.py` behavior in the platform spreadsheet artifact library.

## What the platform script does
- Demonstrates horizontal/vertical alignment options.

## Portable template (ZYR)
Use openpyxl Alignment:

```python
from openpyxl.styles import Alignment
ws['B2'].alignment = Alignment(horizontal='center', vertical='center')
```

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| Alignment | PASS | Portable via openpyxl. |

## QA checklist

- [ ] Visually verify alignment for merged cells and multi-line text.
