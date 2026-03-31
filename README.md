# ZIP-your-Research (ZYR) v1.5.0

**A chat-first, artifact-first research workflow pack for GPT/Codex-style assistants.**

**Status:** formal release  
**Base line:** `v1.4.4_release_20260222`  
**Current repo version:** `v1.5.0`  
**License:** MIT

ZYR is designed for one specific goal: make serious research work in LLM chats more stable, more auditable, and less likely to drift into shallow summaries, silent simplification, or fake completion.

It is not an unattended auto-research runtime. It is a protocol pack that helps an assistant behave like a disciplined research operator.

## Why this repo exists

Modern frontier models are powerful, but they also fail in predictable ways:

- they simplify a task without permission
- they split work into smaller tasks and stop too early
- they hide uncertainty behind fluent prose
- they turn proof-heavy or theory-heavy work into hand-wavy discussion
- they let important evidence disappear into chat history

ZYR exists to counter those failure modes with explicit contracts, routing, artifacts, and deterministic regressions.

## What changed in v1.5

Compared with `v1.4.4`, the current `v1.5` line adds five major upgrades:

1. `completion-first`
   Locked execution now explicitly forbids silent simplification, silent decomposition, and partial-completion masquerading.
2. `scientific-discipline-first`
   Default Chinese output, first-principles analysis, explicit fact/inference separation, strict honesty boundary.
3. `proof-aware`
   Theorem/proof/derivation-heavy tasks route into `proof_engine` with pessimistic and progressive verification.
4. `artifact-first`
   State, evidence, proof traces, and rejected branches live in durable artifacts instead of disappearing into chat text.
5. `loss-minimizing migration`
   Cross-chat continuation now expects a structured migration prompt rather than a light summary.

## Core principles

- `lock-first`
  Pre-lock and locked execution are strictly separated.
- `deliverable-first`
  Once locked, lawful in-scope requests should be completed, not downgraded into advice-only output.
- `truth-first`
  Unknowns must stay unknown; unrun checks must not be reported as completed.
- `artifact-first`
  Important reasoning state should exist in files, not only in messages.
- `first-principles-first`
  Research problems should not be reduced to unsupported heuristic tuning.

## Quick start

### Option A: ZIP-only boot

1. Upload the repository zip to a fresh chat.
2. If resuming work, paste a `MIGRATION PROMPT (v1.5)` in English.
3. Otherwise send `start`.
4. Complete intake.
5. Review the generated `MODE_LOCK`.
6. Reply `CONFIRM`.

After `CONFIRM`, the assistant enters locked execution.

Key entry points:

- `boot/00_BOOTSTRAP_PROTOCOL_v1.3.2.md`
- `boot/04_MODE_LOCK_FORMAT_v1.3.2.md`
- `docs/QUICKSTART.md`

### Option B: direct engine use

If you want a narrower workflow, paste one composite engine directly into a chat:

- writing: `skills/writing_engine/MASTER_v1.3.2.md`
- coding: `skills/coding_engine/MASTER_v1.3.2.md`
- proof/theory: `skills/proof_engine/MASTER_v1.5.md`

## Main execution layers

### `boot/`

Bootstrap, migration detection, intake, `MODE_LOCK`, pre-lock rollback, locked execution rules.

### `router/`

Deterministic routing from user request to the A-J focus taxonomy and companion skills.

### `skills/`

Atomic and composite execution modules:

- `research_core/`
- `experiments/`
- `reproducibility/`
- `paper_ops/`
- `writing_engine/`
- `coding_engine/`
- `proof_engine/`
- `platform_zyr_skills/`

### `artifacts/`

Durable outputs and execution state.

Authoritative v1.5 artifacts:

- `artifacts/evidence_ledger.csv`
- `artifacts/source_archive_manifest.yaml`
- `artifacts/proof_casebook.md`
- `artifacts/negative_result_ledger.md`
- `artifacts/run_state.json`

### `tools/`

Composite builders, validators, audits, and deterministic simulators.

## Proof and theory workflow

`v1.5` introduces a dedicated proof route for theorem-heavy and derivation-heavy tasks.

Core behaviors:

- `first_error_wins`
- `parallel pessimistic review`
- `progressive multiscale verification`
- `majority_vote=diagnostic_only`
- `repair-then-reverify`
- `formal_adapter=optional`

Expected durable proof outputs:

- theorem normalization
- assumption table
- lemma dependency graph
- derivation ledger
- review matrix or chunk verdict matrix
- verification record

