# 05 — Maintenance and diffing

## When to refresh

Refresh this module if any of these are true:
- `zyr_runtime_skills/**` hash snapshot changed
- Platform toolchain behavior changed (rendering, formula eval, exports)
- You need to support a new spreadsheet feature (new chart/table types, etc.)

## Deterministic procedure (no guesswork)

1) Collect the platform file list:
   - `find zyr_runtime_skills -type f | sort`
2) Compute sha256 for each file and compare to:
   - `../rewrites/runtime_rw_20260222_f28/SOURCES.md`
3) If hashes changed, update:
   - `SOURCES.md` (authoritative)
   - Any affected per-file rewrites in `../rewrites/runtime_rw_20260222_f28/by_source/**`
4) Append a changelog entry and bump patch version.

## Rules

- Do not copy platform-private code into user-facing templates.
- Keep rewrites focused on *behavioral intent* + *portable templates* + *QA invariants*.
