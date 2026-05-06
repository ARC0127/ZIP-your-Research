---
id: S621
name: publication_figure_design_theory
category: figure_design_integrated
version: v1.6.3
triggers:
- scientific figure
- publication figure
- figure design
- visualization design
- 论文图
- 科研绘图
- 图表设计
- 图形摘要
inputs_required:
- figure claim
- data fields or conceptual objects
- target medium and size constraints
- style constraints when provided
outputs_required:
- figure claim statement
- plot/layout decision
- style plan
- caption plan
- visual risk list
quality_gates:
- visual form follows the scientific claim
- axes/arrows/panels have explicit semantics
- layout is readable and non-overlapping
---

# S621 Publication Figure Design Theory

Use before drawing a scientific figure. The figure is part of the argument, not decoration.

Procedure: lock the visual claim; choose chart type by comparison structure; apply publication constraints; align every panel with caption and manuscript claim; redesign if the figure cannot support a precise claim. Consult `ext/src/figures/scientific-figure-making/` and all examples under `ext/figures`.

## Non-omission source rule

The complete source trees are preserved under `ext/src/`. This skill is a routing wrapper and logical reconstruction layer, not a replacement for the source files. For exact file-level coverage, inspect `manifests/src_manifest.json` and `manifests/src_FILE_integr_TABLE.md`.


## Physical-layout requirement

For architecture diagrams and scientific figures, the output must satisfy physical layout constraints before style decoration: aligned outer planes, consistent margins, non-overlapping arrows, readable text, explicit arrow semantics, and caption/figure claim consistency. If these fail, redraw rather than explain around the flaw.
