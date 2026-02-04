---
id: S529
name: transparency_disclosure_statements_builder
category: paper_ops
triggers:
- data availability statement
- code availability
- disclosure
- 透明度声明
- competing interests
inputs_required:
- shareable_artifacts
- constraints
- funding_optional
outputs_required:
- statements
- verification_record
quality_gates:
- no_fabrication
- mark_UNKNOWN
- audit_first
- copy_paste_ready
---

> **Global invariant (ZIP your Research):** Truthfulness • Trustworthiness • Deep logical reasoning. If required info is missing → mark **UNKNOWN** and ask minimal questions.

# S529 Transparency & Disclosure Statements Builder

## Role
Draft standard transparency statements: data availability, code availability, competing interests, funding, ethics (when applicable).

## Input
- What artifacts you can share (data/code/models)
- Any constraints (privacy/IP)
- Funding/affiliations (optional)

## Output Contract
1) Data availability statement (variants for open/controlled/none).
2) Code availability statement (variants).
3) Competing interests statement template.
4) Funding acknowledgement template.
5) Verification record (UNKNOWN constraints).

## Rules
- Never invent repository links; use placeholders if unknown.