These live in `artifacts/proof_casebook.md`, with claim links tracked in `artifacts/evidence_ledger.csv`.

## Migration and continuity

`v1.5` treats migration as a structured handoff, not a reminder note.

A good migration prompt should preserve:

- current objective and deliverable
- current `MODE_LOCK`
- proof profile if active
- important files and paths
- completed checks and actual outcomes
- artifact inventory
- blockers, risks, and next executable step

See:

- `boot/01_MIGRATION_PROMPT_TEMPLATE_v1.5.md`
- `boot/02_MIGRATION_DETECTOR_v1.3.2.md`

## Validation

Typical local validation flow:

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
python3 tools/system_audit_v1_3.py
```

Reports are written under:

- `artifacts/locked_regression/`
- `artifacts/completion_compliance/`
- `artifacts/scientific_discipline/`
- `artifacts/proof_verification/`
- `artifacts/system_audit/`

## Platform module

`skills/platform_zyr_skills/` is the repo-native rewrite of the runtime skill pack used for document, PDF, and spreadsheet delivery workflows.

It keeps:

- portable templates
- normalized source snapshots
- QA loops
- maintenance diff instructions

It does not vendor private runtime code.

## Safety and honesty

ZYR treats the following as non-negotiable:

- do not fabricate facts, citations, file states, or execution status
- do not present unexecuted checks as completed
- do not hide uncertainty inside vague prose
- do not downgrade research questions into unsupported tuning guesses
- do not drift locked work without explicit user approval

Key files:

- `boot/11_COMPLETION_FIRST_ANTI_SHORTCUT_v1.5.md`
- `boot/13_SCIENTIFIC_ASSISTANT_OUTPUT_DISCIPLINE_v1.5.md`
- `docs/SECURITY_PROMPT_INJECTION.md`
- `docs/LEGAL.md`

## Repository map

- `README.md`
- `CHANGELOG.md`
- `INDEX.md`
- `skills_manifest.yaml`
- `docs/`
- `research/`
- `interfaces/`
- `templates/`

## Acknowledgments and references

ZYR is open work. Many of its engineering decisions were shaped by public research systems, proof-verification papers, and open learning materials. These works informed the design; they are not claimed here as original ZYR inventions.

Architecture and control-plane references include [Google AI co-scientist](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/), [OpenAI deep research](https://openai.com/index/introducing-deep-research/), [A Vision for Auto Research with LLM Agents](https://arxiv.org/abs/2504.18765), [PiFlow](https://arxiv.org/abs/2505.15047), [AI-Researcher](https://arxiv.org/abs/2505.18705), [ResearStudio](https://arxiv.org/abs/2510.12194), [FS-Researcher](https://arxiv.org/abs/2602.01566), [OR-Agent](https://arxiv.org/abs/2602.13769), [EvoScientist](https://arxiv.org/abs/2603.08127), [ResearchPilot](https://arxiv.org/abs/2603.14629), [AI-Supervisor](https://arxiv.org/abs/2603.24402), and the public-description source for [FARS](https://www.thepaper.cn/newsDetail_forward_32600597).

Proof and theory references include [Pessimistic Verification for Open-Ended Math Questions](https://arxiv.org/abs/2511.21522), [Hard2Verify](https://arxiv.org/abs/2510.13744), [Scaling Flaws of Verifier-Guided Search in Mathematical Reasoning](https://arxiv.org/abs/2502.00271), [Improving Value-based Process Verifier via Low-Cost Variance Reduction](https://arxiv.org/abs/2508.10539), [Asking LLMs to Verify First is Almost Free Lunch](https://arxiv.org/abs/2511.21734), [AI Mathematician](https://arxiv.org/abs/2505.22451), [StepProof](https://arxiv.org/abs/2506.10558), [Goedel-Prover](https://arxiv.org/abs/2502.07640), [Goedel-Prover-V2](https://arxiv.org/abs/2508.03613), [Leanabell-Prover-V2](https://arxiv.org/abs/2507.08649), and [APOLLO](https://arxiv.org/abs/2505.05758).

Open learning and community references include [Hello-Agents (Datawhale)](https://github.com/datawhalechina/hello-agent).

For the full grouped attribution record, source-type notes, and per-reference translation targets, see:

- `docs/ATTRIBUTION.md`
- `research/auto_research_inventory.md`
- `research/engineering_alignment_matrix.md`
- `research/fars_deep_dive.md`
- `research/pessimistic_verification_lineage.md`

## Maintainer

See `docs/ABOUT_MAINTAINER.md`.
