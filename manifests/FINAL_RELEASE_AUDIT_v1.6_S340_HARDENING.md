# Final Release Audit v1.6.0 Addendum: S340 Routing Hardening

## Purpose

This addendum records the final logic-level integration requested after the initial v1.6.0 release candidate. The change strengthens S340 from a preserved source bundle into a mandatory writing and logic gate that is bound to router behavior and local skills.

## Files updated in this addendum

- `README.md`
- `CHANGELOG.md`
- `docs/EXTERNAL_SKILL_ATTRIBUTION_v1.6.md`
- `docs/SKILLS.md`
- `router/route.py`
- `router/weights_v1.3.2.yaml`
- `router/taxonomy.yaml`
- `router/SKILL_MAP_v1.3.2.md`
- `router/ext_router/ROUTER_ADDENDUM_RWF_S340_v2.md`
- `router/ext_router/ROUTER_REQUIREMENTS_BINDING_RWF_S340_v1.6.md`
- `skills/rwf_s340/MASTER.md`
- `skills/rwf_s340/S601_paper_story_section_architecture.md`
- `skills/rwf_s340/S602_claim_evidence_reverse_outline_review.md`
- `skills/rwf_s340/S603_bilingual_human_voice_delta_rewrite.md`
- `skills/rwf_s340/S604_experiment_result_narrative_and_caption.md`
- `skills/rwf_s340/S621_publication_figure_design_theory.md`
- `skills/rwf_s340/S622_matplotlib_publication_script_builder.md`
- `skills/rwf_s340/S623_visual_claim_caption_audit.md`
- `skills/rwf_s340/S640_s340_global_paper_logic_language_audit.md`
- `skills/rwf_s340/req_AND_forbid_phr.md`
- `skills_manifest.yaml`
- `manifests/src_manifest.json`
- `manifests/CHECKSUMS.sha256`

## S340 provenance correction

`S340_v4.2_theory_global_skill_bundle` is a user-authored local ruleset. It is not an external GitHub package, and no upstream GitHub repository should be invented or cited for it. The attribution file and README now state this explicitly.

## Routing guarantee

Writing-like tasks must now display or enforce `S640` as a global writing/logic gate, with local skills attached as companions:

- `S640 + S601` for paper structure and section architecture.
- `S640 + S602` for claim-evidence and reviewer-style audits.
- `S640 + S603` for polishing, translation, compression, expansion, and anti-AI-tone work.
- `S640 + S604` for result narratives and captions.
- `S621/S622/S623` for figure design, script/SVG/PNG generation, and visual-claim audit.
- `S650` for no-omission, checksum, path-length, and package openability validation.

## Forbidden-phrase gate

The new hard-requirement file requires removal or justification of mechanical phrasing, including but not limited to:

- `可追踪、可复查、可继续推进` and similar three-part slogans.
- repeated `不是……而是……` or `not A but B` constructions.
- empty `从A转向B` transitions without a causal chain.
- decorative terms such as `bridge`, `load-bearing knob`, `recipe`, or `criterion` when they do not name a concrete object.
- unsupported overclaims such as `robust`, `reliable`, `general`, `guaranteed`, or `always`.

## Validation output

```text
$ python3 tools/validate_no_omission.py

VALIDATION_OK
source_files=549
byte_preserved=540
release_modified=9
zyr_files=431
rpws_files=43
awesome_files=4
figures_files=70
s340_files=1

exit=0

$ python3 router/route.py 论文润色，去掉机械排比和禁止词 --topk 6

Hard requirement: RWF-S340 task detected → apply S640 as global writing/logic gate when prose is involved.
Next: skills/rwf_s340/MASTER.md and skills/rwf_s340/S640_s340_global_paper_logic_language_audit.md

PRIMARY: S640
SECONDARY (verification/companion): S601, S602, S603, S604

Top 4 matches:
1. S640 | s340_global_paper_logic_language_audit | s340_integrated | score=14.64
   hits: 论文润色, 禁止词, 机械排比
   weights: cat*1.60, s340_hard_writing_gate:skill+5.0, s340_hard_writing_gate:cat*1.45
   file: skills/rwf_s340/S640_s340_global_paper_logic_language_audit.md
2. rwf_s340_master | research_writing_figure_s340_integrated_master | composite | score=5.50
   hits: 论文润色, 禁止词, 机械排比
   weights: cat*1.10, s340_hard_writing_gate:skill+2.0
   file: skills/rwf_s340/MASTER.md
3. S603 | bilingual_human_voice_delta_rewrite | research_writing_integrated | score=4.62
   hits: 润色
   weights: cat*1.45, s340_hard_writing_gate:skill+2.2, s340_hard_writing_gate:cat*1.25
   file: skills/rwf_s340/S603_bilingual_human_voice_delta_rewrite.md
4. writing_engine | writing_engine | composite | score=2.64
   hits: 润色
   weights: cat*1.10, sentence_rewrite:skill+1.5
   file: skills/writing_engine/MASTER_v1.3.2.md

exit=0

$ python3 router/route.py README architecture SVG figure with physical layout and arrow semantics --topk 6

Hard requirement: RWF-S340 task detected → apply S640 as global writing/logic gate when prose is involved.
Next: skills/rwf_s340/MASTER.md and skills/rwf_s340/S640_s340_global_paper_logic_language_audit.md

PRIMARY: S640
SECONDARY (verification/companion): S601, S602, S603, S604

Top 2 matches:
1. S640 | s340_global_paper_logic_language_audit | s340_integrated | score=8.41
   weights: cat*1.60, s340_hard_writing_gate:skill+5.0, s340_hard_writing_gate:cat*1.45
   file: skills/rwf_s340/S640_s340_global_paper_logic_language_audit.md
2. rwf_s340_master | research_writing_figure_s340_integrated_master | composite | score=4.60
   hits: readme architecture, svg
   weights: cat*1.10, s340_hard_writing_gate:skill+2.0
   file: skills/rwf_s340/MASTER.md

exit=0

$ python3 router/route.py 压缩包无法打开，检查文件名过长和禁止遗漏 --topk 6

Hard requirement: RWF-S340 task detected → apply S640 as global writing/logic gate when prose is involved.
Next: skills/rwf_s340/MASTER.md and skills/rwf_s340/S640_s340_global_paper_logic_language_audit.md

PRIMARY: S650
SECONDARY (verification/companion): S407, S431

Top 3 matches:
1. S650 | integrated_pack_no_omission_validation | reproducibility_integrated | score=12.43
   hits: 压缩包无法打开, 文件名过长, 禁止遗漏
   weights: cat*1.35, integrated_release_validation:skill+4.8, integrated_release_validation:cat*1.35
   file: skills/rwf_s340/S650_integrated_pack_no_omission_validation.md
2. rwf_s340_master | research_writing_figure_s340_integrated_master | composite | score=1.17
   hits: 禁止遗漏
   weights: cat*1.10
   file: skills/rwf_s340/MASTER.md
3. S640 | s340_global_paper_logic_language_audit | s340_integrated | score=0.80
   weights: cat*1.60
   file: skills/rwf_s340/S640_s340_global_paper_logic_language_audit.md

exit=0
```
