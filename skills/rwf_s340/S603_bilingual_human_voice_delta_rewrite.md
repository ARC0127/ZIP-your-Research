---
id: S603
name: bilingual_human_voice_delta_rewrite
category: research_writing_integrated
version: v1.6.3
triggers:
- Chinese polish
- English polish
- bilingual rewrite
- human voice
- anti AI tone
- 润色
- 去AI味
- 中文润色
- 英文润色
- 中英互译
inputs_required:
- source text
- target language and tone
- locked terminology/formulas/citations/numbers
- compression or expansion target when relevant
outputs_required:
- revised text
- delta explanation when requested
- preserved facts list
- unresolved ambiguity notes
quality_gates:
- meaning, citations, formulas, and numbers are preserved
- style edits do not create new claims
- S640 forbidden-phrase and evidence gates are applied
---

# S603 Bilingual Human-Voice Delta Rewrite

Use for Chinese/English academic polishing, translation, compression, expansion, anti-AI-tone revision, and delta-based rewriting.

Procedure: preserve facts/formulas/citations/numbers; distinguish language from logic failures; remove mechanical or marketing-like phrasing; preserve LaTeX commands and labels; provide delta explanations when requested.

## Non-omission source rule

The complete source trees are preserved under `ext/src/`. This skill is a routing wrapper and logical reconstruction layer, not a replacement for the source files. For exact file-level coverage, inspect `manifests/src_manifest.json` and `manifests/src_FILE_integr_TABLE.md`.


## Mandatory companion

For polishing, translation, compression, expansion, or anti-AI-tone rewriting, apply `S640` first. S603 may change language, but it must not bypass S640 constraints on evidence, forbidden phrases, and locked terminology.
