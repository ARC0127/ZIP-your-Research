# ZIP-your-Research (ZYR) v1.6.3

**ZIP-your-Research (ZYR)** is a repository-first research workflow system for GPT/Codex-style assistants. It provides a task-locking protocol, a deterministic routing layer, and a set of evidence-aware research skills so that complex research work can be continued, audited, revised, and packaged without losing task boundaries or file-state assumptions.

ZYR is not an autonomous job runner. It is a control and verification layer: it tells an assistant how to identify the task, select the correct engine, preserve evidence, execute the work, and report what has or has not been verified.

## Design intent

ZYR is designed for research conversations where correctness matters more than fluent surface completion. It is especially useful for:

- manuscript and proposal revision;
- claim-evidence and reviewer-style audits;
- code repair and reproducibility checks;
- experiment planning and result interpretation;
- publication-quality figure workflows;
- release packaging and migration handoff.

The core rule is simple: **lock the task before executing it, route the task to the correct engine, and verify the resulting artifact before accepting it.**

## Execution model

A standard ZYR session follows the sequence below:

```text
repository or ZIP loaded
→ bootstrap protocol
→ migration detection if applicable
→ intake and task-boundary lock
→ MODE_LOCK
→ explicit CONFIRM when required
→ locked execution
→ router selects engine / skill stack
→ proof, writing, coding, experiment, figure, or release workflow
→ artifact output and validation report
```

The v1.6 line keeps the earlier ZYR state-machine and completion discipline. The v1.6.3 release makes the integrated writing/figure/S340 layer CI-clean, removes duplicate skill IDs, and formalizes the README and contribution rules.

## Architecture

| Plane | Purpose | Canonical paths |
|---|---|---|
| Control plane | Bootstrap, migration, intake, mode lock, locked execution, global guardrails | `boot/`, `router/` |
| Engine plane | Composite execution engines for broad task families | `skills/proof_engine/`, `skills/writing_engine/`, `skills/coding_engine/` |
| Skill plane | Atomic research, experiment, paper, reproducibility, and integrated S340 skills | `skills/research_core/`, `skills/exp/`, `skills/paper_ops/`, `skills/reproducibility/`, `skills/rwf_s340/` |
| Source-preservation plane | Upstream and user-authored source materials retained for attribution and reference | `ext/src/` |
| Validation plane | Manifests, checksums, path reports, validators, release audits | `manifests/`, `tools/`, `artifacts/` |

The canonical integrated v1.6 skills live under `skills/rwf_s340/`. The earlier duplicate wrapper files under `skills/rw/` and `skills/fig_ops/` were removed because strict validation requires one unique file per skill ID.

## Task-to-engine routing

Use this table when giving ZYR instructions. A high-quality prompt should specify what needs to be done and which engine or skill stack should be used.

