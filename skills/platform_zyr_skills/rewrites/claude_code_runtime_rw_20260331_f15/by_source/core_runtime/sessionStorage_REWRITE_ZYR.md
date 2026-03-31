# Rewrite (portable): src/utils/sessionStorage.ts

**Source (Claude Code snapshot):** `claude-code-sourcemap-main/restored-src/src/utils/sessionStorage.ts`  
**Snapshot:** sha256 `8a123ebce1ee72b9081d34b8f3697e5fcc9c7576df5b98e4206bb28414134412` - 180620 bytes - mtime(UTC) `2026-03-31 08:30:12`  
**Rewrite date:** 2026-03-31

## 1. Source role

Persists session transcripts and runtime log records while preserving the conversation chain.

## 2. Ground truth extracted from source

- Durable transcript messages are separated from ephemeral progress events.
- Chain-participant logic exists to prevent progress-only entries from corrupting replay.
- Session paths are derived carefully to avoid path drift across resume contexts.

## 3. What ZYR should absorb

- JSONL transcript persistence.
- Transcript schema that excludes ephemeral progress.
- Audit-friendly chain hygiene rules.

## 4. ZYR-native rewrite / interface shape

Store transcript artifacts under a stable ZYR path and define explicit types for:

- transcript entry
- chain participant
- ephemeral progress

Provide one transcript loader and one transcript auditor.

## 5. What must not be copied

- Vendor-specific event names or internal session-ingress assumptions.
- Claude product-specific session directory semantics.

## 6. Cross-links to compact topic docs

- [`QUERY_ENGINE_AND_SESSION_STATE_REWRITE_ZYR.md`](../../../claude_code_runtime_rw_20260331/QUERY_ENGINE_AND_SESSION_STATE_REWRITE_ZYR.md)

## 7. Maintenance note

If transcript durability rules change, update the compact session-state note and any ZYR artifact schema together.
