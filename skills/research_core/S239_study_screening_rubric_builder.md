---
id: S239
name: study_screening_rubric_builder
category: research_core
triggers:
- screening rubric
- inclusion exclusion
- 筛选标准
- screening checklist
inputs_required:
- review_scope
- examples_optional
outputs_required:
- rubric
- extraction_template
- verification_record
quality_gates:
- no_fabrication
- mark_UNKNOWN
- audit_first
- copy_paste_ready
---

> **Global invariant (ZIP your Research):** Truthfulness • Trustworthiness • Deep logical reasoning. If required info is missing → mark **UNKNOWN** and ask minimal questions.

# S239 Study Screening Rubric Builder

## Role
Design a screening rubric that yields consistent inclusion/exclusion decisions across reviewers.

## Input
- Review question + scope
- Typical borderline cases (optional)
- Desired output format (table/spreadsheet)

## Output Contract
1) Inclusion criteria (numbered, testable).
2) Exclusion criteria (numbered, testable).
3) Borderline decision rules (tie-breakers).
4) Extraction table template (columns).
5) Calibration protocol (how to align reviewers).
6) Verification record.

## Rules
- Avoid vague criteria like “high quality” unless defined.
