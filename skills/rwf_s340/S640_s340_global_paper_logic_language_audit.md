---
id: S640
name: s340_global_paper_logic_language_audit
category: s340_integrated
version: v1.6.5
triggers:
- S340
- writing engine
- proof engine
- global paper audit
- paper writing
- manuscript
- research plan
- README text
- polish
- rewrite
- revise
- anti AI tone
- forbidden phrases
- mechanical phrasing
- style logic review
- 论文润色
- 论文重构
- 研究计划
- 逻辑审查
- 公式图表引用核查
- 中英文合并
- 禁止词
- 禁用短语
- 机械排比
- 去AI味
inputs_required:
- writing artifact or excerpt
- target reader and artifact type
- locked facts/evidence/references/terminology
- user-specific forbidden phrases or style constraints
outputs_required:
- logic-and-language audit
- revised text or concrete revision operations
- unsupported/UNKNOWN claim list
- final S340 gate status
quality_gates:
- unsupported claims are not polished into certainty
- vague transitions are replaced by causal logic
- forbidden mechanical phrases and overclaims are removed
---

# S640 S340 Global Paper Logic and Language Audit

Use for broad paper writing, rewriting, polishing, final audit, LaTeX/PDF delivery, research plan revision, README architecture text, CV research-description polishing, or manuscript-level logic verification.

## Mandatory status

This skill is a **hard global gate**, not an optional style preference. For writing-like tasks, the assistant must apply S640 before accepting the final text.

S640 must be combined as follows:

```text
paper/story/section work       → S640 + S601
claim-evidence/reviewer audit  → S640 + S602
translation/polishing/rewrite  → S640 + S603
results/captions/ablation text → S640 + S604 (+ S623 for visual claims)
README architecture text       → S640 + S621/S623 when the figure is involved
```

## Procedure

1. Lock artifact type, target reader, frozen constraints, and source evidence.
2. Check structure before wording: problem, gap, method object, evidence, limitation.
3. Build or inspect the claim-evidence chain.
4. Preserve formulas, references, values, file states, and user-locked wording unless explicitly asked to revise them.
5. Remove unsupported claims, vague transitions, mechanical slogans, and forbidden/high-risk phrasing.
6. Mark missing evidence as `UNKNOWN` rather than hiding it in polished prose.
7. Use `skills/rwf_s340/req_AND_forbid_phr.md` as the mandatory phrase and logic gate.

The full user-authored S340 source file is preserved at `ext/src/S340_v4.2_theory_global_skill_bundle/S340_v4.2_theory_global_skill.md`.

## Forbidden phrase and structure gate

S640 must search for and repair high-risk patterns, including but not limited to:

- mechanical three-part slogans such as `trackable, reviewable, and continuously actionable` or Chinese `可追踪、可复查、可继续推进`;
- repeated `not A but B` / `不是……而是……` constructions;
- empty `from A to B` / `从A转向B` transitions without a causal chain;
- decorative terms such as `bridge`, `load-bearing knob`, `recipe`, or `criterion` when they do not name a concrete object;
- unsupported `robust`, `reliable`, `general`, `guaranteed`, `always`, or similar overclaims;
- marketing-like wording such as `empowers`, `unleashes`, `seamlessly`, or `end-to-end solution` when it replaces technical explanation.

## Non-omission source rule

The complete source trees are preserved under `ext/src/`. This skill is a routing wrapper and logical reconstruction layer, not a replacement for the source files. For exact file-level coverage, inspect `manifests/src_manifest.json` and `manifests/src_FILE_integr_TABLE.md`.

## v1.7 safe-release source-traceability addendum

In a safety release, first inspect `manifests/RELEASE_CAPABILITIES.yaml`. If
the original S340 source archive is absent, mark
`DEGRADED_SOURCE_TRACEABILITY` and do not claim exact comparison with or
execution of that archive. The embedded S640 rules and any available,
license-admitted RPWS material may still be used, but the output must preserve
this limitation until the original source is restored and verified.
