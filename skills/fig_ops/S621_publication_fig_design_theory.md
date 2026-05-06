---
id: S621
name: publication_figure_design_theory
category: figure_ops
triggers:
  - publication figure
  - paper figure
  - figure design
  - scientific figure
  - matplotlib figure
  - multi-panel figure
  - 论文图
  - 科研绘图
  - 图表设计
  - 画图
---
# S621 Publication Figure Design Theory

## Source integration
This skill integrates the full figures4papers source tree retained at:
- `ext/src/figures/`

Primary source anchors:
- `scientific-figure-making/SKILL.md`
- `scientific-figure-making/references/design-theory.md`
- `scientific-figure-making/references/common-patterns.md`
- `scientific-figure-making/references/api.md`
- `scientific-figure-making/references/tutorials.md`
- `scientific-figure-making/references/demos.md`
- all `figure_*` demo scripts and generated outputs

## Purpose
Use when a figure is intended for a paper, report, proposal, or slide where visual form must support a scientific claim.

## Required ZYR routing
1. `S203_claim_evidence_matrix`: identify the claim the figure must support.
2. `S322_visualization_plan_results`: decide plot family and evidence layout.
3. `S621`: apply publication figure design principles.
4. `S622`: generate or revise Matplotlib code.
5. `S512_figure_table_audit` and `S517_figure_table_caption_rewrite`: final verification.

## Design rules
- Start from the claim, not from a preferred chart type.
- Use minimal visual complexity compatible with the claim.
- Use consistent typography, axis weight, tick density, margins, and legend placement.
- Prefer vector outputs for line art and high-DPI raster outputs for image-heavy figures.
- Ensure color meaning is semantic and remains interpretable in grayscale when possible.
- Avoid 3D, radar, heatmap, or dense multi-panel designs unless they are genuinely the best carrier for the claim.
- Captions must state what is compared, the metric/unit, and the interpretation boundary.

## Figure-type routing
- Grouped bar: method comparison, ablation, multiple metrics.
- Trend/line: time, training, scaling, sensitivity.
- Heatmap: two-axis interaction or matrix-like composition.
- Scatter/manifold: geometric relation or distribution structure.
- Radar: qualitative profile only; avoid precise numeric claims.
- Multi-panel: when separate subclaims must be compared under a single narrative.

## Output schema
- `FIGURE_CLAIM`
- `DATA_FIELDS_REQUIRED`
- `PLOT_TYPE_DECISION`
- `LAYOUT_PLAN`
- `STYLE_PLAN`
- `CAPTION_PLAN`
- `RISKS`
