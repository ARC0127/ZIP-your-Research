# Rewrite (portable): src/remote/remotePermissionBridge.ts

**Source (Claude Code snapshot):** `claude-code-sourcemap-main/restored-src/src/remote/remotePermissionBridge.ts`  
**Snapshot:** sha256 `9cbdfa6a25969aeaea03df130238f421809061daaee651aa58144f29f7c0d131` - 2378 bytes - mtime(UTC) `2026-03-31 08:30:12`  
**Rewrite date:** 2026-03-31

## 1. Source role

Bridges remote permission requests into local runtime-compatible tool and assistant-message shapes.

## 2. Ground truth extracted from source

- Remote permission prompts may need synthetic local wrappers.
- Tool stubs can stand in for tools that do not exist locally.
- The bridge focuses on preserving permission semantics, not remote business logic.

## 3. What ZYR should absorb

- Synthetic wrappers for remote permission review.
- Tool stubs for unknown remote tools.
- Local-side permission mediation for remote runs.

## 4. ZYR-native rewrite / interface shape

Define a `RemotePermissionBridge` that can build:

- synthetic request records
- tool stubs
- local approval surfaces

## 5. What must not be copied

- Claude-specific assistant message shapes.
- Product-specific permission request wire details.

## 6. Cross-links to compact topic docs

- [`REMOTE_IO_AND_PERMISSION_BRIDGING_REWRITE_ZYR.md`](../../../claude_code_runtime_rw_20260331/REMOTE_IO_AND_PERMISSION_BRIDGING_REWRITE_ZYR.md)

## 7. Maintenance note

If remote tool schemas get richer, keep the bridge focused on mediation and do not let it become a hidden protocol clone.