| Task | Control ZYR to call | Required or typical skills | Expected outcome |
|---|---|---|---|
| Start a new task or resume a migrated task | Bootstrap + router | `boot/00_BOOTSTRAP_PROTOCOL_v1.3.2.md`, `boot/04_MODE_LOCK_FORMAT_v1.3.2.md` | Locked task boundary, artifact type, acceptance criteria, and execution mode |
| Verify a research idea, theorem, method, or explanation | `proof_engine` | `skills/proof_engine/MASTER_v1.5.md`, often `S203`, `S226`, `S227`, `S240`, `S241` | Fact/assumption/inference separation, contradiction checks, unsupported-claim report |
| Write or restructure a manuscript section, proposal, research plan, or README narrative | `writing_engine` + integrated S340 route | `S601` + mandatory `S640`; add `S602` for claim-evidence review | Problem-gap-method-evidence structure before sentence-level polishing |
| Conduct reviewer-style critique or line-level logic audit | `proof_engine` + integrated S340 route | `S602` + mandatory `S640`; often `S203`, `S226`, `S503` | Unsupported claims, weak causal links, missing evidence, and concrete revision actions |
| Polish Chinese/English prose, compress text, expand text, translate, or reduce AI-like tone | `writing_engine` | `S603` + mandatory `S640` | Delta-aware revision that preserves locked facts, formulas, citations, and numbers |
| Write result paragraphs, figure captions, table captions, or ablation narratives | `writing_engine` + integrated result route | `S604` + `S640`; add `S623` for visual claims | Evidence-bounded result narrative with correct metric direction and caption scope |
| Design a scientific figure or architecture diagram | Integrated figure route | `S621` + `S623`; add `S622` for executable plotting | Claim-driven layout, panel semantics, caption plan, and visual risk check |
| Generate or repair Matplotlib/SVG/PNG/PDF figure output | `coding_engine` + figure route | `S622` + `S621` + `S623`; add `S431` when execution is possible | Minimal executable plotting code and inspected figure output when possible |
| Debug code, patch scripts, or prepare release code | `coding_engine` | `skills/coding_engine/MASTER_v1.3.2.md`, often `S402`, `S407`, `S421`, `S431`, `S432` | Minimal patch, changed-file list, runnable commands, and closed-loop verification |
| Plan experiments, select metrics, design ablations, or check experimental completeness | `proof_engine` + experiment skills | `S301`-`S328`, especially `S301`, `S303`, `S305`, `S307`, `S327`, `S328` | Minimal decidable experiment design and claim-evidence alignment |
| Package artifacts, audit reproducibility, or prepare an open-source release | `coding_engine` + reproducibility skills | `S407`, `S422`, `S424`, `S428`, `S431` | Reproducible artifact bundle with inventory, environment, checksums, and release notes |
| Repair this ZYR package or validate ZIP/source completeness | `S650` validation route | `S650`, `tools/validate_no_omission.py`, `tools/validate_v7_2.py`, `tools/drift_audit_v1_3.py` | Duplicate/path/reference/manifest validation and release-ready ZIP |
| Generate a migration prompt or append-only handoff | Migration workflow + `proof_engine` | `boot/01_MIGRATION_PROMPT_TEMPLATE_v1.5.md`, `S203`, `S226`; add `S650` for files | Loss-minimizing project state transfer with files, decisions, constraints, blockers, and next actions |

## Efficient invocation pattern

Do not use vague instructions such as “call ZYR and optimize this.” Instead, bind the task to a route:

```text
Call ZYR v1.6.3 and execute under MODE_LOCK.
Task type: [paper audit / Word revision / code repair / experiment analysis / README rewrite / ZIP validation / migration prompt].
Control engine / skills: [proof_engine / writing_engine / coding_engine / S640 / S650 / S601-S604 / S621-S623].
Input materials: [files, text, ZIP, figures, logs, tables, experiment outputs].
Target deliverable: [revised Word, Markdown report, runnable CLI, repaired ZIP, LaTeX, figure, migration prompt].
Hard constraints: [preserve template, redline edits, no fabricated checks, no unsupported claims, no blind hyperparameter search, etc.].
Final validation: report passed checks, failed checks, unverified items, and the next minimal action.
```

For Chinese workflows, the same contract can be written as:

```text
调用 ZYR v1.6.3，按 MODE_LOCK 执行，不跳过 routing 和 validation。
任务类型：[论文审查 / Word 修订 / 代码修复 / 实验分析 / README 重构 / ZIP 发版检查 / 迁移 prompt]。
指定 engine / skills：[proof_engine / writing_engine / coding_engine / S640 / S650 / S601-S604 / S621-S623]。
输入材料：[文件、文本、ZIP、图片、日志、实验表格]。
目标交付物：[修订版 Word / Markdown 报告 / 可运行 CLI / 修复后 ZIP / LaTeX / 图表 / 迁移 prompt]。
硬约束：[不得遗漏原文、不得虚构已检查内容、保留模板、红色标注、禁止拍脑袋式调参等]。
最后必须输出：已完成内容、判断依据、验证结果、未验证项、下一步最小动作。
```

## Canonical usage recipes

### Paper logic audit

```text
Call ZYR v1.6.3. Task type: paper logic and language audit.
Control engine / skills: proof_engine + S602 + S640.
Focus: problem formulation, method-selection rationale, section causality, claim-evidence alignment, redundant wording, and AI-like phrasing.
Deliverable: line-level issues, concrete replacements, and final verification report.
```

### Word redline revision

