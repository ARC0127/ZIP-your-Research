---
id: rwf_s340_master
name: research_writing_figure_s340_integrated_master
category: composite
version: v1.7.0
---

# RWF-S340 Integrated Master Skill (suite v1.7.0)

This master integrates external research-writing and figure-making materials with the user-authored `S340 v4.2` ruleset into a ZYR-native routing layer.

Preserved sources:

- `ext/src/rpws/`: Research-Paper-Writing-Skills, preserved as the primary external writing backend.
- `ext/src/awesome/`: awesome-ai-research-writing, preserved as supplementary writing references and examples.
- `ext/src/figures/`: figures4papers, preserved as the primary external figure backend, including plotting scripts and assets.
- `ext/src/S340_v4.2_theory_global_skill_bundle/`: user-authored S340 v4.2 ruleset, all source content preserved.

## Mandatory operating chain

```text
ZYR boot/state/guardrails
→ router/route.py + router/ext_router/ROUTER_req_BINDING_RWF_S340_v1.6.md
→ idea/method/storyline tasks: proof_engine → S203/S226/S227/S230 → S237/S240/S241 when needed
→ writing tasks: proof_engine first when logic is being formed, then writing_engine → ext/src/rpws/ → S601/S602/S603/S604 → S640
→ figure tasks: figure_engine → inspect ext/src/figures/ → S621/S622/S623
→ release-validation tasks: S650
```

## Hard requirements

1. `proof_engine` is mandatory for research idea construction, method design, theoretical framing, claim formation, contribution definition, paper storyline construction, and proof/derivation checking.
2. `writing_engine` is mandatory for visible writing tasks.
3. `figure_engine` is mandatory for figure-making tasks.
4. `S640` is mandatory for writing-like work.
5. `figures4papers` inspection is mandatory before proposing a new figure implementation.
6. CSV/table/dataframe loading logic should be preserved unless the data source is intentionally changed and documented.

The detailed requirement and forbidden-phrase gate is:

- `skills/rwf_s340/req_AND_forbid_phr.md`

## Non-omission rule

The source trees are preserved under `ext/src/`. The S6xx/S640/S650 files are routing and execution wrappers, not replacements for source files. Non-omission is checked by:

- `manifests/src_manifest.json`
- `manifests/src_FILE_integr_TABLE.md`
- `manifests/SCRIPT_INVENTORY.md`
- `tools/validate_no_omission.py`

## v1.7 safe-release profile addendum

The preservation statements above apply to the full development checkout.
The default safety release is a capability-declared subset: consult
`manifests/RELEASE_CAPABILITIES.yaml` before invoking an external backend.
When that manifest or the declared local path reports an unavailable source,
return its explicit unavailable/degraded status and never claim that the
excluded tree was inspected. Release completeness is measured against the
fail-closed release policy, not against license-blocked source trees.
