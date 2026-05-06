# ZIP-your-Research (ZYR) v1.6.2

**A chat-first, artifact-first research workflow system for GPT/Codex-style assistants.**

**Status:** repaired v1.6.2 release  
**Baseline:** v1.6.1 repaired package, extended with explicit high-efficiency task routing and prompt recipes  
**License:** MIT

ZIP-your-Research is a protocol-and-skills package for research conversations where evidence, file state, task boundaries, and final artifacts must remain explicit. It does not run unattended jobs by itself. It tells an assistant how to lock a task, route the work to the right engine or skill, verify claims, and preserve durable artifacts.

## Core execution logic

v1.6.2 keeps the original ZYR logic structure:

```text
ZIP upload or repository load
→ boot protocol
→ migration detection when needed
→ intake and task-boundary lock
→ MODE_LOCK
→ user CONFIRM
→ locked execution
→ router selects engine / skill stack
→ proof, writing, coding, figure, or validation workflow
→ artifact and completion report
```

The v1.6 layer is additive. It does not replace the boot/state-machine/proof/completion discipline from v1.5. It adds research-writing, figure-production, S340 style-and-logic review, and no-omission package validation as routable skills.

![ZIP-your-Research architecture](docs/assets/zyr_research_os_arch_v1_6.svg)

## Architecture planes

| Plane | Role | Main paths |
|---|---|---|
| Control plane | Boot rules, state machine, mode lock, routing, global guardrails | `boot/`, `router/` |
| Engine plane | Composite engines used for broad task execution | `skills/proof_engine/`, `skills/writing_engine/`, `skills/coding_engine/` |
| Workflow plane | Atomic research, experiment, paper, figure, and S340 skills | `skills/research_core/`, `skills/exp/`, `skills/paper_ops/`, `skills/rw/`, `skills/fig_ops/`, `skills/rwf_s340/` |
| Validation plane | Source preservation, path-length checks, checksums, release reports | `manifests/`, `tools/`, `artifacts/` |
| Preserved source plane | Integrated upstream sources retained as source references | `ext/src/` |

## If I need X, which ZYR engine should I control?

Use the table below as the explicit routing contract. In a chat, the user or operator can write: **“调用 ZYR 的 `<engine>`，并绑定 `<skills>`。”** The router may add companion skills, but it should not silently downgrade the requested route.

