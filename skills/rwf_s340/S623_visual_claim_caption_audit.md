---
id: S623
name: visual_claim_caption_audit
category: figure_design_integrated
version: v2.0
triggers:
  - figure audit
  - caption audit
  - visual claim
  - panel consistency
  - 图表审查
  - caption检查
  - 图文一致
---

# S623 Visual Claim and Caption Audit

Use to check whether a figure, caption, and manuscript statement support the same claim.

Procedure: extract visual claim from caption and surrounding text; verify panel mapping/axes/units/legends/colors/metric direction; detect overclaim or mismatch; rewrite caption to describe actual evidence; mark unresolved ambiguity as `UNKNOWN`.

## Non-omission source rule

The complete source trees are preserved under `ext/*`. This skill is a routing wrapper and logical reconstruction layer, not a replacement for the source files. For exact file-level coverage, inspect `manifests/src_manifest.json` and `manifests/src_FILE_integr_TABLE.md`.


## Figure acceptance gate

A figure is not accepted if arrows collide with boxes/text, panel borders are visibly inconsistent, labels are not public-facing, or the visual hierarchy contradicts the stated control/workflow/validation semantics.
