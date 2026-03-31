# Rewrite (portable): spreadsheets/examples/features/set_number_formats.py

**Source (platform runtime):** `zyr_runtime_skills/spreadsheets/examples/features/set_number_formats.py`
**Snapshot:** sha256 `9d13a14599e280be6e24409273c4cd278bc564c75c9d0b7ff8ae9564ebcf35cd` · 4977 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
Demonstration script showing `set_number_formats.py` behavior in the platform spreadsheet artifact library.

## What the platform script does
- Demonstrates number formats (dates, currency, percentages, custom formats).

## Portable template (ZYR)
Set `cell.number_format`:

```python
ws['B2'].number_format = '0.0%'
ws['B3'].number_format = '$#,##0'
ws['B4'].number_format = 'yyyy-mm-dd'
```

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| Number formats | PASS | Portable via openpyxl; validate in viewer. |

## QA checklist

- [ ] Verify formats display correctly given locale settings.
