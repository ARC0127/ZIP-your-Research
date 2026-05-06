---
id: S604
name: experiment_result_narrative_and_table_caption
category: research_writing
triggers:
  - results writing
  - experiment analysis
  - table caption
  - figure caption
  - ablation explanation
  - benchmark narrative
  - 实验分析
  - 结果分析
  - 表题
  - 图题
  - 消融实验
---
# S604 Experiment Result Narrative and Table/Figure Caption Writing

## Source integration
This skill integrates:
- `Research-Paper-Writing-Skills-main/research-paper-writing/references/experiments.md`
- caption and experiment-analysis prompts from `awesome-ai-research-writing-main/README.md`
- figure-caption alignment rules from `figures4papers-main/scientific-figure-making/`

## Purpose
Use this skill for Results/Experiments sections, table captions, figure captions, and ablation discussion.

## Required ZYR routing
Companion skills:
- `S303_evaluation_protocol_linter`
- `S304_baseline_selection_protocol`
- `S307_ablation_interpretation_framework`
- `S311_statistical_significance_sanity`
- `S322_visualization_plan_results`
- `S512_figure_table_audit`
- `S517_figure_table_caption_rewrite`

## Operating procedure
1. Identify the claim the result is supposed to support.
2. Identify metric direction, unit, dataset/task, baseline set, and seed/statistics status.
3. Decide whether the evidence supports superiority, tradeoff, stability, efficiency, or failure analysis.
4. Write conservative result narration: describe what the table/figure shows, why it matters, and what it does not prove.
5. For ablation, avoid saying a component is essential unless the ablation isolates it fairly.
6. For captions, make the figure independently interpretable but do not overload it with discussion.

## Output schema
- `RESULT_CLAIM`
- `EVIDENCE_FIELDS`
- `SUPPORTED_STATEMENTS`
- `UNSUPPORTED_OR_OVERSTATED_STATEMENTS`
- `REVISED_RESULT_TEXT`
- `CAPTION`
- `LIMITATION_NOTE`
