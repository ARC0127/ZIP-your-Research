## Proof Engine: Operating Rules

> **Normative rules:** `boot/04_MODE_LOCK_FORMAT_v1.3.2.md` + `boot/11_COMPLETION_FIRST_ANTI_SHORTCUT_v1.5.md` + `boot/13_SCIENTIFIC_ASSISTANT_OUTPUT_DISCIPLINE_v1.5.md` + `skills/research_core/S240_pessimistic_proof_verification.md` + `skills/research_core/S241_progressive_proof_verification.md`.

This engine is for theorem verification and derivation-heavy work.

- Default mode is **natural-language verification first**.
- Use `first-error-wins`: a single fatal flaw is sufficient to reject a proof.
- Treat majority vote as diagnostic only; it cannot override the primary verdict.
- Keep `proof plan`, `repair idea`, and `verified proof` strictly separated.
- Emit canonical blocks before commentary. Do not lead with prose if a ledger, table, or matrix is required.
