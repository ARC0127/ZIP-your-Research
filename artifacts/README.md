# Artifacts (v1.5)

This directory defines the default artifact contract for ONECHAT and LOCKED execution.

## Authoritative v1.5 artifacts
- `evidence_ledger.csv`
  - authoritative claim-to-evidence mapping
  - columns: `claim_id,evidence_id,source_kind,source_ref,scope,status,confidence,notes`
- `source_archive_manifest.yaml`
  - authoritative source inventory and capture policy
  - required when literature/source collection is part of the task
- `proof_casebook.md`
  - authoritative proof/theorem/derivation audit artifact
  - required for theorem/proof-heavy tasks
- `negative_result_ledger.md`
  - authoritative record of rejected branches, failed hypotheses, and failed proofs
- `run_state.json`
  - authoritative current phase / current objective / open issues / next steps state

## Compatibility artifacts
- `acceptance_criteria.md`
- `audit_report.md`
- `runlog.jsonl`
- `claim_evidence_matrix.csv`
- `experiment_manifest.yaml`
- `draft.md`
- `risk_register.md`
- `repro_cmd.sh`

These remain valid, but for v1.5 workflows they are compatibility layers rather than the single source of truth.

## Minimum usage rules
- If an artifact is not applicable, keep it present and write `N/A` rather than silently omitting it.
- Failed directions must be recorded in `negative_result_ledger.md`; do not let them disappear into chat history.
- If a theorem/proof-heavy workflow is active, `proof_casebook.md` is the primary proof artifact, not freeform prose.
