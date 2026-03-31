# Rewrite (portable): src/utils/plugins/pluginLoader.ts

**Source (Claude Code snapshot):** `claude-code-sourcemap-main/restored-src/src/utils/plugins/pluginLoader.ts`  
**Snapshot:** sha256 `06dc53474701f7312c4c9f2967b33097ecb220f57dd66c47099b709892f04fa9` - 110261 bytes - mtime(UTC) `2026-03-31 08:30:12`  
**Rewrite date:** 2026-03-31

## 1. Source role

Discovers, validates, caches, and loads plugins from supported sources.

## 2. Ground truth extracted from source

- Plugin loading has a real lifecycle: discovery, validation, cache resolution, and load-result reporting.
- Versioned cache paths matter for reproducibility and upgrades.
- The loader distinguishes built-in and external plugin families.

## 3. What ZYR should absorb

- Typed plugin loading lifecycle.
- Versioned cache layout.
- Explicit plugin load results and errors.

## 4. ZYR-native rewrite / interface shape

Implement a small ZYR plugin loader that supports:

- local paths
- git-based sources
- versioned cache directories
- typed failure reasons

## 5. What must not be copied

- Anthropic marketplace policy enforcement.
- Vendor-specific repository trust rules.

## 6. Cross-links to compact topic docs

- [`PLUGIN_RUNTIME_AND_PACKAGING_REWRITE_ZYR.md`](../../../claude_code_runtime_rw_20260331/PLUGIN_RUNTIME_AND_PACKAGING_REWRITE_ZYR.md)

## 7. Maintenance note

If ZYR ever adds a marketplace, keep policy rules in a separate layer from the portable loader contract.
