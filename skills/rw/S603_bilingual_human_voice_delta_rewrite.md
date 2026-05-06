---
id: S603
name: bilingual_human_voice_delta_rewrite
category: research_writing
triggers:
  - polish
  - rewrite
  - academic polish
  - chinese polish
  - english polish
  - human voice
  - remove ai style
  - changed sentences only
  - 润色
  - 改写
  - 去AI味
  - 中文润色
  - 英文润色
  - 只输出修改句
---
# S603 Bilingual Human-Voice Delta Rewrite

## Source integration
This skill integrates:
- all revision and polish prompt patterns in `awesome-ai-research-writing-main/README.md`
- section-specific revision discipline from `Research-Paper-Writing-Skills-main/research-paper-writing/SKILL.md`
- ZYR `writing_engine/MASTER_v1.3.2.md` Gate → Rewrite → Verify discipline

## Purpose
Use this skill when the user asks for Chinese or English academic rewriting, translation, concision, expansion, human-voice polishing, or delta-only revision.

## Required ZYR routing
Run Gate first:
1. Identify language, target venue/context, section, strictness, and whether evidence lock is required.
2. If factual or venue claims are present, verify before rewriting or mark `UNKNOWN`.
3. Rewrite only within the requested scope.
4. Verify that the rewrite did not introduce new claims.

## Rewriting principles
- Preserve technical meaning and mathematical objects.
- Do not add unsupported claims for fluency.
- Do not convert precise scientific claims into vague rhetoric.
- Avoid formulaic contrast patterns unless the mechanism is explicitly explained.
- Avoid decorative vocabulary that weakens professional directness.
- For Chinese writing, improve logical continuity and sentence rhythm without creating mechanical parallelism.
- For English LaTeX, preserve commands, labels, citations, equations, and environments unless explicitly asked to modify them.

## Delta output schema
When the user asks for modifications rather than a clean rewrite, output:
- `ORIG:`
- `NEW:`
- `WHY:`
- `CLAIM_CHANGE:` `none | narrowed | broadened | new_claim_added`
- `EVIDENCE_STATUS:` `verified | unknown | not_applicable`

## Full rewrite output schema
When the user asks for a clean rewritten version, output only the revised text unless they ask for commentary.
