# Rewrite (portable): src/types/plugin.ts

**Source (Claude Code snapshot):** `claude-code-sourcemap-main/restored-src/src/types/plugin.ts`  
**Snapshot:** sha256 `a00ee3fda919c8c36b11a2cc65235dea18f83b188431cdbd4504ce4eea2a178a` - 11308 bytes - mtime(UTC) `2026-03-31 08:30:12`  
**Rewrite date:** 2026-03-31

## 1. Source role

Defines the typed plugin surface: manifest references, loaded plugin shape, component categories, and error variants.

## 2. Ground truth extracted from source

- The runtime benefits from typed plugin errors, not free-form strings.
- Built-in plugin definitions differ from loaded external plugin instances.
- Plugin components are an explicit union, not a loose convention.

## 3. What ZYR should absorb

- Typed plugin manifest references.
- Typed error unions.
- Explicit plugin component categories.

## 4. ZYR-native rewrite / interface shape

Define ZYR plugin interfaces for:

- `PluginManifest`
- `LoadedPlugin`
- `PluginComponent`
- `PluginError`

Keep component kinds stable so runtime and docs stay aligned.

## 5. What must not be copied

- Vendor-specific plugin-source assumptions.
- Error variants that exist only for Anthropic product plumbing.

## 6. Cross-links to compact topic docs

- [`PLUGIN_RUNTIME_AND_PACKAGING_REWRITE_ZYR.md`](../../../claude_code_runtime_rw_20260331/PLUGIN_RUNTIME_AND_PACKAGING_REWRITE_ZYR.md)

## 7. Maintenance note

If new component kinds are added, update both manifest typing and loader behavior together.
