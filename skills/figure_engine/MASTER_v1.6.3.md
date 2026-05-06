# MASTER v1.6.3 (Figure Engine)

> **Execution rules:** `boot/11_COMPLETION_FIRST_ANTI_SHORTCUT_v1.5.md` applies after lock activation.

---

# Figure Engine

`figure_engine` is the mandatory composite entry point for figure-making work in ZYR.

Use it whenever the task involves any of the following:
- scientific figures;
- paper figures and graphical abstracts;
- README or documentation figures;
- architecture, workflow, mechanism, or comparison diagrams;
- plotting-code repair or publication-format export.

## Hard binding

Any figure-making task must route through `figure_engine`.

`figure_engine` internally binds:
- `ext/src/figures/` (the preserved `figures4papers` source tree),
- `skills/rwf_s340/S621_publication_fig_design_theory.md`,
- `skills/rwf_s340/S622_matplotlib_publication_script_builder.md`,
- `skills/rwf_s340/S623_visual_claim_caption_audit.md`.

## Mandatory workflow

```text
lock figure claim and target medium
→ inspect figures4papers first and select the closest existing source pattern
→ preserve the source-code / data-loading logic unless an explicit change is required
→ adapt the script or layout minimally
→ export the requested artifact when technically suitable
→ inspect the rendered output
→ audit figure–caption–claim consistency
```

## Non-negotiable constraints

1. Do **not** start from scratch if `figures4papers` already contains a close visual pattern.
2. Do **not** replace CSV / table / dataframe input logic with ad hoc hard-coded arrays unless the user explicitly changes the data source or no structured source exists.
3. Do **not** fabricate values for aesthetic balance.
4. Keep the generating source whenever possible; image files alone are not enough.
5. When SVG is requested, treat it as an export format, not as permission to hand-draw a fragile figure.

## Source anchors

- `ext/src/figures/README.md`
- `ext/src/figures/fig_skill/SKILL.md`
- `ext/src/figures/fig_skill/ref/design_theory.md`
- `ext/src/figures/fig_skill/ref/common_patterns.md`
- `ext/src/figures/fig_skill/ref/api.md`
- `ext/src/figures/fig_skill/ref/tutorials.md`
- `ext/src/figures/fig_skill/ref/demos.md`
