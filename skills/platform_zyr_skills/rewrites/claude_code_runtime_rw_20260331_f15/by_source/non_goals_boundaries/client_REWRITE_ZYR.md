# Rewrite (portable boundary): src/services/api/client.ts

**Source (Claude Code snapshot):** `claude-code-sourcemap-main/restored-src/src/services/api/client.ts`  
**Snapshot:** sha256 `1446470ddd046c95d8254dfd0d6af821cd5b6f4b6eaddd43a8859e5e93d4966a` - 16164 bytes - mtime(UTC) `2026-03-31 08:30:12`  
**Rewrite date:** 2026-03-31

## 1. Source role

Constructs provider clients for Anthropic, Bedrock, Vertex, and Foundry.

## 2. Ground truth extracted from source

- Provider selection is product glue.
- Auth refresh and request headers are tightly coupled to provider choice.
- Model invocation here assumes Anthropic-family backends.

## 3. What ZYR should absorb

- Only the boundary lesson: provider adapters should be isolated from the main runtime.

## 4. ZYR-native rewrite / interface shape

Keep provider adapters behind a replaceable `ModelProvider` interface rather than embedding vendor selection into the core runtime.

## 5. What must not be copied

- Anthropic provider logic.
- Bedrock, Vertex, or Foundry specific auth/header handling.

## 6. Cross-links to compact topic docs

- [`AUTH_PROVIDER_BOUNDARIES_REWRITE_ZYR.md`](../../../claude_code_runtime_rw_20260331/AUTH_PROVIDER_BOUNDARIES_REWRITE_ZYR.md)

## 7. Maintenance note

This file is a boundary marker. If ZYR adopts a provider adapter layer, document it independently rather than porting this implementation.
