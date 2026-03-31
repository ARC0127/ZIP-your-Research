# Rewrite (portable boundary): src/utils/model/configs.ts

**Source (Claude Code snapshot):** `claude-code-sourcemap-main/restored-src/src/utils/model/configs.ts`  
**Snapshot:** sha256 `f217bfc735c8e7a88703371d19210adfe4d4490c46d81179c174bcf82f13c13a` - 4286 bytes - mtime(UTC) `2026-03-31 08:30:12`  
**Rewrite date:** 2026-03-31

## 1. Source role

Catalogs Anthropic model identifiers across multiple providers.

## 2. Ground truth extracted from source

- The file is a provider-specific model catalog, not a generic runtime abstraction.
- Canonical IDs are mapped to provider-specific strings.

## 3. What ZYR should absorb

- Only the separation principle: keep model catalogs outside the runtime core and make them replaceable.

## 4. ZYR-native rewrite / interface shape

If ZYR needs model catalogs, define them as external provider configuration rather than as hard-coded runtime identity.

## 5. What must not be copied

- Anthropic model IDs.
- Provider-specific naming assumptions from Bedrock, Vertex, or Foundry.

## 6. Cross-links to compact topic docs

- [`AUTH_PROVIDER_BOUNDARIES_REWRITE_ZYR.md`](../../../claude_code_runtime_rw_20260331/AUTH_PROVIDER_BOUNDARIES_REWRITE_ZYR.md)

## 7. Maintenance note

Treat this file as a reminder to isolate model catalogs from portable runtime contracts.
