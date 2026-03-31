# Query engine and session state — portable rewrite (compact)

This topic condenses `src/QueryEngine.ts` and `src/utils/sessionStorage.ts`.

## ZYR-native takeaways

The runtime should own conversation execution state outside the UI shell.

Useful portable behaviors:

- one engine per conversation
- persistent mutable message store across turns
- file-read cache owned by the engine
- explicit usage/cost tracking
- transcript persistence as a durable artifact
- separation between durable transcript messages and ephemeral progress noise

## Recommended ZYR shape

- `runtime/query_engine/`
- `interfaces/runtime_state.*`
- `artifacts/transcripts/*.jsonl`
- `artifacts/run_state.json`

This is the strongest candidate for immediate absorption because it complements ZYR's artifact-first discipline directly.

## Source mapping and boundaries

Primary sources:

- `claude-code-sourcemap-main/restored-src/src/QueryEngine.ts`
- `claude-code-sourcemap-main/restored-src/src/utils/sessionStorage.ts`

Absorb:

- execution-state ownership
- transcript durability
- durable vs ephemeral message distinctions

Do not copy:

- vendor-specific message/event names
- backend-specific session ingress assumptions

For the full source-mapped layer, see:

- [QueryEngine_REWRITE_ZYR.md](../claude_code_runtime_rw_20260331_f15/by_source/core_runtime/QueryEngine_REWRITE_ZYR.md)
- [sessionStorage_REWRITE_ZYR.md](../claude_code_runtime_rw_20260331_f15/by_source/core_runtime/sessionStorage_REWRITE_ZYR.md)
