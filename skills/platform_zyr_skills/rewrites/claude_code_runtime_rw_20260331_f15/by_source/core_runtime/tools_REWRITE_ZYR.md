# Rewrite (portable): src/tools.ts

**Source (Claude Code snapshot):** `claude-code-sourcemap-main/restored-src/src/tools.ts`  
**Snapshot:** sha256 `4307f3f7dec2916299cc2fa5c45df8b95fd9a1945be7ac918ccd3d47a42f18cb` - 17294 bytes - mtime(UTC) `2026-03-31 08:30:12`  
**Rewrite date:** 2026-03-31

## 1. Source role

Assembles the runtime tool pool, filters tools through permission rules, and merges built-in and external tools.

## 2. Ground truth extracted from source

- There is one source of truth for built-in tool assembly.
- Blanket deny rules are applied before the model sees the tool list.
- Built-in and external tools are sorted and deduplicated for stable prompt construction.

## 3. What ZYR should absorb

- One registry assembly path for all runtime tools.
- Pre-prompt deny filtering.
- Stable sort and dedupe rules when multiple tool families are merged.

## 4. ZYR-native rewrite / interface shape

Expose a single registry function such as `assemble_runtime_tools(permission_context, builtin_tools, external_tools)` and make all callers use it.

## 5. What must not be copied

- Claude Code feature-flag branching as a design default.
- Product-specific tool availability branches tied to internal builds.

## 6. Cross-links to compact topic docs

- [`TOOL_CONTRACT_AND_PERMISSIONS_REWRITE_ZYR.md`](../../../claude_code_runtime_rw_20260331/TOOL_CONTRACT_AND_PERMISSIONS_REWRITE_ZYR.md)

## 7. Maintenance note

If new external tool families appear, keep the merge path centralized rather than adding parallel registries.
