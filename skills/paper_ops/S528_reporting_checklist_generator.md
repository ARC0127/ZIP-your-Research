---
id: S528
name: reporting_checklist_generator
category: paper_ops
triggers:
- reporting checklist
- Nature reporting summary
- PRISMA checklist
- reporting standards
- 透明度 清单
inputs_required:
- target_venue
- study_type
- manuscript_materials
outputs_required:
- checklist
- remediation_plan
- verification_record
quality_gates:
- no_fabrication
- mark_UNKNOWN
- audit_first
- copy_paste_ready
---

> **Global invariant (ZIP your Research):** Truthfulness • Trustworthiness • Deep logical reasoning. If required info is missing → mark **UNKNOWN** and ask minimal questions.

# S528 Reporting Checklist Generator (Venue-aware)

## Role
Generate a reporting checklist and a gap-remediation plan aligned with the target venue or guideline.

## Input
- Target venue/guideline (e.g., Nature reporting summary, PRISMA, internal)
- Manuscript sections available (or NONE)
- Study type (ML/RL/systematic review/other)

## Output Contract
1) Checklist items (grouped) with “Provided / Missing / N/A” columns.
2) Minimal remediation plan (what to add where).
3) Data/code availability statement template.
4) Verification record (UNKNOWN venue requirements).

## Rules
- If target is PRISMA, include PRISMA-style sections and flow diagram requirements.
