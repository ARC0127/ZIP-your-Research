# MASTER v1.6.5 (Figure Engine)

`figure_engine` is the mandatory composite entry point for all figure-making work in ZYR.

Use it whenever a task involves:
- scientific figures, paper figures, or graphical abstracts;
- README, workflow, architecture, or mechanism diagrams;
- plotting-code generation, repair, or adaptation;
- figure export to PNG / PDF / SVG;
- figure-caption or visual-claim auditing when the visual itself is being created or revised.

## Mandatory backend

`figure_engine` is backed by the preserved `figures4papers` source tree:

```text
figure task
→ figure_engine
→ inspect ext/src/figures/ first
→ select the closest reusable figures4papers pattern
→ adapt the source minimally
→ export the requested artifact when technically suitable
→ inspect the rendered output
→ audit figure-caption-claim consistency
```

## Bound skills

- `skills/rwf_s340/S621_publication_fig_design_theory.md`
- `skills/rwf_s340/S622_matplotlib_publication_script_builder.md`
- `skills/rwf_s340/S623_visual_claim_caption_audit.md`

## Non-negotiable rules

1. Do not start from scratch when `ext/src/figures/` already contains a close visual or plotting pattern.
2. Do not replace CSV, table, dataframe, or other structured data-loading logic with ad hoc hard-coded arrays unless the data source is intentionally changed and documented.
3. Do not fabricate numbers, labels, or visual structure for aesthetics.
4. Keep the generating source whenever possible; exported images alone are not sufficient.
5. Treat SVG, PNG, and PDF as export formats, not as substitutes for source-generation logic.

## Source anchors

- `ext/src/figures/README.md`
- `ext/src/figures/fig_skill/SKILL.md`
- `ext/src/figures/fig_skill/ref/design_theory.md`
- `ext/src/figures/fig_skill/ref/common_patterns.md`
- `ext/src/figures/fig_skill/ref/api.md`
- `ext/src/figures/fig_skill/ref/tutorials.md`
- `ext/src/figures/fig_skill/ref/demos.md`

## v1.7 safe-release capability gate

This addendum is authoritative when the skill is loaded from a safety release.
The mandatory-backend workflow above may run only when
`manifests/RELEASE_CAPABILITIES.yaml` reports the figures4papers capability as
available **and** its declared local path exists.

If that source is absent or its redistribution gate is not satisfied:

1. return `SOURCE_UNAVAILABLE` and identify the missing capability;
2. do not claim that figures4papers was inspected, selected, adapted, or run;
3. do not silently replace the missing backend with invented examples;
4. provide only bounded unblock instructions, including license verification
   and an explicit user-approved local installation path.

`S623` may still audit a figure supplied by the user because that read-only
caption/visual-claim check does not require the excluded source tree. Creating
or revising a figure through this composite remains blocked until the declared
backend is available.
