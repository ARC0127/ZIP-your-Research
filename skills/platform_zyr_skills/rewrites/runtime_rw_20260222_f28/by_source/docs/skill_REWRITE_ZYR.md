# Rewrite (portable): docs/skill.md

**Source (platform runtime):** `zyr_runtime_skills/docs/skill.md`
**Snapshot:** sha256 `3371beed114ef5a2c103367d5102c8b36ca19896e5499c266a9dea50c6bea637` · 3296 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
Guidance for reading, creating, and reviewing DOCX files with a strict render-and-verify loop.

## What the platform file emphasizes
- Convert DOCX to PDF using LibreOffice headless with a unique user profile to avoid profile lock/timeouts.
- Convert PDF to PNG images and visually inspect every page (tables/figures/layout correctness).
- Treat text extraction as last resort; visuals matter.
- Avoid problematic Unicode dashes (use ASCII '-') and ensure citations are human-readable (no tool tokens).

## Portable template (ZYR)
Use `python-docx` for editing; for verification, run a deterministic pipeline:

```bash
OUTDIR=/tmp/docx_render
mkdir -p "$OUTDIR"
soffice -env:UserInstallation=file:///tmp/lo_profile_$$ --headless --convert-to pdf --outdir "$OUTDIR" input.docx
pdftoppm -png "$OUTDIR/input.pdf" "$OUTDIR/input"
```

Open the exported PNG pages and review at 100% zoom.

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| DOCX editing | PASS | Use python-docx; keep styles consistent. |
| Visual QA loop | PASS | PDF→PNG inspection is portable via LibreOffice+pdftoppm. |
| Citation formatting | PASS | Convert tool citations to standard human-readable references. |
| Unicode dash constraints | PASS | Use ASCII '-' in generated documents. |

## QA checklist

- [ ] Run DOCX→PDF→PNG after each meaningful edit batch.
- [ ] Inspect every page at 100% zoom for clipped/overlapping text, broken tables, unreadable glyphs.
- [ ] Ensure headings/list levels are consistent and typography looks deliberate.
- [ ] Replace any tool-internal citation tokens with standard scholarly citations.
