# Rewrite (portable): src/utils/plugins/loadPluginCommands.ts

**Source (Claude Code snapshot):** `claude-code-sourcemap-main/restored-src/src/utils/plugins/loadPluginCommands.ts`  
**Snapshot:** sha256 `019d56133c75b3e5ac967bbc7b45e0be10a679ae27887ae5fcd5d9e6e74936c2` - 30541 bytes - mtime(UTC) `2026-03-31 08:30:12`  
**Rewrite date:** 2026-03-31

## 1. Source role

Transforms plugin-local markdown assets into runtime commands and skills.

## 2. Ground truth extracted from source

- Command naming can be derived from directory structure.
- Skills and commands share a large part of the same frontmatter surface.
- Variable substitution happens before prompt delivery, with special handling for plugin root and skill root.

## 3. What ZYR should absorb

- Markdown-defined plugin commands and skills.
- Namespace derivation from file layout.
- Safe variable substitution.

## 4. ZYR-native rewrite / interface shape

Support plugin-local prompt assets that compile into runtime entries with:

- normalized names
- parsed frontmatter
- prompt substitution
- hidden vs user-invocable distinction

## 5. What must not be copied

- Secret-bearing substitutions into model-visible prompt content.
- Claude-specific placeholder names that are not useful in ZYR.

## 6. Cross-links to compact topic docs

- [`PLUGIN_RUNTIME_AND_PACKAGING_REWRITE_ZYR.md`](../../../claude_code_runtime_rw_20260331/PLUGIN_RUNTIME_AND_PACKAGING_REWRITE_ZYR.md)

## 7. Maintenance note

Keep plugin prompt substitution conservative; if a variable can leak secrets, document it as non-portable rather than porting it.
