# 07 — Tool, query, and session model

This note summarizes the Claude Code runtime patterns that are most directly reusable in a ZYR-native execution layer.

## Core takeaways

### 1. Tooling should be a first-class contract

Useful fields to preserve in a ZYR runtime contract:

- input schema
- validation stage
- permission stage
- model exposure rules
- read-only vs mutating classification
- user-facing progress/activity rendering

This improves honesty: the model only sees tools that are actually allowed and meaningfully described.

### 2. Query execution should live outside the UI shell

The runtime should own:

- mutable conversation state
- file-read cache
- usage/cost accounting
- session persistence hooks
- per-turn discovery state

The UI should consume that state, not define it.

### 3. Session persistence should distinguish durable state from UI noise

ZYR should preserve:

- transcript messages
- chain participants
- durable run metadata

ZYR should not persist:

- ephemeral progress ticks
- purely cosmetic render state

## Recommended ZYR shape

- `runtime/tool_registry/`
- `runtime/query_engine/`
- `interfaces/tool_contract.*`
- `interfaces/runtime_state.*`
- `artifacts/transcripts/*.jsonl`

## Compact sources

- [../rewrites/claude_code_runtime_rw_20260331/TOOL_CONTRACT_AND_PERMISSIONS_REWRITE_ZYR.md](../rewrites/claude_code_runtime_rw_20260331/TOOL_CONTRACT_AND_PERMISSIONS_REWRITE_ZYR.md)
- [../rewrites/claude_code_runtime_rw_20260331/QUERY_ENGINE_AND_SESSION_STATE_REWRITE_ZYR.md](../rewrites/claude_code_runtime_rw_20260331/QUERY_ENGINE_AND_SESSION_STATE_REWRITE_ZYR.md)
