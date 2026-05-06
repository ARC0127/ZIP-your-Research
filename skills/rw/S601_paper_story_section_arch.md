---
id: S601
name: paper_story_section_architecture
category: research_writing
triggers:
  - paper story
  - paper structure
  - manuscript architecture
  - section architecture
  - introduction structure
  - abstract writing
  - method section
  - experiments section
  - 论文结构
  - 论文主线
  - 摘要
  - 引言
  - 方法节
  - 实验节
---
# S601 Paper Story and Section Architecture

## Source integration
This skill integrates the full retained source tree at:
- `ext/src/rpws/`
- `ext/src/awesome/`

Primary source anchors:
- `research-paper-writing/SKILL.md`
- `research-paper-writing/references/abstract.md`
- `research-paper-writing/references/introduction.md`
- `research-paper-writing/references/method.md`
- `research-paper-writing/references/experiments.md`
- `research-paper-writing/references/related-work.md`
- `research-paper-writing/references/conclusion.md`
- `research-paper-writing/references/examples/*.md`
- `awesome-ai-research-writing-main/README.md`

## Purpose
Use this skill when the task is to write, restructure, or diagnose a paper section. This is not a generic polishing skill. It must first lock the paper story, section function, claim-evidence relation, and reviewer-facing logic.

## Required ZYR routing
Use after the ZYR state machine has entered LOCKED execution. Route as:
1. `research_core/S214_thesis_statement_builder` or `S225_research_storyline_arc` if the paper story is not locked.
2. `research_core/S203_claim_evidence_matrix` if claims and evidence are not mapped.
3. `S601` for section architecture.
4. `paper_ops/S526_sentence_rewrite_with_retrieval` or `writing_engine/MASTER_v1.3.2.md` only after the architecture is stable.
5. `paper_ops/S503_submission_readiness_gate` for final readiness.

## Operating procedure
1. Identify the target section: Abstract, Introduction, Related Work, Method, Experiments, Results, Discussion, Conclusion, Appendix.
2. Identify the section-level rhetorical function.
3. Extract every major claim and attach an evidence pointer or mark `UNKNOWN`.
4. Build a reverse outline before rewriting.
5. Rewrite only after the section's purpose, order, and evidence coverage are stable.
6. Run adversarial reviewer review: novelty ambiguity, unsupported claim, baseline weakness, missing ablation, unclear technical advantage, limitation concealment.

## Section contracts
### Abstract
Must answer: task, unresolved challenge, contribution, why the contribution works, technical advantage, strongest experiment signal.

### Introduction
Must create a logically continuous path from task importance to unresolved technical barrier, then to method and evidence. Do not use vague contrast sentences unless the mechanism is spelled out.

### Related Work
Must position by problem and limitation, not by chronological listing. Each comparison should clarify what previous work can do, where it fails under the paper's setting, and what gap remains.

### Method
Must explain design, motivation, technical advantage, assumptions, and failure boundary. Avoid pure module listing.

### Experiments
Must answer: does the method outperform strong baselines, which component matters, when does it fail, and whether the evidence matches the claims.

### Conclusion
Must restate the solved problem, strongest evidence, bounded limitation, and concrete future direction without overclaiming.

## Output schema
- `SECTION_DIAGNOSIS`
- `CLAIM_EVIDENCE_STATUS`
- `REVERSE_OUTLINE`
- `STRUCTURAL_REWRITE_PLAN`
- `REVISED_TEXT` or `CHANGE_LIST`
- `REVIEWER_RISK_LEDGER`
- `COMPLETION_STATUS`
