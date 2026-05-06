---
id: S602
name: claim_evidence_reverse_outline_review
category: research_writing_integrated
version: v2.0
triggers:
  - reverse outline
  - reviewer audit
  - claim evidence
  - paper review
  - 证据链
  - 逻辑审查
  - 审稿意见
  - 逐行审查
---

# S602 Claim-Evidence Reverse Outline Review

Use for deep paper review, reviewer-style critique, line-level logic audit, and claim-evidence consistency checking.

Procedure: extract strong claims; locate evidence; mark unsupported claims as `UNSUPPORTED`; reverse-outline paragraphs; apply first-error-wins; produce actionable fixes: weaken claim, add evidence, move paragraph, define term, add experiment, or remove unsupported statement.

## Non-omission source rule

The complete source trees are preserved under `ext/*`. This skill is a routing wrapper and logical reconstruction layer, not a replacement for the source files. For exact file-level coverage, inspect `manifests/src_manifest.json` and `manifests/src_FILE_integr_TABLE.md`.


## Mandatory companion

For reviewer-style critique or line-level logic audit, apply `S640` first and then S602. S640 removes unsupported phrasing and high-risk language; S602 maps claims to evidence and identifies the first logic failure.
