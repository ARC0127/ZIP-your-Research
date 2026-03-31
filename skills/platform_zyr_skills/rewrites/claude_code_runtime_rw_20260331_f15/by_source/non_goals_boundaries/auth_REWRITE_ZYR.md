# Rewrite (portable boundary): src/utils/auth.ts

**Source (Claude Code snapshot):** `claude-code-sourcemap-main/restored-src/src/utils/auth.ts`  
**Snapshot:** sha256 `930070a5da4b70c3e5ccd1853d028aaa72f7bdd437f32145a73552a8eb8555de` - 65436 bytes - mtime(UTC) `2026-03-31 08:30:12`  
**Rewrite date:** 2026-03-31

## 1. Source role

Implements the Claude Code auth chain, token sourcing, token refresh, and credential persistence.

## 2. Ground truth extracted from source

- Auth is deeply product-specific.
- Runtime behavior changes depending on OAuth, API-key, provider, and managed-session context.
- Secure storage choices are intertwined with platform-specific persistence paths.

## 3. What ZYR should absorb

- Only the architecture lesson: auth and credential storage must remain replaceable, audited, and isolated.

## 4. ZYR-native rewrite / interface shape

Define an auth boundary with:

- credential source
- refresh strategy
- persistence backend

Keep it outside the portable runtime contract layer.

## 5. What must not be copied

- Claude OAuth flow logic.
- Anthropic credential search order.
- Product-specific keychain and token rules.

## 6. Cross-links to compact topic docs

- [`AUTH_PROVIDER_BOUNDARIES_REWRITE_ZYR.md`](../../../claude_code_runtime_rw_20260331/AUTH_PROVIDER_BOUNDARIES_REWRITE_ZYR.md)

## 7. Maintenance note

If a future snapshot changes auth shape, only revisit the boundary statement unless ZYR explicitly chooses to study auth architecture further.
