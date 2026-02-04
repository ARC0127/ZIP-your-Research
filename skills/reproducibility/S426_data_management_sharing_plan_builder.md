---
id: S426
name: data_management_sharing_plan_builder
category: reproducibility
triggers:
- data management plan
- DMS plan
- sharing plan
- 数据管理与共享计划
- NIH DMS
inputs_required:
- data_types
- sensitivity_flags
- sharing_intent
- timeline
outputs_required:
- dms_plan
- data_dictionary_template
- verification_record
quality_gates:
- no_fabrication
- mark_UNKNOWN
- audit_first
- copy_paste_ready
---

> **Global invariant (ZIP your Research):** Truthfulness • Trustworthiness • Deep logical reasoning. If required info is missing → mark **UNKNOWN** and ask minimal questions.

# S426 Data Management & Sharing Plan Builder (DMS)

## Role
Draft a Data Management & Sharing Plan that covers data types, standards, storage, access, and sharing constraints.

## Input
- Data types produced (datasets/logs/code/models)
- Sensitivity flags (human subjects, proprietary, security)
- Intended repositories or sharing channels (if known)
- Timeline (when to share)

## Output Contract
1) Data types + formats + estimated volume.
2) Metadata/data dictionary plan.
3) Storage/backup plan + access control.
4) Sharing plan: what, when, where, how.
5) Preservation plan (long-term).
6) Compliance notes + verification record (UNKNOWN legal/ethical constraints).

## Rules
- If sensitivity is unknown, mark UNKNOWN and list what to check.
