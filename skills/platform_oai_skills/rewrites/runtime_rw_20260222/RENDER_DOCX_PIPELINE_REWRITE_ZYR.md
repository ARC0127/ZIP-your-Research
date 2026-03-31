# DOCX rendering pipeline — portable rewrite (compact)

This is a compact rewrite of the platform script `docs/render_docx.py`.

## Purpose

Rasterize DOCX to per-page PNG images for QA.

## Portable baseline

A CLI-based pipeline is sufficient for most use cases:

```bash
OUTDIR=/tmp/docx_pages
mkdir -p "$OUTDIR"
soffice -env:UserInstallation=file:///tmp/lo_profile_$$ --headless --convert-to pdf --outdir "$OUTDIR" input.docx
pdftoppm -png "$OUTDIR/input.pdf" "$OUTDIR/page"
```

If you need DPI control, choose a fixed DPI (e.g., 200) and keep it explicit.
