---
id: S602
name: claim_evidence_reverse_outline_review
category: research_writing
triggers:
  - reverse outline
  - claim evidence
  - paper review
  - adversarial review
  - reviewer-facing
  - evidence alignment
  - 证据链
  - 审稿意见
  - 论文自审
  - 逻辑检查
---
# S602 Claim-Evidence Reverse Outline and Reviewer Audit

## Source integration
This skill integrates:
- `Research-Paper-Writing-Skills-main/research-paper-writing/references/paper-review.md`
- `Research-Paper-Writing-Skills-main/research-paper-writing/references/does-my-writing-flow-source.md`
- `Research-Paper-Writing-Skills-main/research-paper-writing/SKILL.md`
- relevant review/polish prompts from `awesome-ai-research-writing-main/README.md`

## Purpose
Use this skill for paper review, logical diagnosis, reviewer-style comments, or pre-submission self-audit. It must not degrade into vague language advice.

## Required ZYR routing
Primary companions:
- `S203_claim_evidence_matrix`
- `S226_logic_consistency_audit`
- `S229_paper_storyline_integrity_check`
- `S503_submission_readiness_gate`
- `S512_figure_table_audit`
- `S527_claim_language_risk_linter`

## Operating procedure
1. Segment the manuscript by section and paragraph.
2. Build a reverse outline: one function sentence per paragraph.
3. Extract claims and label each as empirical, theoretical, methodological, positioning, or limitation.
4. For every claim, attach evidence: table, figure, theorem, experiment, citation, or `UNKNOWN`.
5. Run reviewer-risk audit:
   - unsupported novelty
   - unclear contribution
   - method not tied to problem
   - experiment not tied to claim
   - missing baseline or unfair comparison
   - hidden assumption
   - overstated wording
   - figure/table not carrying a claim
6. Produce concrete change actions, preferably anchored to page/line/paragraph when the source supports it.

## Output schema
| ID | Location | Current claim/function | Evidence pointer | Risk | Required action | Priority |

## Completion rule
Never mark review complete if the manuscript, figures, references, or required comments were not accessible. Use `verification_incomplete` with the missing item list.
