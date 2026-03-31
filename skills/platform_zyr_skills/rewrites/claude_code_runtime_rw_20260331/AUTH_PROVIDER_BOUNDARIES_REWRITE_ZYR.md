# Auth and provider boundaries — portable rewrite (compact)

This topic condenses the files that ZYR should treat mainly as non-goal boundaries:

- `src/services/api/client.ts`
- `src/utils/auth.ts`
- `src/utils/model/configs.ts`
- `src/bridge/bridgeEnabled.ts`

## ZYR-native conclusion

These files are useful mostly because they show where **not** to copy product glue.

They encode:

- Anthropic provider selection
- Claude-specific OAuth and token refresh logic
- model-id catalogs tied to Anthropic/Bedrock/Vertex/Foundry
- subscription and entitlement checks for remote control

## What ZYR should extract

- only the architecture boundary:
  - provider adapters should stay isolated
  - auth glue should stay replaceable
  - remote execution must not assume vendor entitlements

## What ZYR must reject

- direct reuse of OAuth flows
- subscription checks
- backend contract assumptions
- vendor model catalogs as if they were ZYR-native runtime assets

For the full source-mapped layer, see:

- [client_REWRITE_ZYR.md](../claude_code_runtime_rw_20260331_f15/by_source/non_goals_boundaries/client_REWRITE_ZYR.md)
- [auth_REWRITE_ZYR.md](../claude_code_runtime_rw_20260331_f15/by_source/non_goals_boundaries/auth_REWRITE_ZYR.md)
- [configs_REWRITE_ZYR.md](../claude_code_runtime_rw_20260331_f15/by_source/non_goals_boundaries/configs_REWRITE_ZYR.md)
- [bridgeEnabled_REWRITE_ZYR.md](../claude_code_runtime_rw_20260331_f15/by_source/non_goals_boundaries/bridgeEnabled_REWRITE_ZYR.md)
