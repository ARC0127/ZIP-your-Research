# Rewrite (portable boundary): src/bridge/bridgeEnabled.ts

**Source (Claude Code snapshot):** `claude-code-sourcemap-main/restored-src/src/bridge/bridgeEnabled.ts`  
**Snapshot:** sha256 `214d6b6d23da9f40b2b4e3b859e8ecad743557a9e4a3cf61489eb306fd1a5d61` - 8442 bytes - mtime(UTC) `2026-03-31 08:30:12`  
**Rewrite date:** 2026-03-31

## 1. Source role

Determines whether Claude remote-control features are enabled for the current account and build.

## 2. Ground truth extracted from source

- Remote enablement is tied to product entitlement, profile scope, and vendor feature gating.
- The remote path assumes a Claude-specific OAuth-backed account model.

## 3. What ZYR should absorb

- Only the boundary lesson: remote execution enablement should be explicit and separated from transport logic.

## 4. ZYR-native rewrite / interface shape

If ZYR gates remote execution, do it with ZYR-owned policy and environment checks, not vendor subscription logic.

## 5. What must not be copied

- claude.ai subscription checks.
- GrowthBook-style vendor gating for portable runtime behavior.

## 6. Cross-links to compact topic docs

- [`AUTH_PROVIDER_BOUNDARIES_REWRITE_ZYR.md`](../../../claude_code_runtime_rw_20260331/AUTH_PROVIDER_BOUNDARIES_REWRITE_ZYR.md)
- [`REMOTE_IO_AND_PERMISSION_BRIDGING_REWRITE_ZYR.md`](../../../claude_code_runtime_rw_20260331/REMOTE_IO_AND_PERMISSION_BRIDGING_REWRITE_ZYR.md)

## 7. Maintenance note

Keep enablement policy separate from transport and session logic in any future ZYR remote runtime.
