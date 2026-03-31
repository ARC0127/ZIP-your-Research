## 3) Progressive Verification

Use `S241` semantics.

### Multi-scale workflow
1) Review the whole proof first.
2) If still unresolved, split the proof into chunks while preserving the full proof as context.
3) Review each chunk independently.
4) Record chunk-level verdicts and explanations.
5) Prune branches that already contain a fatal flaw.
6) Keep drilling down until the minimum chunk size or iteration budget is reached.

### Output requirements
- `iteration_log` with columns:
  - `iter`
  - `granularity`
  - `active_scope`
  - `new_findings`
  - `continue_or_stop`
- `chunk_verdict_matrix` with columns:
  - `iter`
  - `chunk_id`
  - `source_span`
  - `context_retained`
  - `local_verdict`
  - `fatality`
  - `first_error`
  - `prune_decision`
- `pruned_branch_list`
- `first_error_report`
- `proof_verdict`

### Why this exists
- Whole-proof review catches coarse mistakes quickly.
- Chunk-level review exposes local derivation or theorem-use errors that a single pass may miss.
- The chunk matrix is the default carrier for long-proof evidence; do not summarize away the failing chunk.
