# platform_zyr_skills — ZYR module (English prompt content)

This module stores **portable, ZYR-aligned rewrites** of runtime-facing skill packs and runtime architectures that are useful to preserve inside ZYR without copying private implementation details wholesale.

Today it covers two source families:

1. The platform runtime skill pack under `zyr_runtime_skills/**`
2. The Claude Code runtime architecture reconstructed from `claude-code-sourcemap-main`

For both families, the goal is the same:

- keep a verifiable snapshot
- extract portable patterns
- rewrite them in ZYR-native terms
- mark hard boundaries where private or product-specific behavior must not be copied

**Language policy (this module):** all prompt-facing Markdown in `skills/platform_zyr_skills/**` is **English-only** to keep downstream prompts consistent. Chat responses may still default to Chinese per user preference.

## Entry points

- Module overview and source-family split:
  - [modules/00_OVERVIEW.md](modules/00_OVERVIEW.md)
  - [modules/06_CLAUDE_CODE_RUNTIME_OVERVIEW.md](modules/06_CLAUDE_CODE_RUNTIME_OVERVIEW.md)
- Portable templates and QA loops:
  - [modules/02_TEMPLATE_LIBRARY.md](modules/02_TEMPLATE_LIBRARY.md)
  - [modules/03_QA_LOOPS.md](modules/03_QA_LOOPS.md)
- Claude Code runtime architecture notes:
  - [modules/07_TOOL_QUERY_SESSION_MODEL.md](modules/07_TOOL_QUERY_SESSION_MODEL.md)
  - [modules/08_SKILL_PLUGIN_PACKAGING_MODEL.md](modules/08_SKILL_PLUGIN_PACKAGING_MODEL.md)
  - [modules/09_REMOTE_IO_AND_BOUNDARIES.md](modules/09_REMOTE_IO_AND_BOUNDARIES.md)
- Full source-mapped rewrite sets:
  - [rewrites/runtime_rw_20260222_f28/INDEX.md](rewrites/runtime_rw_20260222_f28/INDEX.md)
  - [rewrites/claude_code_runtime_rw_20260331_f15/INDEX.md](rewrites/claude_code_runtime_rw_20260331_f15/INDEX.md)

## What is covered

### Platform runtime family

Platform runtime files (28 total) in three clusters:

- DOCX: `rewrites/runtime_rw_20260222_f28/by_source/docs/skill_REWRITE_ZYR.md`, `rewrites/runtime_rw_20260222_f28/by_source/docs/render_docx_REWRITE_ZYR.md`
- PDF: `rewrites/runtime_rw_20260222_f28/by_source/pdfs/skill_REWRITE_ZYR.md`
- Spreadsheets: `rewrites/runtime_rw_20260222_f28/by_source/spreadsheets/skill_REWRITE_ZYR.md`, `rewrites/runtime_rw_20260222_f28/by_source/spreadsheets/spreadsheet_REWRITE_ZYR.md`, API/formula docs, and 19 example scripts.

### Claude Code runtime family

Claude Code runtime files (15 total) in four clusters:

- Core Runtime: `Tool.ts`, `tools.ts`, `QueryEngine.ts`, `sessionStorage.ts`
- Skills & Plugins: `loadSkillsDir.ts`, `loadPluginCommands.ts`, `pluginLoader.ts`, `plugin.ts`, `builtinPlugins.ts`
- Remote Runtime: `remoteIO.ts`, `remotePermissionBridge.ts`
- Non-goals / Boundaries: `client.ts`, `auth.ts`, `configs.ts`, `bridgeEnabled.ts`

The authoritative 1:1 map lives under `rewrites/claude_code_runtime_rw_20260331_f15/`.

## Maintenance

- See [modules/05_MAINTENANCE_DIFFING.md](modules/05_MAINTENANCE_DIFFING.md) for platform runtime refresh rules.
- See [modules/10_CLAUDE_CODE_MAINTENANCE_DIFFING.md](modules/10_CLAUDE_CODE_MAINTENANCE_DIFFING.md) for Claude Code runtime refresh rules.
