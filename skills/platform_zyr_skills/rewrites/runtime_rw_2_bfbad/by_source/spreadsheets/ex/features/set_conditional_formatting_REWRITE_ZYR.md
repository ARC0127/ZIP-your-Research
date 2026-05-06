# Rewrite (portable): spreadsheets/examples/features/set_conditional_formatting.py

**Source (platform runtime):** `zyr_runtime_skills/spreadsheets/examples/features/set_conditional_formatting.py`
**Snapshot:** sha256 `69cc7d58ebe5fc83179760275194c132792a26d10d12c28c7187a9dc5c7dab96` · 9036 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
Demonstration script showing `set_conditional_formatting.py` behavior in the platform spreadsheet artifact library.

## What the platform script does
- Demonstrates conditional formatting rules over ranges (e.g., not-blank checks).

## Portable template (ZYR)
Use openpyxl conditional formatting rules:

```python
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.styles import PatternFill

dxf = DifferentialStyle(fill=PatternFill('solid', fgColor='B7E1CD'))
rule = FormulaRule(formula=['LEN(A1)>0'], dxf=dxf)
ws.conditional_formatting.add('A1:D1', rule)
```

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| Conditional formatting | PASS | Portable via openpyxl; verify in viewer. |

## QA checklist

- [ ] Verify rules trigger as expected in Excel/LibreOffice.
