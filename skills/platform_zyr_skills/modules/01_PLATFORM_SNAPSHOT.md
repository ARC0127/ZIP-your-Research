# 01 — Platform snapshot

The platform runtime files are versioned implicitly by their **hashes** and file metadata.

Authoritative snapshot for this module:
- `../rewrites/runtime_rw_20260222_f28/SOURCES.md`

## Why hashes matter

- The platform may update without notice.
- If a future run produces different outputs, hashes let you deterministically decide whether the environment changed or your pipeline changed.

## How to refresh

See `05_MAINTENANCE_DIFFING.md`.
