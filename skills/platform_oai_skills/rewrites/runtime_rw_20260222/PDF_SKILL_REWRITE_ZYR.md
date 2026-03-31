# PDF skill — portable rewrite (compact)

This is a compact rewrite of the platform file `pdfs/skill.md`.

## Core invariant

PDF → PNG pages → inspection → fix → repeat.

## Portable baseline

- Create: `reportlab`
- Inspect: `pdftoppm -png`

## Pitfalls

- Rendering defects (clipped elements, broken tables, unreadable glyphs).
- Citation tokens that are not human-readable.
