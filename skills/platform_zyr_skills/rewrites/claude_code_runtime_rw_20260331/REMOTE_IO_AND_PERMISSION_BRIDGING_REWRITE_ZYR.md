# Remote IO and permission bridging — portable rewrite (compact)

This topic condenses:

- `src/cli/remoteIO.ts`
- `src/remote/remotePermissionBridge.ts`

## ZYR-native takeaways

Remote execution is most reusable as a transport pattern:

- separate transport from runtime logic
- allow refreshed auth/header injection at reconnect time
- expose session state and metadata reporting hooks
- bridge permission requests for tools that are not loaded on the local side

## Recommended ZYR shape

- `interfaces/remote_transport.*`
- `runtime/remote_runner/`
- `artifacts/permission_ledger.*`

The portable value is the shape of the bridge, not the concrete Claude backend.

## Source mapping and boundaries

Primary sources:

- `claude-code-sourcemap-main/restored-src/src/cli/remoteIO.ts`
- `claude-code-sourcemap-main/restored-src/src/remote/remotePermissionBridge.ts`

Absorb:

- transport abstraction
- remote permission bridge
- state-reporting hooks

Do not copy:

- Claude Remote Control protocol names
- session-ingress-specific backend expectations

For the full source-mapped layer, see:

- [remoteIO_REWRITE_ZYR.md](../claude_code_runtime_rw_20260331_f15/by_source/remote_runtime/remoteIO_REWRITE_ZYR.md)
- [remotePermissionBridge_REWRITE_ZYR.md](../claude_code_runtime_rw_20260331_f15/by_source/remote_runtime/remotePermissionBridge_REWRITE_ZYR.md)
