# Rewrite (portable): spreadsheets/artifact_tool_spreadsheets_api.md

**Source (platform runtime):** `/home/oai/skills/spreadsheets/artifact_tool_spreadsheets_api.md`
**Snapshot:** sha256 `a99e138a3ecdd2d43ff637367a4a9ddf58cc123ed55de4d19d02f606c2daf6f4` · 51513 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
Reference material for an internal spreadsheet artifact API (workbook/sheet/cell/range, formatting, charts, export/render).

## What to carry over into ZYR (portable abstraction)
Even if the specific API is unavailable, you can preserve the *capability surface*:
- Construct/edit workbook and sheets
- Set values and formulas (cell + range)
- Apply formatting primitives
- Add charts and tables
- Export to XLSX and render for QA

## Portable template (ZYR)
Use openpyxl as the implementation baseline and define a thin wrapper only if you need API stability across backends.

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| API surface capture | PASS | ZYR stores the portable capability model. |
| Direct API parity | GAP | Internal classes/protos are not portable; avoid binding user workflows to them. |

## QA checklist

- [ ] Do not leak platform-internal library details into user-facing code.
- [ ] Prefer implementation-agnostic requirements (inputs/outputs/QA) over method-by-method mirroring.
