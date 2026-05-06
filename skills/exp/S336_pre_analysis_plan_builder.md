---
id: S336
name: pre_analysis_plan_builder
category: experiments
triggers:
- pre-analysis plan
- analysis plan
- 统计分析计划
- decision rule plan
inputs_required:
- hypotheses
- data_structure
- metrics
- comparisons
outputs_required:
- analysis_plan
- decision_rules
- verification_record
quality_gates:
- no_fabrication
- mark_UNKNOWN
- audit_first
- copy_paste_ready
---

> **Global invariant (ZIP your Research):** Truthfulness • Trustworthiness • Deep logical reasoning. If required info is missing → mark **UNKNOWN** and ask minimal questions.

# S336 Pre-analysis Plan Builder (Statistics & Decision Rules)

## Role
Turn hypotheses into a concrete analysis plan with explicit decision rules.

## Input
- Hypotheses (H1..Hk)
- Data structure (obs units, episodes, seeds)
- Planned comparisons / baselines
- Metrics and aggregation rules

## Output Contract
1) Model/tests to run (or evaluation protocol for ML/RL).
2) Primary vs secondary endpoints.
3) Multiple comparisons strategy (if relevant).
4) Robustness checks (sensitivity analyses).
5) Reporting plan: effect sizes/CI, plots, tables.
6) Verification record (UNKNOWN statistics or assumptions).

## Rules
- If significance testing is inappropriate, propose alternative reporting (CI/effect sizes).
