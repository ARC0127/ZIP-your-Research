# Plugin runtime and packaging — portable rewrite (compact)

This topic condenses:

- `src/utils/plugins/loadPluginCommands.ts`
- `src/utils/plugins/pluginLoader.ts`
- `src/types/plugin.ts`
- `src/plugins/builtinPlugins.ts`

## ZYR-native takeaways

Useful portable ideas:

- typed plugin manifest
- typed plugin errors
- built-in vs external plugin split
- versioned plugin cache layout
- markdown-defined commands and skills inside plugins
- plugin-provided hooks, MCP, and LSP surfaces

## Recommended ZYR shape

- `interfaces/plugin_manifest.*`
- `runtime/plugin_loader/`
- `tools/validate_plugin_manifest.*`

Adopt the packaging model conservatively: local and git-based sources first, with explicit non-goal boundaries around vendor marketplace policy.

## Source mapping and boundaries

Primary sources:

- `claude-code-sourcemap-main/restored-src/src/utils/plugins/loadPluginCommands.ts`
- `claude-code-sourcemap-main/restored-src/src/utils/plugins/pluginLoader.ts`
- `claude-code-sourcemap-main/restored-src/src/types/plugin.ts`
- `claude-code-sourcemap-main/restored-src/src/plugins/builtinPlugins.ts`

Absorb:

- manifest typing
- cache/version discipline
- prompt-asset packaging

Do not copy:

- Anthropic marketplace naming policy
- official-source enforcement rules
- product-specific plugin install/update workflows

For the full source-mapped layer, see:

- [loadPluginCommands_REWRITE_ZYR.md](../claude_code_runtime_rw_20260331_f15/by_source/skills_plugins/loadPluginCommands_REWRITE_ZYR.md)
- [pluginLoader_REWRITE_ZYR.md](../claude_code_runtime_rw_20260331_f15/by_source/skills_plugins/pluginLoader_REWRITE_ZYR.md)
- [plugin_REWRITE_ZYR.md](../claude_code_runtime_rw_20260331_f15/by_source/skills_plugins/plugin_REWRITE_ZYR.md)
- [builtinPlugins_REWRITE_ZYR.md](../claude_code_runtime_rw_20260331_f15/by_source/skills_plugins/builtinPlugins_REWRITE_ZYR.md)
