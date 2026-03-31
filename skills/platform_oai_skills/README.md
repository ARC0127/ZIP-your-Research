# platform_oai_skills — ZYR module (English prompt content)

This module vendors a **portable, ZYR-aligned rewrite** of the platform runtime skill pack found under `/home/oai/skills/**`.

- The **platform files themselves are not copied** into ZYR.
- Instead, we store:
  1) a hash-based snapshot of the platform files,
  2) portable templates (open-source tools: `python-docx`, `reportlab`, `openpyxl`),
  3) QA loops that do not depend on platform-private libraries.

**Language policy (this module):** all prompt-facing Markdown in `skills/platform_oai_skills/**` is **English-only** to keep downstream prompts consistent. (Chat responses may still default to Chinese per user preference.)

## Entry points

- Concept + usage:
  - `modules/00_OVERVIEW.md`
  - `modules/02_TEMPLATE_LIBRARY.md`
  - `modules/03_QA_LOOPS.md`
- Full 28-file rewrite set (mirrors `/home/oai/skills/**` 1:1):
  - `rewrites/runtime_rw_20260222_f28/INDEX.md`

## What is covered

Platform runtime files (28 total) in three clusters:

- DOCX: `rewrites/runtime_rw_20260222_f28/by_source/docs/skill_REWRITE_ZYR.md`, `rewrites/runtime_rw_20260222_f28/by_source/docs/render_docx_REWRITE_ZYR.md`
- PDF: `rewrites/runtime_rw_20260222_f28/by_source/pdfs/skill_REWRITE_ZYR.md`
- Spreadsheets: `rewrites/runtime_rw_20260222_f28/by_source/spreadsheets/skill_REWRITE_ZYR.md`, `rewrites/runtime_rw_20260222_f28/by_source/spreadsheets/spreadsheet_REWRITE_ZYR.md`, API/formula docs, and 19 example scripts.

## Maintenance

See `modules/05_MAINTENANCE_DIFFING.md` for a deterministic update procedure when the platform runtime changes.
