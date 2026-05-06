# ZIP-your-Research (ZYR) v1.6.5

**ZIP-your-Research (ZYR)** is a repository-first research workflow system for GPT/Codex-style assistants. It is designed for long-running research tasks where correctness depends on preserving task boundaries, evidence, file state, and final artifacts across repeated revisions.

ZYR is not a generic prompt collection and it is not an autonomous job runner. It is a control-and-verification layer: it locks the task, routes it to the correct engine, preserves source materials, executes through explicit skills, and reports what has or has not been verified.

## Core workflow

```text
repository or ZIP loaded
→ bootstrap protocol
→ migration detection when needed
→ intake and task-boundary lock
→ MODE_LOCK
→ explicit CONFIRM when required
→ locked execution
→ router selects engine / skill stack
→ proof, writing, figure, coding, experiment, or release workflow
→ artifact output
→ validation report
```

The central rule is:

```text
lock the task
→ route to the correct engine
→ execute against preserved sources
→ verify before accepting the artifact
```

## Mandatory engine bindings

Engine binding is the most important v1.6.5 rule. A task should not be handled by generic chat behavior when a dedicated engine applies.

### 1. Research idea, method, contribution, or paper-storyline tasks

Use **`proof_engine`** before prose polishing when the task involves research logic rather than surface writing.

```text
idea / method / storyline task
→ proof_engine
→ S203 claim_evidence_matrix
→ S226 logic_consistency_audit
→ S227 method_correctness_audit
→ S230 proof_idea_check
→ S237 theorem_assumption_normalizer when assumptions matter
→ S240 / S241 for pessimistic or progressive verification
→ writing_engine only after the logic is stable
```

Use this route for:
- research idea construction;
- method design and method-rationale checking;
- theoretical framing and assumption analysis;
- contribution definition;
- paper storyline construction;
- theorem, proof sketch, derivation, or claim-evidence verification.

### 2. Writing, rewriting, polishing, and document prose tasks

Use **`writing_engine`** for visible writing. The writing engine is backed by the preserved Research-Paper-Writing-Skills source tree.

```text
writing task
→ writing_engine
→ ext/src/rpws/  # Research-Paper-Writing-Skills
→ S601 / S602 / S603 / S604 as needed
→ S640 global writing and logic gate
```

Use this route for:
- manuscript sections, proposals, recommendation letters, CV project descriptions, README prose, and rebuttals;
- rewriting, polishing, compression, expansion, translation, and anti-AI-tone editing;
- result paragraphs, table captions, figure captions, and reviewer-facing edits.

If the prose depends on an unstable idea, method, contribution, or claim-evidence chain, run `proof_engine` first.

### 3. Figure, plotting, diagram, and visual-claim tasks

Use **`figure_engine`** for figure-making. The figure engine is backed by the preserved figures4papers source tree.

```text
figure task
→ figure_engine
→ inspect ext/src/figures/ first  # figures4papers
→ S621 / S622 / S623 as needed
→ coding_engine only when execution or code repair is required
```

Hard figure constraints:
- inspect `ext/src/figures/` before drawing;
- do not start from scratch when a close figures4papers pattern exists;
- preserve source-code-first generation;
- do not replace CSV, table, dataframe, or structured input logic with ad hoc hard-coded arrays unless the data source is intentionally changed and documented;
- treat SVG, PNG, and PDF as export formats, not as substitutes for generating source.

### 4. Code, repository, and release tasks

Use **`coding_engine`** for code repair and repository changes.

```text
code / repository task
→ coding_engine
→ smallest sufficient patch
→ closed-loop verification
→ S650 when packaging or release validation is involved
```

Use **`S650`** for integrated ZIP/package validation, source preservation, manifest checks, checksums, and no-omission release review.

## Architecture

