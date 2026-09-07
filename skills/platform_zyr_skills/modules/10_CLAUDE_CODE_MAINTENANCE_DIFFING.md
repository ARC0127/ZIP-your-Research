# 10 — Claude Code maintenance and diffing

## When to refresh

Refresh the Claude Code runtime rewrite pack if any of these are true:

- the `claude-code-sourcemap-main` snapshot changes
- the selected 15-file subset changes
- the runtime architecture meaningfully shifts in tools, sessions, skills, plugins, or remote execution
- ZYR decides to absorb additional files or retire some current non-goal boundaries

## Deterministic procedure

1. Re-extract or re-open the authoritative snapshot source.
2. Recompute the 15-file metadata table used by:
   - `../rewrites/claude_code_runtime_rw_20260331/SOURCES.md`
   - `../rewrites/claude_code_runtime_rw_20260331/SOURCES.md`
3. Compare the old and new source list.
4. If the source set changed, update:
   - compact topic notes
   - full source-mapped rewrites
   - `INDEX.md` in the full set
   - this maintenance note if category boundaries changed
5. Keep the split stable:
   - `Core Runtime`
   - `Skills & Plugins`
   - `Remote Runtime`
   - `Non-goals / Boundaries`

## Rules

- Do not copy private auth, subscription, or backend logic into ZYR-native templates.
- Preserve logical source paths in `SOURCES.md`; do not bake machine-specific absolute paths into rewrite artifacts.
- Keep every full rewrite dual-layered:
  - what ZYR should absorb
  - what ZYR must explicitly reject
- Update compact and full rewrite layers together.
