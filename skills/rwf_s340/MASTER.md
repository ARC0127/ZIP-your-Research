---
id: rwf_s340_master
name: research_writing_figure_s340_integrated_master
category: composite
version: v1.6.0
---

# RWF-S340 Integrated Master Skill

This master integrates external research-writing and figure-making materials with the user-authored `S340 v4.2` ruleset into a ZYR-native routing layer.

Preserved sources:

- `ext/src/rpws/`: Research-Paper-Writing-Skills, all 43 source files preserved.
- `ext/src/awesome/`: awesome-ai-research-writing, all 4 source files preserved.
- `ext/src/figures/`: figures4papers, all 70 source files preserved, including plotting scripts and image/PDF assets.
- `ext/src/S340_v4.2_theory_global_skill_bundle/`: user-authored S340 v4.2 ruleset, all source content preserved.

## Mandatory operating chain

```text
ZYR boot/state/guardrails
→ router/route.py + router/ext_router/ROUTER_REQUIREMENTS_BINDING_RWF_S340_v1.6.md
→ S640 global writing/logic hard gate for writing-like tasks
→ S601/S602/S603/S604 for paper writing, review, rewriting, and result narratives
→ S621/S622/S623 for figure design, script output, and visual-claim audit
→ S650 for packaging, source preservation, checksum, and path-length validation
```

## Hard requirement

`S640` is not optional for writing-like work. It must be applied whenever the task involves paper prose, research-plan prose, README architecture text, reviewer critique, rebuttal, CV research descriptions, translation, polishing, or figure/table captions.

The detailed requirement and forbidden-phrase gate is:

- `skills/rwf_s340/req_AND_forbid_phr.md`

## Non-omission rule

The source trees are preserved under `ext/src/`. The S6xx/S640/S650 files are routing and execution wrappers, not replacements for source files. Non-omission is checked by:

- `manifests/src_manifest.json`
- `manifests/src_FILE_integr_TABLE.md`
- `manifests/SCRIPT_INVENTORY.md`
- `tools/validate_no_omission.py`
