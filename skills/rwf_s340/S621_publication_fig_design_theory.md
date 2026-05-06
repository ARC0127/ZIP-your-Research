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
- workflow diagram
- architecture diagram
- 流程图
inputs_required:
- figure claim
- data fields or conceptual objects
- target medium and size constraints
- style constraints when provided
outputs_required:
- figure claim statement
- closest reusable figures4papers source pattern
- plot/layout decision
- style plan
- caption plan
- visual risk list
quality_gates:
- visual form follows the scientific claim
- figures4papers is inspected before proposing a new implementation
- source-code or source-file generation path is explicit
- axes/arrows/panels have explicit semantics
- layout is readable, aligned, and non-overlapping
---

# S621 Publication Figure Design Theory

Use before drawing a scientific figure. The figure is part of the argument, not decoration.

Procedure: lock the visual claim; identify whether the object is data, mechanism, workflow, architecture, or caption evidence; inspect `ext/src/figures/` and select the closest existing figures4papers pattern; choose the visual form by comparison structure and target medium; then apply publication constraints. Align every panel with the caption and manuscript claim. Redesign if the figure cannot support a precise claim. Consult `ext/src/figures/fig_skill/SKILL.md`, `ext/src/figures/fig_skill/ref/design_theory.md`, `ext/src/figures/fig_skill/ref/common_patterns.md`, and the example scripts under `ext/src/figures/figure_*/`.

## Non-omission source rule

The complete source trees are preserved under `ext/src/`. This skill is a routing wrapper and logical reconstruction layer, not a replacement for the source files. For exact file-level coverage, inspect `manifests/src_manifest.json` and `manifests/src_FILE_integr_TABLE.md`.

## Figures4papers-first rule

Do not start from a blank figure if a close figures4papers source pattern already exists. Prefer minimal adaptation of an upstream plotting layout, panel structure, legend style, or export workflow.

Preserve the existing data-input logic whenever practical:
- if the selected upstream pattern reads CSV, table, dataframe, or another structured source, keep that pattern unless the user explicitly changes the data source;
- do not replace structured input with ad hoc hard-coded arrays merely for convenience;
- do not fabricate values for visual balance.

## Format rule

Treat SVG, PNG, and PDF as output formats, not as a substitute for source generation. The generating script or structured source should remain available whenever possible. If the requested format is unsuitable for the target medium or the figure claim, state the limitation and provide the closest safe export.

## Physical-layout requirement

For architecture diagrams and scientific figures, the output must satisfy physical layout constraints before style decoration: aligned outer planes, consistent margins, non-overlapping arrows, readable text, explicit arrow semantics, and caption/figure claim consistency. If these fail, redraw or change the source implementation rather than explain around the flaw.
