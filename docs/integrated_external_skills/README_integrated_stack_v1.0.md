# ZYR Integrated Research-Writing-Figure Skills Pack v1.0

## What this package is
This package is a full ZIP-your-Research integration of three external skill repositories:

1. `Research-Paper-Writing-Skills-main`
2. `awesome-ai-research-writing-main`
3. `figures4papers-main`

It keeps the original ZIP-your-Research repository intact as the base runtime, retains every file from the three external repositories, and adds ZYR-native S6xx skills plus router integration.

## What was changed
Inside `ZIP-your-Research-main_integrated/`:

- Original ZYR files are copied as the base.
- All three external repositories are retained under `ext/src/`.
- New ZYR-native skills are added:
  - `skills/rw/S601_paper_story_section_architecture.md`
  - `skills/rw/S602_claim_evidence_reverse_outline_review.md`
  - `skills/rw/S603_bilingual_human_voice_delta_rewrite.md`
  - `skills/rw/S604_experiment_result_narrative_and_table_caption.md`
  - `skills/fig_ops/S621_publication_figure_design_theory.md`
  - `skills/fig_ops/S622_matplotlib_publication_script_builder.md`
  - `skills/fig_ops/S623_visual_claim_caption_audit.md`
- A master entrypoint is added:
  - `skills/master_integrated/MASTER_research_writing_figure_stack_v1.0.md`
- Router integration is added:
  - `router/ext_router/ROUTER_ADDENDUM_research_writing_figures_v1.0.md`
  - appended entries in `router/SKILL_MAP_v1.3.2.md`
  - updated `router/taxonomy.yaml`
  - patched `router/route.py` with `research_writing_figure_stack` composite hints.

## Non-skipping guarantee
The integration does not discard source content. Every file from the three source repositories is copied into `ext/src/`, and source checksums are recorded in:

- `integr_manifest.json`
- `CHECKSUMS.sha256`

Original ZIP archives are also preserved under `original_zips/` at the package root.

## How to use
Use the integrated root as the ZYR repository:

```bash
cd ZIP-your-Research-main_integrated
python router/route.py "帮我审查论文Introduction的逻辑和证据链" --topk 8
python router/route.py "生成一个论文用matplotlib grouped bar svg和png" --topk 8
```

Expected route examples:

- Paper structure / abstract / introduction / method / experiments → `S601`
- Claim-evidence review / reverse outline / reviewer comments → `S602`
- Chinese/English polish / anti-AI-style rewrite / delta output → `S603`
- Experiment narrative / table caption / figure caption → `S604`
- Publication figure design → `S621`
- Matplotlib script generation → `S622`
- Figure/caption claim audit → `S623`

## Priority rule
If an external-source recommendation conflicts with ZYR guardrails, the ZYR guardrail wins.
