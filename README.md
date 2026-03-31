# ZIP-your-Research (ZYR) v1.5.0-wip

**Status:** alignment work-in-progress  
**Workspace lineage:** `zyr_v1.5.0_alignment_wip_20260330`  
**Base release:** `v1.4.4_release_20260222`  
**License:** MIT

ZIP-your-Research is a chat-first research workflow pack for GPT/Codex-style assistants. Its goal is not to turn the model into an unattended auto-research runtime. Its goal is to make high-rigor research work more stable, more auditable, and harder to derail.

Compared with `v1.4.4`, the current `v1.5` workline adds a stronger execution posture:

- `lock-first`: pre-lock and locked execution remain strictly separated.
- `completion-first`: the assistant must not silently simplify, silently decompose, or silently under-deliver a lawful in-scope request.
- `scientific-discipline-first`: default Chinese output, first-principles analysis, explicit fact/inference split, strict honesty boundary.
- `artifact-first`: important state should live in explicit artifacts rather than disappearing into chat history.
- `proof-aware`: theorem/proof-heavy tasks activate a dedicated `proof_engine` with pessimistic and progressive verification.

## What ZYR is

ZYR is a modular protocol pack with five layers:

1. `boot/`
   Handles bootstrap, migration detection, intake, `MODE_LOCK`, pre-lock rollback, and locked execution rules.
2. `router/`
   Maps user requests into the A-J focus taxonomy and chooses primary/secondary execution paths.
3. `skills/`
   Contains atomic and composite skills for research, experiments, reproducibility, writing, coding, and proof work.
4. `artifacts/`
   Defines the authoritative durable outputs that preserve state, evidence, proof audit traces, and failures.
5. `tools/`
   Builds composite prompts and runs deterministic validators/regressions.

## What ZYR is not

- It is not a full autonomous research agent runtime.
- It does not assume multi-agent decomposition by default.
- It does not treat "plan only" as an acceptable replacement for completing a lawful in-scope request.
- It does not allow proof verdicts, novelty claims, or experiment status to remain only in transient chat text.

## v1.5 highlights

### 1. Stronger locked execution

`v1.5` adds a stricter post-lock behavior layer:

- `deliver_full_requested_scope=true`
- `silent_simplification=forbid`
- `silent_decomposition=forbid`
- `partial_completion_labeling=required`
- `discover_before_asking=true`

See:

- `boot/04_MODE_LOCK_FORMAT_v1.3.2.md`
- `boot/11_COMPLETION_FIRST_ANTI_SHORTCUT_v1.5.md`
- `boot/13_SCIENTIFIC_ASSISTANT_OUTPUT_DISCIPLINE_v1.5.md`

### 2. Proof and theorem verification path

`v1.5` introduces `skills/proof_engine/` to strengthen theoretical derivation and mathematical proof work.

Core mechanisms:

- `first_error_wins`
- `parallel pessimistic review`
- `progressive multiscale verification`
- `majority_vote=diagnostic_only`
- `reviewer-feedback refinement loop`
- `formal_adapter=optional`

Key files:

- `skills/proof_engine/README.md`
- `skills/proof_engine/MASTER_v1.5.md`
- `skills/research_core/S237_theorem_assumption_normalizer.md`
- `skills/research_core/S240_pessimistic_proof_verification.md`
- `skills/research_core/S241_progressive_proof_verification.md`
- `skills/reproducibility/S433_formal_proof_adapter.md`

### 3. Durable artifact substrate

`v1.5` upgrades the artifact layer so state, evidence, proofs, and failed branches can survive chat boundaries.

Authoritative artifacts:

- `artifacts/evidence_ledger.csv`
- `artifacts/source_archive_manifest.yaml`
- `artifacts/proof_casebook.md`
- `artifacts/negative_result_ledger.md`
- `artifacts/run_state.json`

Compatibility artifacts such as `audit_report.md`, `runlog.jsonl`, and `claim_evidence_matrix.csv` remain usable, but they are no longer treated as the only source of truth.

See `artifacts/README.md`.

### 4. Loss-minimizing migration

`v1.5` replaces lightweight resume notes with a stronger migration contract. Migration prompts are expected to preserve:

- current objective and deliverable
- current `MODE_LOCK`
- proof profile if active
- important paths and artifacts
- completed checks and actual outcomes
- open blockers and next executable step

See:

- `boot/01_MIGRATION_PROMPT_TEMPLATE_v1.5.md`
- `boot/02_MIGRATION_DETECTOR_v1.3.2.md`
- `docs/QUICKSTART.md`

### 5. Regression coverage beyond prompt text

`v1.5` extends deterministic regression beyond basic locked behavior:

