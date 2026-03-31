# Rewrite (portable): src/QueryEngine.ts

**Source (Claude Code snapshot):** `claude-code-sourcemap-main/restored-src/src/QueryEngine.ts`  
**Snapshot:** sha256 `7df34a6a6d106927403d49e3405dfaf70da37cae5b644b658ebaf0b877988af6` - 46630 bytes - mtime(UTC) `2026-03-31 08:30:12`  
**Rewrite date:** 2026-03-31

## 1. Source role

Owns the query lifecycle and persistent conversation state outside the terminal UI.

## 2. Ground truth extracted from source

- One engine instance owns one conversation.
- Mutable messages, file-read cache, usage totals, and permission denials persist across turns.
- Turn-scoped discovery state is reset per submission but belongs to the engine, not the UI shell.

## 3. What ZYR should absorb

- Separate execution state from UI state.
- Keep transcript, cache, and usage in one conversation engine.
- Treat skill discovery as runtime state.

## 4. ZYR-native rewrite / interface shape

Introduce a ZYR `ConversationEngine` that exposes:

- `submit_message(...)`
- persistent state
- transcript hooks
- tool gating hooks

Use the same engine across REPL, batch, and remote shells.

## 5. What must not be copied

- Vendor-specific SDK status types.
- Claude-specific message normalization assumptions.

## 6. Cross-links to compact topic docs

- [`QUERY_ENGINE_AND_SESSION_STATE_REWRITE_ZYR.md`](../../../claude_code_runtime_rw_20260331/QUERY_ENGINE_AND_SESSION_STATE_REWRITE_ZYR.md)

## 7. Maintenance note

If query state ownership moves into multiple subsystems, revisit this rewrite and keep the ZYR engine boundary explicit.
