## 5) Formal Adapter

Use `S433` only when formalization is explicitly requested or clearly beneficial.

### What it does
- suggest autoformalization candidates
- extract lemma inventory
- produce a Lean-oriented sketch
- record formal gaps and unsupported steps

### What it does not do
- it does not replace the natural-language audit
- it does not block the main proof-verification path if unavailable
- it does not allow the engine to claim a proof is verified merely because a formal sketch was proposed

### Output requirements
- `autoformalization_candidates`
- `lemma_inventory`
- `lean_sketch`
- `formal_gap_record`
- `verification_record`

### Adapter template
When `S433` is active, structure the adapter block as:
- `target_system`
- `candidate_statement_1..n`
- `lemma_inventory`
- `lean_sketch`
- `formal_gap_record`
- `non_blocking_status`
