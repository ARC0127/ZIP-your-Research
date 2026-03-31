# Rewrite (portable): spreadsheets/skill.md

**Source (platform runtime):** `zyr_runtime_skills/spreadsheets/skill.md`
**Snapshot:** sha256 `cef2ed8d3e50f618914f7d68c98c2158461f00e83ad836e1033cf236e48131ed` · 10012 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
Guidance for creating, editing, analyzing, and visualizing spreadsheets with a strong emphasis on formulas, formatting, and verification.

## What the platform file emphasizes
- Prefer a workflow that can *recalculate formulas* and *render sheets* to visually verify formatting.
- Avoid dynamic array formulas (e.g., FILTER/XLOOKUP/SORT/SEQUENCE) for compatibility reasons.
- Use simple, legible formulas; avoid volatile functions unless necessary.
- Preserve existing formatting when editing a provided workbook.

## Portable template (ZYR)
Use `openpyxl` for construction and formatting; for verification:
- Open the workbook in Excel/LibreOffice to ensure formulas calculate as intended.
- Export to PDF/PNG if you need a visual check of layout.

```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
```

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| Spreadsheet editing API | PASS | Use openpyxl; avoid environment-specific libraries in user-facing code. |
| Formula caching | PARTIAL | openpyxl does not cache results; rely on Excel/LibreOffice recalculation for final values. |
| Dynamic array formulas | PASS | Keep formulas compatible with target spreadsheet apps. |
| Preserve existing formatting | PASS | Render/inspect before edits; change minimal cells. |

## QA checklist

- [ ] No formula errors (#REF!, #DIV/0!, #VALUE!, #NAME?, etc.).
- [ ] No dynamic-array-only functions unless you can guarantee compatibility.
- [ ] Verify formulas by opening in a real spreadsheet application before delivery.
- [ ] Visually inspect key sheets (especially those with charts/tables/conditional formatting).
