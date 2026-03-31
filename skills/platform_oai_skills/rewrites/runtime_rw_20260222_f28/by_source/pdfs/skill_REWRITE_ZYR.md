# Rewrite (portable): pdfs/skill.md

**Source (platform runtime):** `/home/oai/skills/pdfs/skill.md`
**Snapshot:** sha256 `76af35f8932f3cda08a5438605f87789670bd90d720f67cf0aa7af9ddad4e7f4` · 3120 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
Guidance for reading, creating, and reviewing PDF files with a strict render-and-verify loop.

## What the platform file emphasizes
- Prefer PDF→PNG rendering (`pdftoppm`) for inspection; text extraction misses layout defects.
- Generate PDFs programmatically with `reportlab` as the primary tool.
- Avoid Unicode dashes that render poorly; keep citations human-readable (no tool tokens).

## Portable template (ZYR)
Create with reportlab; verify every page via PNG rendering:

```bash
pdftoppm -png input.pdf /tmp/input_page
```

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| PDF generation with reportlab | PASS | Reportlab is a portable baseline. |
| Visual QA loop | PASS | pdftoppm is widely available; otherwise use poppler equivalents. |
| Citation formatting | PASS | Always convert internal tokens to standard citations. |

## QA checklist

- [ ] Render every page to PNG after meaningful layout changes.
- [ ] Check for clipped/overlapping elements, broken tables, unreadable glyphs.
- [ ] Ensure charts/diagrams are readable without excessive zoom.
