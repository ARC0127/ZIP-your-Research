# Tool contract and permissions — portable rewrite (compact)

This topic condenses the Claude Code files `src/Tool.ts` and `src/tools.ts`.

## ZYR-native takeaways

ZYR should treat tools as a first-class runtime contract, not as loose prompt hints.

Useful portable fields:

- input schema
- validation hook
- permission hook
- read-only vs mutating classification
- user-facing activity/progress rendering
- model exposure controls such as defer/always-load behavior

Useful runtime behavior:

- filter denied tools before the model sees them
- assemble built-in and external tools through one registry path
- keep permission context separate from UI state

## Recommended ZYR shape

- `interfaces/tool_contract.*`
- `interfaces/permission_contract.*`
- `runtime/tool_registry/`

The main value is honesty and bounded execution: the model only sees tools that are actually available and policy-allowed.

## Source mapping and boundaries

Primary sources:

- `claude-code-sourcemap-main/restored-src/src/Tool.ts`
- `claude-code-sourcemap-main/restored-src/src/tools.ts`

Absorb:

- typed tool contract
- tool-pool assembly
- pre-prompt deny filtering

Do not copy:

- Anthropic-specific tool metadata conventions
- build-flag-heavy feature gating patterns

For the full source-mapped layer, see:

- [Tool_REWRITE_ZYR.md](../claude_code_runtime_rw_20260331_f15/by_source/core_runtime/Tool_REWRITE_ZYR.md)
- [tools_REWRITE_ZYR.md](../claude_code_runtime_rw_20260331_f15/by_source/core_runtime/tools_REWRITE_ZYR.md)
