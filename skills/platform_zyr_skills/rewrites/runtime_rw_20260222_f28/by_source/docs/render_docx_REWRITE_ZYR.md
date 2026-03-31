# Rewrite (portable): docs/render_docx.py

**Source (platform runtime):** `zyr_runtime_skills/docs/render_docx.py`
**Snapshot:** sha256 `aa90e7455a45ffb1051cda0db3bc5a39fe402e93f178197e471f84fc864bbe01` · 9074 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
A small utility to rasterize DOCX-like inputs into per-page PNG images, choosing DPI to fit within target pixel bounds.

## What the platform script does (high-level)
- Computes a reasonable DPI either from DOCX OOXML page size (twips) or from the converted PDF page size (points).
- Converts input to PDF via LibreOffice headless using a unique user profile directory.
- Rasterizes the PDF to PNG via `pdf2image.convert_from_path` and normalizes output filenames to `page-<N>.png`.

## Portable template (ZYR)
If you only need a stable verification loop, a pure-CLI version is often sufficient:

```bash
OUTDIR=/tmp/docx_pages
mkdir -p "$OUTDIR"
soffice -env:UserInstallation=file:///tmp/lo_profile_$$ --headless --convert-to pdf --outdir "$OUTDIR" input.docx
pdftoppm -png "$OUTDIR/input.pdf" "$OUTDIR/page"
```

If you need DPI control, treat it as an input parameter (e.g., 150–300) rather than relying on complex heuristics.

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| Core functionality (DOCX→PNG pages) | PASS | CLI pipeline provides equivalent output for QA. |
| Auto DPI heuristics | PARTIAL | Platform computes DPI from OOXML/PDF; portable workflows can accept a fixed DPI. |
| Concurrency-safe LO profile | PASS | Use `-env:UserInstallation=file:///tmp/lo_profile_$$`. |

## QA checklist

- [ ] Use a unique LibreOffice profile directory per run to avoid lock/timeouts.
- [ ] Confirm output filenames are deterministic and ordered by page number.
- [ ] Verify that the rasterized PNGs preserve table/figure legibility at normal zoom.
