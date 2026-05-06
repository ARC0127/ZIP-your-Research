# ROUTER Addendum: Integrated Research-Writing-Figure Skills v1.0

This addendum integrates three external skill repositories into the ZYR router. It is additive: original ZYR routes remain active.

## External repositories retained verbatim
- `ext/src/rpws/`
- `ext/src/awesome/`
- `ext/src/figures/`

## New skill categories
- `research_writing`: paper story, section architecture, bilingual polish, experiment narration.
- `figure_ops`: publication-quality scientific figures and visual-claim verification.

## New primary skills
- `S601 paper_story_section_architecture`
- `S602 claim_evidence_reverse_outline_review`
- `S603 bilingual_human_voice_delta_rewrite`
- `S604 experiment_result_narrative_and_table_caption`
- `S621 publication_figure_design_theory`
- `S622 matplotlib_publication_script_builder`
- `S623 visual_claim_caption_audit`

## Routing rules
1. If the user asks for paper writing/revision and the section logic is not stable, route to `S601` before sentence polishing.
2. If the user asks for review/self-review, route to `S602` plus `S203/S226/S503`.
3. If the user asks for bilingual polish, delta-only rewrite, or anti-AI-style editing, route to `S603` after evidence gate.
4. If the user asks for experiment/result/table/caption writing, route to `S604` plus experiment rigor skills.
5. If the user asks for paper figures, route to `S621` before code.
6. If the user asks for actual Matplotlib code or SVG/PNG/PDF generation, route to `S622` plus `S402/S431` when executable.
7. If the user asks whether a figure/caption supports a claim, route to `S623` plus `S512/S517`.

## Priority rule
ZYR state machine and guardrails override all external-source advice.
