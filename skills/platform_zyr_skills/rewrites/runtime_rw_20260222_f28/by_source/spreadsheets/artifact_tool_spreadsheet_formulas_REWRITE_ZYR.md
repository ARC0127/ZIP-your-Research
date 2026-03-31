# Rewrite (portable): spreadsheets/artifact_tool_spreadsheet_formulas.md

**Source (platform runtime):** `zyr_runtime_skills/spreadsheets/artifact_tool_spreadsheet_formulas.md`
**Snapshot:** sha256 `b5299c87e4dc0a2e0c077eec369a4998cd890a69b32fbb28572c73c272c4b228` · 50238 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
A compatibility matrix indicating which spreadsheet functions are supported by the platform formula engine.

## What to carry over into ZYR
- Keep formulas simple and widely supported by Excel/LibreOffice.
- Avoid dynamic-array-only functions when portability matters.
- When using advanced functions, verify in the target application.

## Portable template (ZYR)
Maintain a project-level 'allowed functions' policy for deliverables, e.g.:
- Allowed: SUM, AVERAGE, MIN/MAX, IF, INDEX/MATCH, ROUND, TEXT, DATE/TIME basics
- Caution: OFFSET, INDIRECT, volatile functions
- Avoid: FILTER/SORT/SEQUENCE/XLOOKUP unless your target environment is guaranteed

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| Portability policy | PASS | ZYR encodes rules-of-thumb rather than a backend-specific matrix. |
| Exact support matrix replication | GAP | Backend-specific; not stable across environments. |

## QA checklist

- [ ] List any non-trivial functions used in the workbook and verify in the target spreadsheet app.
- [ ] Prefer helper cells over deeply nested formulas for debuggability.
