---
id: S604
name: experiment_result_narrative_and_caption
category: research_writing_integrated
version: v2.0
triggers:
  - experiment analysis
  - result narrative
  - table caption
  - figure caption
  - ablation description
  - 实验分析
  - 结果描述
  - 图题
  - 表题
  - 消融实验
---

# S604 Experiment Result Narrative and Caption

Use to write or audit result paragraphs, table captions, figure captions, and ablation narratives.

Procedure: identify the exact claim; read values as given; separate main result/ablation/robustness/cost/failure evidence; check metric direction and protocol; caption must state comparison, setting, metric, and visually supported conclusion.

## Non-omission source rule

The complete source trees are preserved under `ext/*`. This skill is a routing wrapper and logical reconstruction layer, not a replacement for the source files. For exact file-level coverage, inspect `manifests/src_manifest.json` and `manifests/src_FILE_integr_TABLE.md`.


## Mandatory companion

For result narratives and captions, apply `S640` first. If the task involves a figure or table, also apply `S623` to verify that the visual evidence, caption, and manuscript claim match.