| Layer | Purpose | Main paths |
|---|---|---|
| Control layer | Bootstrap, migration detection, intake, mode lock, locked execution, global guardrails | `boot/`, `router/` |
| Engine layer | Composite execution engines for broad task families | `skills/proof_engine/`, `skills/writing_engine/`, `skills/figure_engine/`, `skills/coding_engine/` |
| Skill layer | Atomic research, experiment, paper-operation, reproducibility, and integrated S6xx skills | `skills/research_core/`, `skills/exp/`, `skills/paper_ops/`, `skills/reproducibility/`, `skills/rwf_s340/` |
| Source-preservation layer | External and user-authored sources retained for attribution and reuse | `ext/src/` |
| Validation layer | Manifests, checksums, route smoke tests, package audits, and validators | `manifests/`, `tools/`, `artifacts/` |

## If I need X, which engine should I control?

| Task | Primary route | Mandatory companion |
|---|---|---|
| Research idea, method design, contribution framing, paper storyline | `proof_engine` | `S203`, `S226`, `S227`, `S230`; add `S237/S240/S241` when assumptions or proofs matter |
| Manuscript logic audit or reviewer-style critique | `proof_engine` + `writing_engine` | `S602` + `S640` |
| Paper section, proposal, README, recommendation letter | `writing_engine` | `ext/src/rpws/` + `S601` + `S640`; add `proof_engine` if logic is still being formed |
| Rewrite, polish, compress, expand, translate, or reduce AI-like tone | `writing_engine` | `S603` + `S640` |
| Result paragraph, table caption, figure caption, ablation narrative | `writing_engine` | `S604` + `S640`; add `S623` for visual-evidence consistency |
| Scientific figure, workflow diagram, architecture diagram | `figure_engine` | inspect `ext/src/figures/` first; use `S621` + `S623` |
| Plotting code, figure export, figure repair | `figure_engine` + `coding_engine` | `S622` + `S621` + `S623`; keep source-generation logic |
| Experiment design, metric choice, ablation plan | `proof_engine` + experiment skills | `S301`-`S328`, especially `S301`, `S303`, `S305`, `S307`, `S327`, `S328` |
| Code repair, CI failure, repository cleanup | `coding_engine` | `S402`, `S407`, `S421`, `S431`, `S432` |
| ZIP, release, manifest, checksum, path-length, no-omission validation | `S650` | `tools/validate_no_omission.py`, `tools/validate_integrated_sources.py`, `tools/validate_v7_2.py` |
| Migration prompt or append-only handoff | migration workflow + `proof_engine` | `boot/01_MIGRATION_PROMPT_TEMPLATE_v1.5.md`; add `S650` when files are involved |

## Efficient invocation template

```text
Call ZYR v1.6.5 and execute under MODE_LOCK.
Task type: [idea construction / method design / paper audit / Word revision / code repair / experiment analysis / README rewrite / ZIP validation / migration prompt / figure generation].
Control engine / skills: [proof_engine / writing_engine / figure_engine / coding_engine / S203 / S226 / S227 / S230 / S237 / S240 / S241 / S601-S604 / S621-S623 / S640 / S650].
Input materials: [files, text, ZIP, figures, logs, tables, experiment outputs].
Target deliverable: [revised Word, Markdown report, runnable CLI, repaired ZIP, LaTeX, figure, migration prompt].
Hard constraints: [preserve template, redline edits, no fabricated checks, no unsupported claims, preserve figures4papers data-loading logic, etc.].
Final validation: report passed checks, failed checks, unverified items, and the next minimal action.
```

## Installation and validation

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Standard validation:

```bash
python tools/cleanup_legacy_duplicate_paths_v1_6_5.py
python tools/build_all.py
python tools/validate_v7_2.py
python tools/drift_audit_v1_3.py
```

Integrated source and release validation:

```bash
python tools/validate_no_omission.py
python tools/validate_integrated_sources.py
python router/route.py "research idea method design contribution proof audit"
python router/route.py "paper writing RPWS S340 logic audit"
python router/route.py "figure engine figures4papers plotting code png pdf"
python router/route.py "ZIP release no omission checksum path length"
```

## Repository map

