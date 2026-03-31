# Rewrite (portable): src/Tool.ts

**Source (Claude Code snapshot):** `claude-code-sourcemap-main/restored-src/src/Tool.ts`  
**Snapshot:** sha256 `29d555ab8e50de9fb005264b5334aba870f1da472198e14d0b3ab0bf86d7c49c` - 29516 bytes - mtime(UTC) `2026-03-31 08:30:12`  
**Rewrite date:** 2026-03-31

## 1. Source role

Defines the central tool contract, permission context, and per-tool lifecycle hooks used by the runtime.

## 2. Ground truth extracted from source

- A tool is more than a callable: it carries schema, validation, permission, prompt, result, and progress semantics.
- The permission context is a separate runtime structure with allow, deny, ask, and directory-scope rules.
- Tool visibility to the model can be shaped through defer or always-load behavior.

## 3. What ZYR should absorb

- A typed tool contract.
- A standalone permission context.
- Explicit model-exposure controls for tools.

## 4. ZYR-native rewrite / interface shape

Define a ZYR `ToolContract` with:

- schema
- validate
- check_permissions
- render_activity
- prompt_exposure

Keep `PermissionContext` runtime-owned and pass it into registry assembly before prompt construction.

## 5. What must not be copied

- Anthropic SDK-specific message block types.
- Claude-specific telemetry or naming conventions.

## 6. Cross-links to compact topic docs

- [`TOOL_CONTRACT_AND_PERMISSIONS_REWRITE_ZYR.md`](../../../claude_code_runtime_rw_20260331/TOOL_CONTRACT_AND_PERMISSIONS_REWRITE_ZYR.md)

## 7. Maintenance note

If the source adds new contract stages or permission modes, update both this file and the compact tool-contract note together.
