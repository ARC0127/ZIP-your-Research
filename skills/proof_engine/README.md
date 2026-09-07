# proof_engine (suite v1.7.0)

A composite proof-audit engine for theorem verification, derivation checking, gap finding, and optional formal adaptation.

- Use when: theorem/proof-heavy input, long derivations, lemma dependency checks, proof repair after reviewer feedback.
- Default posture: natural-language verification first, `first-error-wins`, progressive refinement, majority vote diagnostic-only.
- Output posture: canonical blocks first, prose summary second. Prefer tables and ledgers over freeform narrative.
- Scientific assistant posture: first-principles, research-grade, honest about unknowns, Chinese by default.
- Formal tools are optional adapters; they never block the natural-language audit path.
- Primary artifact: theorem-/proof-heavy execution should materialize into `artifacts/proof_casebook.md`, with claim links recorded in `artifacts/evidence_ledger.csv`.
- Failure artifact: rejected proof routes and failed branches should be preserved in `artifacts/negative_result_ledger.md`.

Build:
```bash
python -B tools/zyr.py build
```

Outputs:
- `skills/proof_engine/MASTER_v1.5.md`
- Routing companion for `F_proof_idea` and `C_calculation`
