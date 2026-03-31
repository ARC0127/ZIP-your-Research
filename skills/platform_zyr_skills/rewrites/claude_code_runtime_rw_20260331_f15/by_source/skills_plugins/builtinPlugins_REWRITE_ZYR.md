# Rewrite (portable): src/plugins/builtinPlugins.ts

**Source (Claude Code snapshot):** `claude-code-sourcemap-main/restored-src/src/plugins/builtinPlugins.ts`  
**Snapshot:** sha256 `80ab9558ba03766b2fbd0478da00e7dadd1685904b4559c7bb3c5de51f44fbec` - 4980 bytes - mtime(UTC) `2026-03-31 08:30:12`  
**Rewrite date:** 2026-03-31

## 1. Source role

Maintains a registry of built-in plugins that ship with the runtime and can be enabled or disabled.

## 2. Ground truth extracted from source

- Built-in plugins are treated differently from bundled skills.
- They can expose skills, hooks, and MCP servers while still being user-toggleable.
- Enablement is a user setting layered on top of runtime defaults.

## 3. What ZYR should absorb

- A registry for built-in plugins.
- Default-enabled vs user-enabled distinction.
- Built-in plugin -> runtime skill expansion.

## 4. ZYR-native rewrite / interface shape

Use a small built-in registry that can emit:

- runtime plugin objects
- runtime skill entries
- default enablement metadata

## 5. What must not be copied

- Claude UI assumptions around plugin management.
- Product-specific marketplace identifiers.

## 6. Cross-links to compact topic docs

- [`PLUGIN_RUNTIME_AND_PACKAGING_REWRITE_ZYR.md`](../../../claude_code_runtime_rw_20260331/PLUGIN_RUNTIME_AND_PACKAGING_REWRITE_ZYR.md)

## 7. Maintenance note

Keep built-in plugin registration declarative; do not let built-ins bypass the manifest/component discipline.
