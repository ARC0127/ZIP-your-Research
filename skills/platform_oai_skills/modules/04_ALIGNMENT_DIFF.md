# 04 — Alignment diff (platform vs portable ZYR)

This module separates **what must remain invariant** from **what is runtime-specific**.

## Invariants (should stay the same)

- Visual QA loops: DOCX/PDF/Spreadsheet should be inspected visually before shipping.
- Compatibility discipline: avoid features that break common viewers (dynamic array functions, volatile formulas).
- Citation hygiene: no tool-internal citation tokens in user-facing outputs.

## Runtime-specific (do not rely on outside the platform)

- Platform-private spreadsheet artifact library and formula engine.
- Platform "render to PNG" functionality for spreadsheets (portable substitutes exist but differ).
- Platform-specific "cite tether" metadata on cells/ranges.

## How to document gaps

Use the per-file rewrites (full28) and mark:
- PASS: portable baseline can reproduce the user-visible behavior
- PARTIAL: achievable but requires external viewer or manual verification
- GAP: platform-only concept; provide an alternative (comments / source columns / external docs)