| If I need to do... | Control ZYR to call... | Required / typical bound skills | Purpose |
|---|---|---|---|
| Start a new research task or resume from a migration prompt | boot protocol + router | `boot/00_BOOTSTRAP_PROTOCOL_v1.3.2.md`, `boot/04_MODE_LOCK_FORMAT_v1.3.2.md` | Lock task boundary, artifact type, acceptance criteria, and execution mode before work starts. |
| Check whether a research idea, method, theorem, or explanation is logically valid | `proof_engine` | `skills/proof_engine/MASTER_v1.5.md`, usually `S203`, `S226`, `S227`, `S240`, `S241` | Run pessimistic and progressive verification; separate facts, assumptions, inference, and unsupported claims. |
| Write or restructure a paper section, research plan, proposal, README narrative, Introduction, Method, Results, or Discussion | `writing_engine` + `rwf_s340_master` | `S601` + `S640`; add `S602` if claims need reverse-outline review | Build the problem→gap→method→evidence chain before sentence polishing. |
| Perform reviewer-style critique, line-level logic audit, or claim-evidence check | `proof_engine` + `rwf_s340_master` | `S602` + `S640`; often add `S203`, `S226`, `S503` | Identify unsupported claims, broken causality, weak contribution framing, missing evidence, and wording risks. |
| Polish Chinese/English prose, compress/expand text, reduce AI tone, or produce delta-only rewrite | `writing_engine` | `S603` + mandatory `S640` | Improve language without erasing locked meaning, evidence boundaries, or user-specified style constraints. |
| Write result paragraphs, table captions, figure captions, or ablation narratives | `writing_engine` + RWF skills | `S604` + `S640`; add `S623` when a figure or visual claim is involved | Align numerical evidence, interpretation boundary, and caption/paragraph wording. |
| Design a publication-quality figure, architecture diagram, or scientific visualization | `rwf_s340_master` figure route | `S621` + `S623`; add `S622` for executable Matplotlib/SVG/PNG/PDF output | Start from the scientific claim, then choose layout, visual grammar, and caption boundary. |
| Generate or repair plotting code / SVG / PNG / PDF figure output | `coding_engine` + figure route | `S622` + `S621` + `S623`; add `S431` for closed-loop verification | Produce executable, minimal, verifiable figure code and check output consistency. |
| Debug code, patch scripts, fix runtime errors, or prepare release code | `coding_engine` | `skills/coding_engine/MASTER_v1.3.2.md`, usually `S402`, `S407`, `S421`, `S431`, `S432` | Diagnose first, patch minimally, verify in a closed loop, and report what changed. |
| Plan experiments, choose metrics, design ablations, or check experimental completeness | `proof_engine` + experiment skills | `S301`–`S328`, especially `S301`, `S303`, `S305`, `S307`, `S327`, `S328` | Convert claims into minimal decidable experiments; avoid blind grid search and unbounded tuning. |
| Build reproducible artifacts, package code/data, or audit open-source release readiness | `coding_engine` + reproducibility skills | `S407`, `S422`, `S424`, `S428`, `S431` | Package artifacts with environment, checksums, file inventory, and reproducibility notes. |
| Repair this ZYR package, check whether files were omitted, or validate ZIP/path-length safety | `S650` validation route | `skills/rwf_s340/S650_integrated_pack_no_omission_valid.md`, `tools/validate_no_omission.py`, `manifests/src_manifest.json` | Verify source preservation, path consistency, checksums, route smoke tests, and Windows-safe packaging. |
| Generate a migration prompt or append-only project handoff | boot migration + `proof_engine` | `boot/01_MIGRATION_PROMPT_TEMPLATE_v1.5.md`, `S203`, `S226`, `S650` when files are involved | Preserve project background, constraints, decisions, files, current state, unresolved issues, and next actions. |


## High-efficiency use protocol

The fastest way to use ZYR is not to write only “call ZYR”. The operator should state the task type, target artifact, evidence source, engine route, forbidden shortcuts, and validation gate in one prompt. The recommended compact control form is:

```text
Call ZYR v1.6.2 and execute under MODE_LOCK.
Task type: [paper audit / Word revision / code repair / experiment analysis / README rewrite / ZIP release validation / migration prompt].
Control engine / skills: [proof_engine / writing_engine / coding_engine / S640 / S650 / S601-S604 / S621-S623].
Input materials: [files, text, ZIP, figures, logs, tables, experiment outputs].
Target deliverable: [revised Word, Markdown report, runnable CLI, repaired ZIP, LaTeX, figure, migration prompt].
Hard constraints: [no deletion, no fabricated checks, preserve template, redline edits, no heuristic shortcut, JAX-only, etc.].
Final validation: report completed checks, failed checks, unverified items, and the next minimal action.
```

In Chinese workflows, the same contract can be written as:

```text
调用 ZYR v1.6.2，按 MODE_LOCK 执行，不跳过 routing 和 validation。
任务类型：[论文审查 / Word 修订 / 代码修复 / 实验分析 / README 重构 / ZIP 发版检查 / 迁移 prompt]。
指定 engine / skills：[proof_engine / writing_engine / coding_engine / S640 / S650 / S601-S604 / S621-S623]。
输入材料：[文件、文本、ZIP、图片、日志、实验表格]。
目标交付物：[修订版 Word / Markdown 报告 / 可运行 CLI / 修复后 ZIP / LaTeX / 图表 / 迁移 prompt]。
硬约束：[不得遗漏原文、不得虚构已检查内容、保留模板、红色标注、禁止拍脑袋式调参等]。
最后必须输出：已完成内容、判断依据、验证结果、未验证项、下一步最小动作。
```

### Recommended ready-to-use prompts

#### Paper logic audit

