# DOCX skill — portable rewrite (compact)

This is a compact rewrite of the platform file `docs/skill.md`.

## Core invariant

Use a **visual verification loop**:

DOCX → PDF → PNG pages → human inspection → fix → repeat.

## Portable baseline

- Edit with `python-docx`
- Convert with LibreOffice headless (unique profile)
- Render with `pdftoppm`

## Key pitfalls

- LibreOffice profile lock/timeouts if you reuse the default profile.
- Unicode dashes that render incorrectly (use ASCII '-').
- Tool-internal citation tokens must never appear in user-facing documents.

For a full, file-specific rewrite see the full28 set.
