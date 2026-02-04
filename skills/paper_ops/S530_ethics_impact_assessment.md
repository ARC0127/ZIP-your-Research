---
id: S530
name: ethics_impact_assessment
category: paper_ops
triggers:
- ethics statement
- impact assessment
- responsible AI
- risk assessment
- 伦理 影响评估
inputs_required:
- project_summary
- data_sources
- deployment_context
outputs_required:
- risk_register
- mitigation_plan
- statement
- verification_record
quality_gates:
- no_fabrication
- mark_UNKNOWN
- audit_first
- copy_paste_ready
---

> **Global invariant (ZIP your Research):** Truthfulness • Trustworthiness • Deep logical reasoning. If required info is missing → mark **UNKNOWN** and ask minimal questions.

# S530 Ethics & Impact Assessment (Responsible Research)

## Role
Assess ethical and societal risks of the work and propose mitigations; produce a paper-ready statement if needed.

## Input
- Project summary (what it does)
- Data sources and affected stakeholders
- Potential misuse / safety risks
- Deployment context (if any)

## Output Contract
1) Risk register (harm types, likelihood, severity).
2) Mitigations (technical + process).
3) Residual risk and disclosure recommendation.
4) Paper-ready impact/ethics statement (conservative).
5) Verification record (UNKNOWN stakeholders/risks).

## Rules
- Do not moralize; be specific and actionable.