```text
Call ZYR v1.6.2. Task type: paper logic and language audit.
Control engine / skills: proof_engine + S602 + S640.
Goal: inspect problem formulation, method-selection rationale, section causality, claim-evidence alignment, redundant wording, and AI-like phrasing.
Requirements:
1. Be specific to page / paragraph / sentence when source location is available.
2. Separate fatal logic issues, fixable structure issues, and language issues.
3. Avoid generic advice.
4. Output replacement sentences or concrete revision operations.
```

Use this route for manuscripts, research plans, proposal drafts, and reviewer-readiness checks.

#### Word redline revision

```text
Call ZYR v1.6.2. Task type: Word source-document revision.
Control engine / skills: writing_engine + S640; use proof_engine after revision.
Requirements:
1. Preserve the original Word template, fonts, paragraph structure, numbering, and headings.
2. Mark every added or changed expression in red.
3. Do not rewrite the entire document unless explicitly requested.
4. Keep deletions minimal and explain why each major deletion was made.
5. Output the revised Word document and a revision report.
6. Run a final logic check and report unresolved risks.
```

Use this route for reviewer revisions, recommendation letters, project applications, and formal institutional documents.

#### Research plan or manuscript restructuring

```text
Call ZYR v1.6.2. Task type: research-plan or manuscript restructuring.
Control engine / skills: writing_engine + proof_engine + S601 + S602 + S640.
Goal: restructure the problem setting, literature basis, method causality, section order, and contribution framing.
Requirements:
1. First judge whether the current research line is logically viable.
2. Identify unsupported transitions, vague contrasts, and suspended claims.
3. For every method design, explain why it answers the preceding problem.
4. Avoid slogan-like prose and mechanical parallel phrasing.
5. Output the revised draft and a change-by-change explanation.
```

Use this route when the document needs conceptual repair, not only sentence polishing.

#### Code repair or repository cleanup

```text
Call ZYR v1.6.2. Task type: code repair and release cleanup.
Control engine / skills: coding_engine + S650.
Goal: make the smallest necessary changes without changing algorithmic logic unless explicitly requested.
Requirements:
1. Diagnose the first real failure before patching.
2. List every modified file.
3. State which files were deleted, retained, renamed, or ignored.
4. Provide copy-paste runnable CLI when local execution is needed.
5. Run closed-loop verification when execution is possible.
6. Report passed checks, failed checks, and unverified items.
```

Use this route for public GitHub release, package cleanup, script repair, and runtime bug fixing.

#### Experiment result analysis

```text
Call ZYR v1.6.2. Task type: experiment result analysis.
Control engine / skills: experiment workflow + proof_engine + S602.
Goal: determine whether the data support the current paper claims.
Requirements:
1. Do not omit any table, seed, metric, or critical field.
2. Separate observed facts, inference, and claims that remain unsupported.
3. Check counterexamples, seed instability, reporting bias, and metric mismatch.
4. Output a claim-evidence matrix.
5. State whether the paper narrative should be retained, narrowed, or rewritten.
```

Use this route for offline RL, long-horizon control, ablations, W&B exports, benchmark tables, and failure-case analysis.

#### README / ZIP release validation

```text
Call ZYR v1.6.2. Task type: README and ZIP release validation.
Control engine / skills: S650 + coding_engine + writing_engine.
Goal: check whether the package is complete, paths are consistent, README routes tasks to the correct engines, and release artifacts are usable.
Requirements:
1. Verify manifest, checksums, path length, README route table, and smoke-test commands.
2. Detect stale paths, legacy names, broken references, and omitted files.
3. Repair only necessary files.
4. Repackage the ZIP.
5. Output the repaired ZIP, repair report, validation results, and unresolved risks.
```

Use this route before sending a ZYR release, GitHub package, public codebase, or collaborator handoff.

#### Migration prompt or append-only project handoff