- locked regression: `tests/corpus_v1_3.jsonl`
- completion compliance: `tests/compliance_v1_5/`
- proof verification: `tests/proof_verification_v1_5/`
- scientific discipline: `tests/scientific_discipline_v1_5/`

This is an explicit design choice: important protocol claims should be backed by validators and reports, not only by prose documentation.

## Quick start

### Option A: ZIP-only boot

1. Upload the repository zip to a fresh chat.
2. If resuming previous work, paste a `MIGRATION PROMPT (v1.5)` in English.
3. Otherwise say `start`.
4. Complete intake.
5. Read the generated `MODE_LOCK`.
6. Reply `CONFIRM`.

After `CONFIRM`, the assistant enters locked execution.

Reference:

- `boot/00_BOOTSTRAP_PROTOCOL_v1.3.2.md`
- `boot/07_FIRST_TURN_APPLICATION_GUIDE_v1.3.2.md`
- `docs/QUICKSTART.md`

### Option B: Use one engine directly

If you do not want the full lock flow, you can also paste a composite engine or atomic skill directly into a chat.

Recommended entry points:

- writing tasks: `skills/writing_engine/MASTER_v1.3.2.md`
- coding tasks: `skills/coding_engine/MASTER_v1.3.2.md`
- theorem/proof tasks: `skills/proof_engine/MASTER_v1.5.md`

## Default posture

Unless the user overrides it during intake:

- default language: Chinese
- analysis basis: first principles
- fact/inference separation: required for nontrivial tasks
- honesty boundary: strict
- citation mode: conservative
- web browsing policy: allow after lock
- debug trace: off
- completion posture: full requested scope by default

## Proof-heavy workflow

For theorem/proof-heavy work, `v1.5` expects proof outputs to become durable artifacts.

At minimum:

- theorem normalization
- assumption table
- lemma dependency graph
- derivation ledger when applicable
- review matrix or chunk verdict matrix
- verification record

These are the authoritative sections of `artifacts/proof_casebook.md`.

In addition:

- theorem/proof claims should be mapped into `artifacts/evidence_ledger.csv`
- failed proof attempts or rejected branches should be preserved in `artifacts/negative_result_ledger.md`

This prevents the common failure mode where a conversation contains a verdict but the proof trace and failure anchors are lost.

## Repository layout

### Core protocol

- `boot/`
- `router/`
- `skills_manifest.yaml`
- `INDEX.md`

### Skill families

- `skills/research_core/`
- `skills/experiments/`
- `skills/reproducibility/`
- `skills/paper_ops/`
- `skills/writing_engine/`
- `skills/coding_engine/`
- `skills/proof_engine/`

### Durable state and outputs

- `artifacts/`

### Research and alignment notes

- `research/`

### Tooling and validation

- `tools/`
- `tests/`

### Supporting documentation

- `docs/`
- `templates/`
- `interfaces/`

## Build and validate

Typical local workflow:

```bash
python3 tools/build_all.py
python3 tools/validate_v7_2.py
python3 tools/drift_audit_v1_3.py
python3 tools/validate_corpus_v1_3.py
python3 tools/simulate_locked_regression_v1_3.py --n 25 --seed 0
python3 tools/validate_completion_corpus_v1_5.py
python3 tools/simulate_completion_compliance_v1_5.py
python3 tools/validate_scientific_discipline_corpus_v1_5.py
python3 tools/simulate_scientific_discipline_v1_5.py
python3 tools/validate_proof_verification_corpus_v1_5.py
python3 tools/simulate_proof_verification_v1_5.py
```

Generated reports land under:

- `artifacts/locked_regression/`
- `artifacts/completion_compliance/`
- `artifacts/scientific_discipline/`
- `artifacts/proof_verification/`

## Design references

The current `v1.5` alignment work is informed by recent agentic/deep-research systems and proof-verification work, but it deliberately keeps a conservative scope.

Broadly:

- adopt: artifact-first collaboration, explicit control plane, verification-before-synthesis
- adapt: structured proof verification, refinement loops, optional formal adapters
- reject: unattended research factory posture, silent scope mutation, default multi-agent decomposition

Research notes live under `research/`.

## Safety and honesty

ZYR treats the following as non-negotiable:

- do not fabricate facts, file states, execution status, or citations
- do not present unexecuted checks as completed
- do not hide uncertainty behind vague prose
- do not downgrade research questions into unsupported heuristic tuning
- do not let locked tasks drift without explicit user approval

See:

- `docs/LEGAL.md`
- `docs/SECURITY_PROMPT_INJECTION.md`
- `boot/13_SCIENTIFIC_ASSISTANT_OUTPUT_DISCIPLINE_v1.5.md`

## Maintainer

See `docs/ABOUT_MAINTAINER.md`.

## License

MIT. See `LICENSE`.
