# ZYR v1.6.1 Repair Report

- generated_utc: 2026-05-06T08:32:03Z
- input_package: `ZIP-your-Research_v1.6.0_win_safe_install_short_paths.zip`
- output_version: `1.6.1`

## Conclusion

The repaired package keeps the prior ZYR logic: boot → intake → MODE_LOCK → CONFIRM → locked execution → router → engine/skill execution → artifact completion. The repair does not replace the state machine; it reconciles the Windows-safe short-path package with README, manifests, validation scripts, and routing documentation.

## README architecture update

`README.md` was rewritten around the actual repository layout and now contains an explicit control table of the form: “If I need to do X, control ZYR to call Y engine and bind Z skills.” The table covers boot, proof_engine, writing_engine, coding_engine, RWF/S340 writing, figure generation, experiment planning, reproducibility packaging, S650 ZIP validation, and migration prompts.

## Repaired path families
- `external_sources/`, `external_skills/original_sources/` → `ext/src/`
- `skills/research_writing/` → `skills/rw/`
- `skills/figure_ops/` → `skills/fig_ops/`
- `skills/integrated_master/` → `skills/master_integrated/`
- `router/integrated_extensions/` → `router/ext_router/`
- `skills/experiments/` → `skills/exp/`
- `manifests/SOURCE_MANIFEST.json` → `manifests/src_manifest.json`
- `manifests/SOURCE_FILE_INTEGRATION_TABLE.md` → `manifests/src_FILE_integr_TABLE.md`
- `skills/rwf_s340/REQUIREMENTS_AND_FORBIDDEN_PHRASES.md` → `skills/rwf_s340/req_AND_forbid_phr.md`
- `docs/assets/zyr_research_os_architecture_v1_6.svg` → `docs/assets/zyr_research_os_arch_v1_6.svg`

## Changed files
- `CHANGELOG.md`
- `INDEX.md`
- `README.md`
- `artifacts/integration/integr_manifest.json`
- `artifacts/integration/src_FILE_integr_TABLE.md`
- `docs/EXTERNAL_SKILL_ATTRIBUTION_v1.6.md`
- `docs/SKILLS_INDEX_GENERATED_v1.3.md`
- `docs/integrated_external_skills/LOGIC_RECONSTRUCTION_v1.0.md`
- `docs/integrated_external_skills/README_integrated_stack_v1.0.md`
- `manifests/FINAL_NO_DELETE_OVERLAY_AUDIT_v1.6.md`
- `manifests/FINAL_RELEASE_AUDIT_v1.6.md`
- `manifests/FINAL_RELEASE_AUDIT_v1.6_S340_HARDENING.md`
- `manifests/PATH_LENGTH_REPORT.md`
- `manifests/README_REWRITE_AUDIT_v1.6.md`
- `manifests/ROUTE_SMOKE_TESTS_v1.6.json`
- `manifests/SCRIPT_INVENTORY.md`
- `manifests/WINDOWS_SAFE_INSTALL_REPORT_v1.6.md`
- `manifests/WINDOWS_SAFE_PATH_RENAME_MAP_v1.6.csv`
- `manifests/WINDOWS_SAFE_PATH_RENAME_MAP_v1.6.json`
- `manifests/src_FILE_integr_TABLE.md`
- `manifests/src_manifest.json`
- `router/SKILL_MAP_v1.3.2.md`
- `router/ext_router/ROUTER_ADDENDUM_RWF_S340_v2.md`
- `router/ext_router/ROUTER_ADDENDUM_research_write_figures_v1.0.md`
- `router/ext_router/ROUTER_req_BINDING_RWF_S340_v1.6.md`
- `router/route.py`
- `router/taxonomy.yaml`
- `router/weights_v1.3.2.yaml`
- `skills/fig_ops/S621_publication_fig_design_theory.md`
- `skills/master_integrated/MASTER_research_write_fig_stack_v1.0.md`
- `skills/rw/S601_paper_story_section_arch.md`
- `skills/rwf_s340/MASTER.md`
- `skills/rwf_s340/S601_paper_story_section_arch.md`
- `skills/rwf_s340/S602_claim_evidence_reverse_outline_review.md`
- `skills/rwf_s340/S603_bilingual_human_voice_delta_rewrite.md`
- `skills/rwf_s340/S604_experiment_result_narrative_and_caption.md`
- `skills/rwf_s340/S621_publication_fig_design_theory.md`
- `skills/rwf_s340/S622_matplotlib_publication_script_builder.md`
- `skills/rwf_s340/S623_visual_claim_caption_audit.md`
- `skills/rwf_s340/S640_s340_global_paper_logic_language_audit.md`
- `skills/rwf_s340/S650_integrated_pack_no_omission_valid.md`
- `skills_manifest.yaml`
- `tools/validate_integrated_sources.py`
- `tools/validate_no_omission.py`
- `v`

## Validation results
### `python3 tools/validate_no_omission.py`
- returncode: 0
```text
VALIDATION_OK
source_files=549
byte_preserved=539
release_modified=10
zyr_files=431
rpws_files=43
awesome_files=4
figures_files=70
s340_files=1
```
### `python3 tools/validate_integrated_sources.py`
- returncode: 0
```text
VALIDATION_OK
source_files=117
new_skills=8
```
### `python3 -m py_compile tools/validate_no_omission.py tools/validate_integrated_sources.py router/route.py`
- returncode: 0

## Manifest consistency
- skills_manifest_missing_paths: 0
- src_manifest_missing_paths: 0
- current_file_count_without_git: 598
- max_path_length_current: 134
- max_path_current: `skills/platform_zyr_skills/rewrites/claude_code_runtime_rw_20260331_f15/by_source/remote_runtime/remotePermissionBridge_REWRITE_ZYR.md`

## Route smoke tests
- `论文润色 S340 逻辑审查` → returncode=0; PRIMARY: S640
- `matplotlib plotting script svg png` → returncode=0; PRIMARY: S622
- `压缩包 文件遗漏 checksum path length` → returncode=0; PRIMARY: S650