```text
Call ZYR v1.6.2. Task type: migration prompt / append-only handoff.
Control engine / skills: boot migration workflow + proof_engine; add S650 when file paths or ZIP packages are involved.
Goal: preserve project background, key decisions, current files, locked constraints, status, unresolved questions, and next executable actions.
Requirements:
1. Do not replace prior content with a short summary when the user asked for lossless migration.
2. Preserve file paths, command-line context, important negative results, and current state.
3. Mark confirmed facts, reasonable inference, and unverified items.
4. Use English for the final migration prompt unless the user explicitly requests otherwise.
5. Append changelog entries instead of silently overwriting project history.
```

Use this route when a new conversation must continue a project without losing constraints or execution state.

### Low-efficiency vs high-efficiency invocation

Avoid ambiguous prompts such as:

```text
Call ZYR and optimize this.
Call ZYR and review it.
Call ZYR and analyze deeply.
```

Prefer route-bound prompts such as:

```text
Call ZYR v1.6.2. Task type: paper logic audit.
Control engine / skills: proof_engine + S602 + S640.
Focus: claim-evidence alignment, method-selection rationale, and section causality.
Deliverable: line-level issues, concrete replacements, and final verification report.
```

A route-bound prompt lets the assistant select the correct validation path immediately, reduces back-and-forth clarification, and prevents writing-only polishing from replacing proof, code, experiment, or release validation work.

## Mandatory routing rules

For visible writing tasks, `S640` is a hard gate. It must be applied before final prose is accepted. It checks unsupported claims, vague transitions, inflated language, mechanical contrasts, and forbidden/high-risk phrase patterns recorded in:

```text
skills/rwf_s340/req_AND_forbid_phr.md
```

For package repair or release validation tasks, `S650` is the required validation gate:

```text
skills/rwf_s340/S650_integrated_pack_no_omission_valid.md
```

For code modification tasks, `coding_engine` must be paired with closed-loop verification when execution is possible:

```text
skills/coding_engine/MASTER_v1.3.2.md
skills/reproducibility/S431_closed_loop_verification.md
```

For proof, theorem, derivation, claim, or method-correctness tasks, `proof_engine` is the primary engine:

```text
skills/proof_engine/MASTER_v1.5.md
```

## Repository map

```text
boot/                         bootstrap, migration, intake, mode lock, locked execution
router/                       deterministic routing and v1.6 route addenda
router/ext_router/            integrated research-writing-figure/S340 router addenda
skills/                       atomic and composite ZYR skills
skills/proof_engine/          proof, derivation, claim, and logic verification engine
skills/writing_engine/        manuscript and prose rewriting engine
skills/coding_engine/         debugging, patching, and code-verification engine
skills/research_core/         problem framing, novelty, claim-evidence, method audit
skills/exp/                   experiment design, metrics, ablations, sanity checks
skills/paper_ops/             submission, rebuttal, captions, appendices, open-source notes
skills/rw/                    paper-writing wrappers from the integrated stack
skills/fig_ops/               scientific-figure wrappers from the integrated stack
skills/master_integrated/     integrated research-writing-figure entry point
skills/rwf_s340/              v1.6 S601-S604, S621-S623, S640, S650 integrated skills
ext/src/                      preserved source trees for integrated external materials
manifests/                    source inventories, route tests, checksums, release audits
tools/                        validators, builders, simulators, and packaging scripts
artifacts/                    durable execution and verification artifacts
```

## v1.6.2 README usage extension

This release keeps the v1.6.1 repaired package layout and adds a clearer operator-facing usage layer to `README.md`. The intended usage contract is now explicit: for each task, the user should specify what they need to do and which ZYR engine or skill stack must be invoked. This reduces route ambiguity and prevents a writing-only response from replacing proof, code, experiment, figure, or package-validation work.

| Added README layer | Function |
|---|---|
| High-efficiency use protocol | Defines the compact prompt structure: task type, engine route, inputs, deliverable, hard constraints, and validation gate. |
| Bilingual invocation template | Provides both English and Chinese route-bound prompt formats. |
| Ready-to-use prompt recipes | Covers paper audit, Word redline revision, research-plan restructuring, code cleanup, experiment analysis, README/ZIP validation, and migration handoff. |
| Low-efficiency warning | Explicitly discourages vague prompts such as “call ZYR and optimize this” without engine binding. |

## v1.6.1 repair scope

