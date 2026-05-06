---
id: S623
name: visual_claim_caption_audit
category: figure_ops
triggers:
  - figure audit
  - caption audit
  - visual claim
  - figure table audit
  - caption rewrite
  - 图表审查
  - 图题优化
  - caption
---
# S623 Visual Claim and Caption Audit

## Source integration
This skill integrates:
- `figures4papers-main/scientific-figure-making/references/common-patterns.md`
- `figures4papers-main/scientific-figure-making/references/design-theory.md`
- `Research-Paper-Writing-Skills-main/research-paper-writing/references/experiments.md`
- `awesome-ai-research-writing-main/README.md` caption prompts

## Purpose
Use this skill to check whether a figure/table and its caption actually support the manuscript claim.

## Audit checklist
1. What exact claim does the visual support?
2. Are all axes, units, sample sizes, statistics, and metric directions clear?
3. Are baselines, variants, and proposed methods visually distinguishable without relying only on color?
4. Does the caption state the comparison target and interpretation boundary?
5. Does any annotation overstate causality or significance?
6. Would the figure remain readable after being reduced to journal column width?
7. Does the visual duplicate a table without adding interpretive value?

## Output schema
| Visual ID | Claimed message | Evidence shown | Missing metadata | Visual risk | Caption risk | Required fix |
