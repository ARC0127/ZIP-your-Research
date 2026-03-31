# 09 — Remote IO and boundaries

The Claude Code remote path is valuable to ZYR mainly as a transport-pattern reference.

## What is reusable

- a transport abstraction instead of hard-coding one remote backend
- explicit session token/header refresh hooks
- state and metadata reporting hooks
- permission request bridging for tools not loaded locally

## What is not reusable

- Claude Remote Control backend semantics
- Anthropic session-ingress assumptions
- account entitlement checks
- claude.ai subscription requirements

## ZYR-native target

If ZYR adds remote execution, the portable shape should be:

- remote transport interface
- session state reporter
- permission bridge
- transcript/internal-event adapter

This should live behind ZYR-owned contracts, not vendor-specific protocol names.

## Compact sources

- [../rewrites/claude_code_runtime_rw_20260331/REMOTE_IO_AND_PERMISSION_BRIDGING_REWRITE_ZYR.md](../rewrites/claude_code_runtime_rw_20260331/REMOTE_IO_AND_PERMISSION_BRIDGING_REWRITE_ZYR.md)
- [../rewrites/claude_code_runtime_rw_20260331/AUTH_PROVIDER_BOUNDARIES_REWRITE_ZYR.md](../rewrites/claude_code_runtime_rw_20260331/AUTH_PROVIDER_BOUNDARIES_REWRITE_ZYR.md)
