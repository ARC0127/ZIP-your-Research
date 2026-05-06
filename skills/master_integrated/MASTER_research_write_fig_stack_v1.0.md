# MASTER Research-Writing-Figure Integrated Stack v1.0

This master entrypoint fuses three external skill repositories into ZIP-your-Research without replacing the ZYR state machine.

## Integrated sources
1. Research-Paper-Writing-Skills: section writing, paper story, reverse outline, reviewer-facing structure.
2. awesome-ai-research-writing: bilingual rewriting prompts, human-voice polishing, experiment analysis, reviewer prompts, caption prompts.
3. figures4papers: publication figure design theory, Matplotlib API conventions, demo scripts and generated outputs.

All original files are retained verbatim under `ext/src/`. The integration adds ZYR-native S6xx skills and router hooks; it does not delete original ZYR skills.

## Primary routing
- Manuscript structure / abstract / introduction / method / experiments → `S601`.
- Claim-evidence audit / reverse outline / reviewer report → `S602`.
- Sentence polish / bilingual rewrite / human voice / delta-only output → `S603`.
- Result narrative / table or figure caption → `S604`.
- Publication figure design → `S621`.
- Matplotlib figure script generation → `S622`.
- Visual claim and caption audit → `S623`.

## Mandatory ordering
1. ZYR Mode Lock and scope lock.
2. Claim/evidence check when scientific claims are involved.
3. Section or visual routing.
4. Execution.
5. Verification and completion status.

## Non-overwrite rule
If any integrated source conflicts with ZYR guardrails, ZYR wins. In particular:
- no unsupported claims
- no invented citations or results
- no fake file/path/execution claims
- no heuristic downgrade for research tasks
- no broad rewrite when the user requested delta-only changes
