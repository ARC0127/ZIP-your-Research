# Windows-safe install package report (v1.6)
This package is optimized for Windows Explorer extraction and avoids nested source ZIP duplication.
## Policy
- Active install package only.
- No nested original ZIP archives.
- Long paths are renamed, not dropped.
- File contents are preserved byte-for-byte and checked with SHA-256.
- Full old-path to new-path mapping is stored in `WINDOWS_SAFE_PATH_RENAME_MAP_v1.6.csv` and `.json`.

## Summary
- Source files: 591
- Files copied: 591
- Renamed paths: 222
- Max old internal path length: 200
- Max new internal path length: 134
- Checksum mismatches: 0

## Longest paths before
- `200` `ext/src/rpws/research-paper-writing/references/examples/introduction/technical-challenge-version-2-existing-task-insight-backed-by-traditional.md`
- `179` `ext/src/rpws/research-paper-writing/references/examples/introduction/pipeline-version-1-one-contribution-multi-advantages.md`
- `177` `ext/src/rpws/research-paper-writing/references/examples/introduction/pipeline-version-3-new-module-on-existing-pipeline.md`
- `170` `ext/src/rpws/research-paper-writing/references/examples/introduction/technical-challenge-version-1-existing-task.md`
- `167` `ext/src/rpws/research-paper-writing/references/examples/introduction/technical-challenge-version-3-novel-task.md`
- `165` `ext/src/rpws/research-paper-writing/references/examples/introduction/pipeline-not-recommended-abstract-only.md`
- `164` `ext/src/rpws/research-paper-writing/references/examples/introduction/pipeline-version-4-observation-driven.md`
- `164` `ext/src/rpws/research-paper-writing/references/examples/introduction/version-3-general-to-specific-setting.md`
- `163` `ext/src/rpws/research-paper-writing/references/examples/introduction/pipeline-version-2-two-contributions.md`
- `161` `ext/src/rpws/research-paper-writing/references/examples/introduction/novel-task-challenge-decomposition.md`
- `158` `ext/src/rpws/research-paper-writing/references/examples/introduction/version-1-task-then-application.md`
- `156` `ext/src/rpws/research-paper-writing/references/examples/introduction/version-4-open-with-challenge.md`
- `154` `ext/src/rpws/research-paper-writing/references/examples/introduction/version-2-application-first.md`
- `154` `ext/src/rpws/research-paper-writing/references/examples/method/method-writing-common-issues-note.md`
- `154` `ext/src/rpws/research-paper-writing/references/examples/method/neural-body-annotated-figure-text.md`
- `150` `ext/src/rpws/research-paper-writing/references/examples/method/example-of-the-three-elements.md`
- `147` `ext/src/rpws/research-paper-writing/references/examples/method/module-motivation-patterns.md`
- `146` `ext/src/rpws/research-paper-writing/references/examples/method/module-design-instant-ngp.md`
- `145` `ext/src/rpws/research-paper-writing/references/examples/method/module-triad-neural-body.md`
- `142` `ext/src/rpws/research-paper-writing/references/examples/method/pre-writing-questions.md`

## Longest paths after
- `134` `skills/platform_zyr_skills/rewrites/claude_code_runtime_rw_20260331_f15/by_source/remote_runtime/remotePermissionBridge_REWRITE_ZYR.md`
- `132` `skills/platform_zyr_skills/rewrites/runtime_rw_20260222_f28/by_source/spreadsheets/artifact_tool_spreadsheet_formulas_REWRITE_ZYR.md`
- `132` `skills/platform_zyr_skills/rewrites/runtime_rw_20260222_f28/by_source/spreadsheets/ex/create_spreadsheet_with_styling_REWRITE_ZYR.md`
- `131` `skills/platform_zyr_skills/rewrites/runtime_rw_20260222_f28/by_source/spreadsheets/ex/features/create_doughnut_chart_REWRITE_ZYR.md`
- `131` `skills/platform_zyr_skills/rewrites/runtime_rw_20260222_f28/by_source/spreadsheets/ex/features/set_cell_width_height_REWRITE_ZYR.md`
- `131` `skills/platform_zyr_skills/rewrites/runtime_rw_2_bfbad/by_source/spreadsheets/ex/features/set_conditional_formatting_REWRITE_ZYR.md`
- `131` `skills/platform_zyr_skills/rewrites/claude_code_runtime_rw_20260331_f15/by_source/non_goals_boundaries/bridgeEnabled_REWRITE_ZYR.md`
- `130` `skills/platform_zyr_skills/rewrites/claude_code_runtime_rw_20260331_f15/by_source/skills_plugins/loadPluginCommands_REWRITE_ZYR.md`
- `129` `skills/platform_zyr_skills/rewrites/runtime_rw_20260222_f28/by_source/spreadsheets/ex/features/change_exist_charts_REWRITE_ZYR.md`
- `129` `skills/platform_zyr_skills/rewrites/runtime_rw_20260222_f28/by_source/spreadsheets/ex/features/set_wrap_txt_styles_REWRITE_ZYR.md`
- `128` `skills/platform_zyr_skills/rewrites/runtime_rw_20260222_f28/by_source/spreadsheets/artifact_tool_spreadsheets_api_REWRITE_ZYR.md`
- `128` `skills/platform_zyr_skills/rewrites/runtime_rw_20260222_f28/by_source/spreadsheets/ex/features/set_number_formats_REWRITE_ZYR.md`
- `127` `skills/platform_zyr_skills/rewrites/runtime_rw_20260222_f28/by_source/spreadsheets/ex/features/create_area_chart_REWRITE_ZYR.md`
- `127` `skills/platform_zyr_skills/rewrites/runtime_rw_20260222_f28/by_source/spreadsheets/ex/features/create_line_chart_REWRITE_ZYR.md`
- `127` `skills/platform_zyr_skills/rewrites/runtime_rw_20260222_f28/by_source/spreadsheets/ex/features/set_txt_alignment_REWRITE_ZYR.md`
- `126` `skills/platform_zyr_skills/rewrites/runtime_rw_20260222_f28/by_source/spreadsheets/ex/features/create_bar_chart_REWRITE_ZYR.md`
- `126` `skills/platform_zyr_skills/rewrites/runtime_rw_20260222_f28/by_source/spreadsheets/ex/features/create_pie_chart_REWRITE_ZYR.md`
- `126` `skills/platform_zyr_skills/rewrites/runtime_rw_20260222_f28/by_source/spreadsheets/ex/features/set_cell_borders_REWRITE_ZYR.md`
- `126` `skills/platform_zyr_skills/rewrites/claude_code_runtime_rw_20260331_f15/by_source/skills_plugins/builtinPlugins_REWRITE_ZYR.md`
- `125` `skills/platform_zyr_skills/rewrites/runtime_rw_20260222_f28/by_source/spreadsheets/ex/create_basic_spreadsheet_REWRITE_ZYR.md`
