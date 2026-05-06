# Rewrite (portable): spreadsheets/examples/features/set_wrap_text_styles.py

**Source (platform runtime):** `zyr_runtime_skills/spreadsheets/examples/features/set_wrap_text_styles.py`
**Snapshot:** sha256 `2d107a03be0227fdbb364843cc7f9a6a68139e17257d51b26505bc82bcfa6300` · 3787 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
Demonstration script showing `set_wrap_text_styles.py` behavior in the platform spreadsheet artifact library.

## What the platform script does
- Demonstrates wrap-text behavior and cell text layout handling.

## Portable template (ZYR)
Use Alignment(wrap_text=True):

```python
from openpyxl.styles import Alignment
ws['B2'].alignment = Alignment(wrap_text=True)
```

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| Wrap text | PASS | Portable via openpyxl; row height may need manual tuning. |

## QA checklist

- [ ] Verify row heights accommodate wrapped text.
