---
id: S601
name: paper_story_section_architecture
category: research_writing_integrated
version: v1.6.5
triggers:
- paper story
- manuscript architecture
- Introduction structure
- Method section
- Experiments section
- Conclusion section
- 论文结构
- 论文主线
- 引言重构
- 方法节重构
- 实验节写作
inputs_required:
- target paper section or manuscript excerpt
- task goal and target venue/reader when available
- locked facts, formulas, references, and evidence anchors
outputs_required:
- section diagnosis
- claim-evidence status
- reverse outline or revised section
- remaining risks or UNKNOWN items
quality_gates:
- problem-gap-method-evidence chain is explicit
- locked content is preserved unless explicitly revised
- S640 global language and logic gate is applied
---

# S601 Paper Story and Section Architecture

Use when writing, rewriting, or auditing research-paper sections. It combines ZYR writing discipline, `ext/src/rpws/paper_skill/SKILL.md`, the RPWS section guides, and S340.

Procedure: lock artifact type and frozen content; build problem→gap→method→evidence chain; select the exact RPWS reference file for the target section; apply S340 truthfulness/structure/language constraints; output the actual revised section or precise line-level revision.

## Non-omission source rule

The complete source trees are preserved under `ext/src/`. This skill is a routing wrapper and logical reconstruction layer, not a replacement for the source files. For exact file-level coverage, inspect `manifests/src_manifest.json` and `manifests/src_FILE_integr_TABLE.md`.


## Mandatory companion

For any visible prose rewrite or section design, apply `S640` first. S601 defines the section architecture; S640 enforces the global style, evidence, and forbidden-phrase requirements.
