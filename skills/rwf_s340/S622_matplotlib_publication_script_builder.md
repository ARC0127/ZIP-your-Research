---
id: S622
name: matplotlib_publication_script_builder
category: figure_design_integrated
version: v2.0
triggers:
  - matplotlib
  - plotting script
  - grouped bar
  - heatmap
  - radar chart
  - trend plot
  - svg png pdf
  - 绘图脚本
  - 画图代码
  - 输出svg
  - 输出png
---

# S622 Matplotlib Publication Script Builder

Use when executable plotting code or figure files are requested.

Procedure: select the closest source pattern from `ext/figures`; do not skip the script inventory; preserve deterministic data construction and explicit exports; prefer Matplotlib in generated code; validate by running/syntax-checking when possible. Every original figures4papers `.py` file is preserved and indexed in `manifests/SCRIPT_INVENTORY.md`.

## Non-omission source rule

The complete source trees are preserved under `ext/*`. This skill is a routing wrapper and logical reconstruction layer, not a replacement for the source files. For exact file-level coverage, inspect `manifests/src_manifest.json` and `manifests/src_FILE_integr_TABLE.md`.


## Executable-output requirement

When SVG/PNG/PDF files are requested, generate deterministic source code or native SVG whenever possible, export the requested assets, and visually inspect the rendered output when the environment allows. Do not substitute a raster image for an editable SVG unless the user explicitly accepts it.
