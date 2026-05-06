# ROUTER Addendum: Integrated Research-Writing-Figure Skills v1.0

This addendum integrates external writing and figure repositories into the ZYR router. It is additive: original ZYR routes remain active, but figure and writing requests now have mandatory engine bindings.

## External repositories retained verbatim
- `ext/src/rpws/`
- `ext/src/awesome/`
- `ext/src/figures/`

## Primary engines
- `writing_engine`: visible writing tasks, backed by Research-Paper-Writing-Skills and the integrated S601-S604 + S640 chain.
- `figure_engine`: figure-making tasks, backed by figures4papers and the integrated S621-S623 chain.

## Primary skills
- `S601 paper_story_section_architecture`
- `S602 claim_evidence_reverse_outline_review`
- `S603 bilingual_human_voice_delta_rewrite`
- `S604 experiment_result_narrative_and_caption`
- `S621 publication_figure_design_theory`
- `S622 matplotlib_publication_script_builder`
- `S623 visual_claim_caption_audit`

## Routing rules
1. If the user asks for paper writing or revision, route to `writing_engine` first.
2. If the user asks for review or self-review, route to `writing_engine` + `proof_engine`, then use `S602`.
3. If the user asks for bilingual polish, delta-only rewrite, or anti-AI-style editing, route to `writing_engine`, then use `S603` after the evidence gate.
4. If the user asks for experiment/result/table/caption writing, route to `writing_engine`, then use `S604`.
5. If the user asks for paper figures, workflow diagrams, or architecture explanations, route to `figure_engine` first.
6. If the user asks for actual plotting code, file export, or figure repair, route to `figure_engine` + `coding_engine`, then use `S622`.
7. If the user asks whether a figure or caption supports a claim, route to `figure_engine`, then use `S623`.

## Figure-specific rule
Before proposing a new figure implementation, inspect `ext/src/figures/` and reuse the closest figures4papers pattern when practical. Do not replace CSV / table / dataframe input logic with hard-coded arrays without a documented reason.

## Priority rule
ZYR state machine and guardrails override all external-source advice.