```text
boot/                         bootstrap, migration, intake, mode lock, locked execution
router/                       deterministic routing and route addenda
router/ext_router/            integrated proof, writing, figure, and S340 routing notes
skills/proof_engine/          idea, theorem, derivation, claim, and logic-verification engine
skills/writing_engine/        RPWS-backed manuscript and prose-rewriting engine
skills/figure_engine/         figures4papers-backed figure engine
skills/coding_engine/         debugging, patching, and code-verification engine
skills/research_core/         research framing, novelty, literature, and method checks
skills/exp/                   experiment design, metrics, ablations, and sanity checks
skills/paper_ops/             paper operations, rebuttal, captions, and release notes
skills/reproducibility/       artifacts, dependency, security, and verification skills
skills/rwf_s340/              integrated S601-S604, S621-S623, S640, and S650 workflows
ext/src/                      preserved upstream and user-authored source materials
manifests/                    source inventories, checksums, path reports, and release audits
tools/                        validators, builders, cleanup scripts, and packaging utilities
artifacts/                    durable task, evidence, proof, and release artifacts
docs/how_to_use/              concise operational guides for engine-bound use
```

## Acknowledgments and references

ZYR is open work. Its design was shaped by public research systems, proof-verification papers, open learning materials, and open-source writing/figure-making repositories. These works informed the system; they are not claimed here as original ZYR inventions.

Architecture and control-plane references include [Google AI co-scientist](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/), [OpenAI deep research](https://openai.com/index/introducing-deep-research/), [A Vision for Auto Research with LLM Agents](https://arxiv.org/abs/2504.18765), [PiFlow](https://arxiv.org/abs/2505.15047), [AI-Researcher](https://arxiv.org/abs/2505.18705), [ResearStudio](https://arxiv.org/abs/2510.12194), [FS-Researcher](https://arxiv.org/abs/2602.01566), [OR-Agent](https://arxiv.org/abs/2602.13769), [EvoScientist](https://arxiv.org/abs/2603.08127), [ResearchPilot](https://arxiv.org/abs/2603.14629), [AI-Supervisor](https://arxiv.org/abs/2603.24402), and the public-description source for [FARS](https://www.thepaper.cn/newsDetail_forward_32600597).

Proof and theory references include [Pessimistic Verification for Open-Ended Math Questions](https://arxiv.org/abs/2511.21522), [Hard2Verify](https://arxiv.org/abs/2510.13744), [Scaling Flaws of Verifier-Guided Search in Mathematical Reasoning](https://arxiv.org/abs/2502.00271), [Improving Value-based Process Verifier via Low-Cost Variance Reduction](https://arxiv.org/abs/2508.10539), [Asking LLMs to Verify First is Almost Free Lunch](https://arxiv.org/abs/2511.21734), [AI Mathematician](https://arxiv.org/abs/2505.22451), [StepProof](https://arxiv.org/abs/2506.10558), [Goedel-Prover](https://arxiv.org/abs/2502.07640), [Goedel-Prover-V2](https://arxiv.org/abs/2508.03613), [Leanabell-Prover-V2](https://arxiv.org/abs/2507.08649), and [APOLLO](https://arxiv.org/abs/2505.05758).

Open learning and community references include [Hello-Agents (Datawhale)](https://github.com/datawhalechina/hello-agent).

The v1.6 writing and figure workflows integrate and preserve the following external sources with attribution:

- [Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills), preserved under `ext/src/rpws/`, for paper structure, section guides, and claim-evidence writing discipline.
- [Prof. Peng Sida's open research notes](https://github.com/pengsida/learning_research), acknowledged through the upstream attribution of Research-Paper-Writing-Skills.
- [awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing), preserved under `ext/src/awesome/`, for academic-writing prompts, bilingual rewriting patterns, and logic-checking examples.
- [figures4papers](https://github.com/ChenLiu-1996/figures4papers), preserved under `ext/src/figures/`, for scientific figure-design principles, plotting scripts, demonstrations, and reusable figure-generation patterns.

For detailed attribution and integration boundaries, see:

- `docs/ATTRIBUTION.md`
- `docs/EXTERNAL_SKILL_ATTRIBUTION_v1.6.md`
- `docs/integrated_external_skills/README_integrated_stack_v1.0.md`
- `research/auto_research_inventory.md`
- `research/engineering_alignment_matrix.md`
- `research/fars_deep_dive.md`
- `research/pessimistic_verification_lineage.md`