```text
Call ZYR v1.6.3. Task type: Word source-document revision.
Control engine / skills: writing_engine + S640; use proof_engine after revision.
Constraints: preserve template, font, numbering, headings, and paragraph structure; mark additions or changed expressions in red; output the revised Word file and revision report.
```

### Code repair or repository cleanup

```text
Call ZYR v1.6.3. Task type: code repair and release cleanup.
Control engine / skills: coding_engine + S650.
Constraints: diagnose the first real failure before patching; make the smallest necessary change; list modified/deleted files; run closed-loop validation when possible.
```

### Experiment result analysis

```text
Call ZYR v1.6.3. Task type: experiment result analysis.
Control engine / skills: experiment workflow + proof_engine + S602.
Constraints: do not omit seeds, tables, metrics, or failure cases; separate facts, inference, and unsupported claims; output a claim-evidence matrix.
```

### README or ZIP release validation

```text
Call ZYR v1.6.3. Task type: README and ZIP release validation.
Control engine / skills: S650 + coding_engine + writing_engine.
Constraints: check duplicate skill IDs, stale paths, manifests, checksums, path length, README route table, and CI commands; repackage only after validation passes.
```

## Installation and validation

Install the only runtime dependency used by the validators:

```bash
python -m pip install -r requirements.txt
```

Run the standard CI-equivalent validation from the repository root:

```bash
python tools/cleanup_legacy_duplicate_paths_v1_6_3.py
python tools/build_all.py
python tools/validate_v7_2.py
python tools/drift_audit_v1_3.py
```

Run the integrated package checks when validating a release ZIP or source-preservation update:

```bash
python tools/validate_no_omission.py
python tools/validate_integrated_sources.py
python router/route.py "paper writing S340 logic audit"
python router/route.py "matplotlib publication figure svg png"
python router/route.py "ZIP release no omission checksum path length"
```

If you are upgrading an existing Git checkout by copying files from a release ZIP, run the cleanup command before validation. It removes stale aliases such as `skills/experiments/` and older long-name skill files that can otherwise create duplicate skill IDs.

## Repository map

```text
boot/                         bootstrap, migration, intake, mode lock, locked execution
router/                       deterministic routing and route addenda
router/ext_router/            integrated research-writing/figure/S340 routing notes
skills/proof_engine/          proof, derivation, claim, and logic verification engine
skills/writing_engine/        manuscript and prose rewriting engine
skills/coding_engine/         debugging, patching, and code-verification engine
skills/research_core/         research framing, novelty, literature, and method checks
skills/exp/                   experiment design, metrics, ablations, and sanity checks
skills/paper_ops/             paper operations, rebuttal, captions, and release notes
skills/reproducibility/       artifacts, dependency, security, and verification skills
skills/rwf_s340/              canonical v1.6 integrated S601-S604, S621-S623, S640, S650 skills
ext/src/                      preserved upstream and user-authored source materials
manifests/                    source inventories, checksums, path reports, and release audits
tools/                        validators, builders, cleanup scripts, and packaging utilities
artifacts/                    durable task, evidence, proof, and release artifacts
```

## Integrated sources and attribution

The v1.6 line preserves integrated source materials under `ext/src/` and exposes them through ZYR-native wrapper skills under `skills/rwf_s340/`.

- `ext/src/rpws/`: research-paper writing source materials.
- `ext/src/awesome/`: academic writing prompt collections and examples.
- `ext/src/figures/`: scientific figure-making references, demos, scripts, and assets.
- `ext/src/S340_v4.2_theory_global_skill_bundle/`: maintainer-authored S340 style-and-logic ruleset.

See `docs/EXTERNAL_SKILL_ATTRIBUTION_v1.6.md` for attribution details and integration boundaries.

## Safety and acceptance rules

ZYR treats the following as mandatory:

- do not fabricate facts, citations, file states, command results, or experimental outcomes;
- do not report an unexecuted check as completed;
- do not hide uncertainty inside polished prose;
- do not reduce research problems to unsupported heuristic tuning;
- do not accept writing output before the relevant S640 checks are satisfied;
- do not call a package repaired until duplicate IDs, path references, manifests, and validation scripts have been checked.

## Maintainer and license

Maintainer information is available in `docs/ABOUT_MAINTAINER.md`. This repository is released under the MIT License.
