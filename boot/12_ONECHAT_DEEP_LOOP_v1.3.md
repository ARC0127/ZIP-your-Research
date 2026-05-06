# ONECHAT Deep Extended Thinking Loop (v1.5 semantics on v1.3 path)

**Purpose:** In a single ChatGPT conversation (no external agent framework), emulate an agentic research workflow with strict phase gating.

This protocol is inspired by public descriptions of multi-agent research pipelines (e.g., FARS: Ideation/Planning/Experiment/Writing) and adapts them to one chat by enforcing:
- phase gates,
- artifact contracts,
- per-turn lock loop,
- review/audit checkpoints.

## Enable
During intake or after MODE_LOCK, set:
```yaml
SESSION_OVERRIDES:
  onechat_loop: v1.3
  onechat_phases: [Ideation, Planning, Experiment, Writing, Review, Ops]
```

## Phase contracts (minimal)
### Ideation
Outputs: `artifacts/idea.md`, `artifacts/question.md`, `artifacts/related_keywords.md`, `artifacts/src_arch_manifest.yaml`, `artifacts/evidence_ledger.csv`

### Planning
Outputs: `artifacts/plan.md`, `artifacts/experiment_manifest.yaml`, `artifacts/acceptance_criteria.md`, `artifacts/run_state.json`

### Experiment
Outputs: `artifacts/patch.diff` or `artifacts/changed_files.md`, `artifacts/repro_cmd.sh`, `artifacts/runlog.jsonl`, `artifacts/run_state.json`

### Writing
Outputs: `artifacts/draft.md`, `artifacts/claim_evidence_matrix.csv`, `artifacts/evidence_ledger.csv`

### Review
Outputs: `artifacts/audit_report.md`, `artifacts/risk_register.md`, `artifacts/run_state.json`, `artifacts/negative_result_ledger.md`

### Ops
Outputs: `artifacts/release_checklist.md`, `artifacts/next_steps.md`, `artifacts/run_state.json`

### Proof-heavy addendum
- If the task is theorem/proof-heavy, `artifacts/proof_casebook.md` becomes a required artifact.
- If a proof, hypothesis, or branch is rejected, record it in `artifacts/negative_result_ledger.md`.
- `artifacts/evidence_ledger.csv` should map theorem/proof claims to the corresponding proof artifact sections.

## Per-turn rule
In LOCKED execution: always run `boot/11_req_LOCK_LOOP_v1.3.md`, and refuse out-of-phase requests unless explicitly accepted by MODE_LOCK.

## When user perturbs the topic
- classify as OUT_OF_SCOPE → refuse → re-anchor → offer CHANGE_REQUEST.
