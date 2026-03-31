## 1) Proof Verification Profile

Activate this engine when the task is theorem-, proof-, or derivation-heavy.

### Default profile
- `verifier_mode: pessimistic_progressive`
- `first_error_wins: true`
- `proof_refinement_loop: on`
- `majority_vote: diagnostic_only`
- `formal_adapter: optional`
- `annotation_or_rigor_mismatch_label: enabled`

### Routing policy
- If the user asks for theorem/proof verification: `F_proof_idea -> proof_engine -> S237/S240/S241/S235`
- If the user asks for line-by-line derivation audit: `C_calculation -> proof_engine -> S326/S237/S240`
- If the user explicitly asks for Lean / autoformalization / theorem prover adaptation: add `S433`

### Minimal inputs
Ask only for the smallest missing set:
1) theorem statement or target claim
2) proof text / derivation steps
3) definitions, assumptions, and available lemmas
4) rigor target if the user already has one

### Canonical output order
When `proof_engine` is the primary engine, emit blocks in this order unless the user explicitly asks for another format:
1) `THEOREM_NORMALIZATION`
2) `ASSUMPTION_TABLE`
3) `LEMMA_DEPENDENCY_GRAPH`
4) `DERIVATION_LEDGER` or `N/A`
5) `REVIEW_MATRIX` or `CHUNK_VERDICT_MATRIX`
6) `VERIFICATION_RECORD`
7) optional `REPAIR_PROPOSAL`
8) optional `FORMAL_ADAPTER`

### Artifact binding
- For theorem-/proof-heavy tasks, `artifacts/proof_casebook.md` is an authoritative deliverable, not an optional note.
- Map proof-related claims into `artifacts/evidence_ledger.csv` so verdicts do not live only in chat text.
- If a branch, lemma route, or proof attempt fails, mirror the failure reason into `artifacts/negative_result_ledger.md`.
- Keep `artifacts/run_state.json` aligned with the current proof phase, active checks, and next executable step.

### Template discipline
- Do not collapse tables into prose.
- If a block is not applicable, write `N/A` explicitly.
- If evidence is missing, write `UNKNOWN` explicitly.
- Use stable ids such as `A1`, `L1`, `D1`, `R1`, `C1`.
