---
id: S603
name: bilingual_human_voice_delta_rewrite
category: research_writing_integrated
version: v2.0
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
---

# S603 Bilingual Human-Voice Delta Rewrite

Use for Chinese/English academic polishing, translation, compression, expansion, anti-AI-tone revision, and delta-based rewriting.

Procedure: preserve facts/formulas/citations/numbers; distinguish language from logic failures; remove mechanical or marketing-like phrasing; preserve LaTeX commands and labels; provide delta explanations when requested.

## Non-omission source rule

The complete source trees are preserved under `ext/*`. This skill is a routing wrapper and logical reconstruction layer, not a replacement for the source files. For exact file-level coverage, inspect `manifests/src_manifest.json` and `manifests/src_FILE_integr_TABLE.md`.


## Mandatory companion

For polishing, translation, compression, expansion, or anti-AI-tone rewriting, apply `S640` first. S603 may change language, but it must not bypass S640 constraints on evidence, forbidden phrases, and locked terminology.
