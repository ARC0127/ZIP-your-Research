---
id: S236
name: preregistration_builder
category: research_core
triggers:
- preregistration
- pre-registration
- OSF registration
- 预注册
- analysis plan prereg
inputs_required:
- research_question
- hypotheses_or_claims
- outcomes_metrics
- data_or_env
- constraints
outputs_required:
- prereg_draft
- decision_rules
- verification_record
quality_gates:
- no_fabrication
- mark_UNKNOWN
- audit_first
- copy_paste_ready
---

> **Global invariant (ZIP your Research):** Truthfulness • Trustworthiness • Deep logical reasoning. If required info is missing → mark **UNKNOWN** and ask minimal questions.

# S236 Preregistration Builder (OSF-ready)

## Role
Convert a research idea into a preregistration draft that cleanly separates:
- confirmatory hypotheses
- exploratory analyses
- decision rules

## Input
- Research question + hypothesis (or claim map)
- Primary outcomes/metrics
- Data sources / simulation environment
- Constraints (time/compute) and exclusions

## Output Contract
1) **Hypotheses** (H1..Hk) each with measurable operationalization.
2) **Design**: data, sampling/episodes, inclusion/exclusion, randomization/seeds.
3) **Analysis plan**: statistical tests or evaluation protocol; multiple comparisons (if applicable).
4) **Decision rules**: stop criteria; acceptance/rejection thresholds; what counts as support.
5) **Exploratory section** explicitly labeled.
6) **Verification record**: UNKNOWN items + exact steps to verify.

## Rules
- Do not assert novelty; keep prereg factual.
- If a metric is undefined, mark UNKNOWN and propose a definition.

## Template output (ready to paste)
Provide headings compatible with common OSF prereg forms.
