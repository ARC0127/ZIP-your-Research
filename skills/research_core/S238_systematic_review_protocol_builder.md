---
id: S238
name: systematic_review_protocol_builder
category: research_core
triggers:
- systematic review
- PRISMA
- meta-analysis protocol
- 系统综述
- PRISMA protocol
inputs_required:
- review_question
- scope
- constraints
outputs_required:
- protocol_draft
- screening_rubric
- extraction_schema
- verification_record
quality_gates:
- no_fabrication
- mark_UNKNOWN
- audit_first
- copy_paste_ready
---

> **Global invariant (ZIP your Research):** Truthfulness • Trustworthiness • Deep logical reasoning. If required info is missing → mark **UNKNOWN** and ask minimal questions.

# S238 Systematic Review Protocol Builder (PRISMA-aligned)

## Role
Produce a reproducible protocol for a systematic review: search → screen → extract → synthesize.

## Input
- Review question (PICO-style optional)
- Scope boundaries (years, venues, domains)
- Inclusion/exclusion criteria (if any)
- Constraints (time, team size)

## Output Contract
1) Search strategy (databases/venues + query families + inclusion window).
2) Screening workflow (title/abstract/full-text) with decision rubric.
3) Data extraction schema (fields + coding guide).
4) Synthesis plan (narrative themes + evidence grading).
5) Flow diagram plan (what counts as identified/removed/included).
6) Verification record (what is assumed vs known).

## Rules
- If databases are unavailable, output a plan and mark retrieval results UNKNOWN.
