# 08 — Skill and plugin packaging model

Claude Code is useful to ZYR here because it treats prompt assets as runtime-loadable units rather than as static prose only.

## Skill packaging takeaways

Useful frontmatter fields:

- `name`
- `description`
- `when_to_use`
- `allowed-tools`
- `model`
- `effort`
- `user-invocable`
- `hooks`
- `paths`

Useful loading behaviors:

- layered discovery from managed, user, and project roots
- dedup by resolved file identity
- conditional activation based on touched paths

## Plugin packaging takeaways

Useful portable ideas:

- built-in vs external plugin split
- typed plugin manifest
- typed plugin errors
- versioned plugin cache layout
- plugin-provided commands, skills, hooks, MCP, and LSP surfaces

## ZYR adaptation rule

Absorb the packaging model, not the vendor policy layer.

Keep:

- manifest typing
- cache/version discipline
- markdown-defined prompt assets

Reject:

- Anthropic marketplace branding rules
- official-source impersonation policy
- product-specific install/update assumptions

## Compact sources

- [../rewrites/claude_code_runtime_rw_20260331/SKILL_DISCOVERY_AND_FRONTMATTER_REWRITE_ZYR.md](../rewrites/claude_code_runtime_rw_20260331/SKILL_DISCOVERY_AND_FRONTMATTER_REWRITE_ZYR.md)
- [../rewrites/claude_code_runtime_rw_20260331/PLUGIN_RUNTIME_AND_PACKAGING_REWRITE_ZYR.md](../rewrites/claude_code_runtime_rw_20260331/PLUGIN_RUNTIME_AND_PACKAGING_REWRITE_ZYR.md)
