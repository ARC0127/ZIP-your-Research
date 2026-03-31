# Rewrite (portable): src/cli/remoteIO.ts

**Source (Claude Code snapshot):** `claude-code-sourcemap-main/restored-src/src/cli/remoteIO.ts`  
**Snapshot:** sha256 `c1376ac176c001568942eedc13dc2a6afe1792147a2b6208eea734ed7fac5a2b` - 9946 bytes - mtime(UTC) `2026-03-31 08:30:12`  
**Rewrite date:** 2026-03-31

## 1. Source role

Wraps structured remote IO around a transport abstraction and manages state/reporting hooks for remote sessions.

## 2. Ground truth extracted from source

- Remote transport is abstracted from the higher-level runtime.
- Headers can be refreshed dynamically when tokens change.
- Session metadata, state, and internal events are surfaced through explicit hooks.

## 3. What ZYR should absorb

- Transport abstraction.
- Reconnect-safe header refresh.
- Session state and metadata hooks.

## 4. ZYR-native rewrite / interface shape

Build a `RemoteRuntimeTransport` plus a `RemoteSessionIO` layer that owns:

- connect
- on_data
- state reporting
- internal event flushing

## 5. What must not be copied

- Claude-specific CCR or session-ingress protocol details.
- Vendor-specific environment variable names.

## 6. Cross-links to compact topic docs

- [`REMOTE_IO_AND_PERMISSION_BRIDGING_REWRITE_ZYR.md`](../../../claude_code_runtime_rw_20260331/REMOTE_IO_AND_PERMISSION_BRIDGING_REWRITE_ZYR.md)
- [`AUTH_PROVIDER_BOUNDARIES_REWRITE_ZYR.md`](../../../claude_code_runtime_rw_20260331/AUTH_PROVIDER_BOUNDARIES_REWRITE_ZYR.md)

## 7. Maintenance note

If ZYR adds remote execution, keep transport contracts provider-agnostic from the first implementation.
