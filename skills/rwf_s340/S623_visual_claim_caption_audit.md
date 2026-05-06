---
id: S623
name: visual_claim_caption_audit
category: figure_design_integrated
version: v1.6.3
triggers:
- figure caption
- visual claim
- caption audit
- figure audit
- 图注
- 视觉审查
- 图文一致
- workflow audit
inputs_required:
- figure or figure specification
- caption or intended claim
- surrounding manuscript claim when available
outputs_required:
- claim-to-visual audit
- caption risk list
- mismatch report
- correction suggestions
quality_gates:
- caption does not exceed what the visual supports
- figure, caption, and surrounding prose are mutually consistent
- figures4papers-based output is checked at the rendered level when available
- unsupported visual claims are explicitly downgraded
---

# S623 Visual Claim and Caption Audit

Use when deciding whether a figure, workflow diagram, or caption actually supports the stated claim.

Procedure: inspect the rendered figure or the figure specification; compare the visual to the claimed takeaway; compare the caption to the manuscript statement; flag any panel, legend, label, or wording that overclaims the evidence. When the figure was generated through `figure_engine`, confirm that the final output still matches the figures4papers-derived source logic and that no unsupported simplification was introduced during adaptation.

## Visual-consistency rule

A figure is not accepted if arrows collide with boxes or text, panel borders are visibly inconsistent, labels are not public-facing, the chosen format obscures the underlying source logic, or the visual hierarchy contradicts the stated semantics.

## Caption rule

The caption must describe what the visual actually shows. It must not inherit stronger claims from the surrounding prose when the visual itself does not support them.