This release repairs the v1.6.0 Windows-safe package without changing the core execution model.

| Area | v1.6.0 issue | v1.6.1 repair |
|---|---|---|
| README architecture | Mixed old long paths and new short paths | Rewritten around actual paths and explicit task→engine routing table. |
| Source paths | `external_sources/` and `external_skills/original_sources/` references remained after short-path packaging | Standardized to `ext/src/`. |
| Writing/figure paths | `skills/research_writing/`, `skills/figure_ops/`, `skills/integrated_master/` references remained | Standardized to `skills/rw/`, `skills/fig_ops/`, `skills/master_integrated/`. |
| Router addenda | `router/integrated_extensions/` references remained | Standardized to `router/ext_router/`. |
| Manifests | `SOURCE_MANIFEST.json` and `SOURCE_FILE_INTEGRATION_TABLE.md` references remained | Standardized to `manifests/src_manifest.json` and `manifests/src_FILE_integr_TABLE.md`. |
| S340 requirement file | Long filename references remained | Standardized to `skills/rwf_s340/req_AND_forbid_phr.md`. |
| No-omission validator | Script looked for the old manifest filename | Updated to read `manifests/src_manifest.json`. |
| Skill manifest | Several entries pointed to renamed files | Reconciled against actual files under `skills/`. |
| Checksums/path report | Old package checksums and path report did not reflect the repaired state | Regenerated after repair. |

## Quick start

### ZIP-only chat boot

1. Upload the repository ZIP to a fresh chat.
2. If resuming existing work, paste a migration prompt in English.
3. Otherwise send `start`.
4. Complete intake.
5. Review the generated `MODE_LOCK`.
6. Reply `CONFIRM` to enter locked execution.

Key entry points:

```text
boot/00_BOOTSTRAP_PROTOCOL_v1.3.2.md
boot/04_MODE_LOCK_FORMAT_v1.3.2.md
boot/13_SCIENTIFIC_ASSISTANT_OUTPUT_DISCIPLINE_v1.5.md
```

### Direct engine use

For narrower workflows, paste or reference the relevant engine directly:

```text
skills/proof_engine/MASTER_v1.5.md
skills/writing_engine/MASTER_v1.3.2.md
skills/coding_engine/MASTER_v1.3.2.md
skills/rwf_s340/MASTER.md
skills/master_integrated/MASTER_research_write_fig_stack_v1.0.md
```

## Integrated sources and attribution

v1.6.2 preserves integrated source materials under `ext/src/` and uses ZYR-native wrappers for routing.

- `ext/src/rpws/`: research-paper writing source materials.
- `ext/src/awesome/`: academic writing prompt collections and examples.
- `ext/src/figures/`: scientific figure-making references, demos, scripts, and assets.
- `ext/src/S340_v4.2_theory_global_skill_bundle/`: user-authored S340 style-and-logic ruleset.

See `docs/EXTERNAL_SKILL_ATTRIBUTION_v1.6.md` for attribution details and integration boundaries.

## Validation

Run from the repository root:

```bash
python3 tools/validate_no_omission.py
python3 router/route.py "论文润色 S340 逻辑审查"
python3 router/route.py "matplotlib figure svg png"
python3 router/route.py "压缩包 文件遗漏 checksum path length"
```

The release package also includes:

```text
manifests/src_manifest.json
manifests/src_FILE_integr_TABLE.md
manifests/CHECKSUMS.sha256
manifests/PATH_LENGTH_REPORT.md
manifests/REPAIR_AUDIT_v1.6.1.md
```

## Safety and honesty rules

ZYR treats the following as non-negotiable:

- do not fabricate facts, citations, file states, execution status, or experimental results;
- do not report unexecuted checks as completed;
- do not hide uncertainty inside polished prose;
- do not reduce research problems to unsupported heuristic tuning;
- do not simplify or split locked work without explicit approval;
- do not accept visible writing output before the relevant S640 checks are satisfied;
- do not call a package repaired until path references, manifests, and validation scripts point to real files.

## Maintainer

See `docs/ABOUT_MAINTAINER.md`.
