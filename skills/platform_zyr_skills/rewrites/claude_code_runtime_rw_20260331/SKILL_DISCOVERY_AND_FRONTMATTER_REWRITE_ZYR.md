# Skill discovery and frontmatter — portable rewrite (compact)

This topic condenses `src/skills/loadSkillsDir.ts`.

## ZYR-native takeaways

Useful skill metadata fields:

- `name`
- `description`
- `when_to_use`
- `allowed-tools`
- `model`
- `effort`
- `user-invocable`
- `hooks`
- `paths`

Useful loading behavior:

- search layered roots in a deterministic order
- deduplicate by resolved file identity
- activate some skills conditionally when touched paths match declared patterns

## Recommended ZYR shape

- `interfaces/skill_frontmatter_schema.*`
- `runtime/skill_loader/`
- `tools/validate_skill_frontmatter.*`

This helps convert ZYR skills from static prompt assets into runtime-discoverable units without losing provenance discipline.

## Source mapping and boundaries

Primary source:

- `claude-code-sourcemap-main/restored-src/src/skills/loadSkillsDir.ts`

Absorb:

- frontmatter shape
- layered discovery
- path-scoped activation

Do not copy:

- Claude-specific directory policy assumptions
- user-setting names that only make sense in Claude Code

For the full source-mapped layer, see:

- [loadSkillsDir_REWRITE_ZYR.md](../claude_code_runtime_rw_20260331_f15/by_source/skills_plugins/loadSkillsDir_REWRITE_ZYR.md)
