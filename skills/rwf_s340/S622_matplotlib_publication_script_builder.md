---
id: S622
name: matplotlib_publication_script_builder
category: figure_design_integrated
version: v1.6.3
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
- workflow diagram
- architecture diagram
- 流程图
inputs_required:
- data or deterministic data-construction plan
- desired figure type and export formats
- target output path and size/DPI constraints when available
outputs_required:
- executable plotting script or another source-native artifact selected after inspecting figures4papers
- exported figure files when execution is possible
- run/inspection notes and any format-fallback rationale
quality_gates:
- script or source artifact is minimal and reproducible
- figures4papers is inspected first
- structured data-loading logic is preserved unless a documented change is required
- requested formats are exported when technically suitable
- generated output is inspected or unverified status is stated
---

# S622 Matplotlib Publication Script Builder

Use when executable plotting code or figure files are requested.

Procedure: inspect `ext/src/figures/` first and select the closest source pattern; do not skip the script inventory; preserve deterministic data construction and explicit exports; preserve CSV/table/dataframe loading logic unless there is a documented reason to change it; prefer minimal adaptation over a from-scratch rewrite; validate by running, syntax-checking, or rendered-output inspection when possible. Every original figures4papers `.py` file is preserved and indexed in `manifests/SCRIPT_INVENTORY.md`.

## Non-omission source rule

The complete source trees are preserved under `ext/src/`. This skill is a routing wrapper and logical reconstruction layer, not a replacement for the source files. For exact file-level coverage, inspect `manifests/src_manifest.json` and `manifests/src_FILE_integr_TABLE.md`.

## Executable-output requirement

When SVG/PNG/PDF files are requested, keep the generating source code whenever possible, export the requested assets when technically suitable, and visually inspect the rendered output when the environment allows. Do not fabricate data or silently substitute a pretty image for a source artifact.

SVG-specific rule: SVG is an export target, not a license to bypass the generating source. If the SVG export is unreadable or semantically broken, repair the generating code or provide a safer export while preserving the source artifact.
