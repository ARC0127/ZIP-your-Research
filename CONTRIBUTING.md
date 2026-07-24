# Contributing to ZIP-your-Research

Thank you for improving ZIP-your-Research (ZYR). Contributions are welcome when they preserve the repository's central purpose: task-boundary discipline, evidence-aware execution, and verifiable research artifacts.

This document defines the contribution rules for the v1.6.6 line.

## Contribution principles

A contribution is acceptable only if it preserves the following invariants:

1. **One skill ID maps to one canonical routable skill file.** Do not add alias files with the same `S###` identifier.
2. **Evidence boundaries must remain explicit.** New prompts or skills must not encourage unsupported claims, fabricated verification, or hidden uncertainty.
3. **Canonical short paths remain authoritative.** Use `skills/exp/`, `skills/rwf_s340/`, `ext/src/`, `router/ext_router/`, and the current manifest filenames.
4. **Builders and validators must pass.** A change is not complete until the repository builds and strict validation succeeds.
5. **Historical material may be retained for attribution, but not as duplicate routable skills.** If a source is preserved, place it under `ext/src/` or a clearly non-routable reference path.
6. **Idea, method, and research-logic tasks must remain bound to `proof_engine`.** Do not add a research-construction workflow that bypasses `proof_engine`, the claim-evidence matrix, or logic/method correctness checks.
7. **Writing tasks must remain bound to `writing_engine`.** Do not add a writing-facing workflow that bypasses `writing_engine`, `ext/src/rpws/`, and the integrated S601-S604 + S640 chain.
8. **Figure tasks must remain bound to `figure_engine`.** Do not add a figure-facing workflow that bypasses `figure_engine`, `ext/src/figures/`, and the integrated S621-S623 chain.

## What to contribute

Appropriate contributions include:

- new atomic skills with unique IDs;
- improvements to proof, writing, coding, experiment, figure, or release workflows;
- validator, builder, manifest, or CI hardening;
- documentation that clarifies task routing or reduces misuse;
- regression tests or examples that expose real failure modes.

Do not contribute:

- duplicate files with the same `S###` ID;
- undocumented rewrites of existing behavior;
- long-path aliases for files that already have Windows-safe canonical paths;
- skills that convert research problems into unsupported heuristic tuning;
- documentation that says a command or check passed unless it was actually executed;
- figure-generation instructions that ignore `figures4papers` when a close reusable pattern already exists;
- ad hoc hard-coded replacement of CSV / table / dataframe figure inputs unless the data source is intentionally changed and documented.

## Engine-binding policy

ZYR v1.6.6 uses explicit engine bindings.

### Proof engine

Any idea, method, contribution, theorem, derivation, or paper-storyline construction request must route through:

```text
proof_engine
→ S203 claim_evidence_matrix
→ S226 logic_consistency_audit
→ S227 method_correctness_audit
→ S230 proof_idea_check
→ S237 / S240 / S241 when assumptions, theorem sketches, or derivations matter
```

This gate must run before writing polish when the logical structure is still being formed.

### Writing engine

Any visible writing request must route through:

```text
writing_engine
→ ext/src/rpws/
→ S601 / S602 / S603 / S604 as needed
→ S640 as the global writing/logic gate
```

This covers manuscript sections, proposals, recommendation letters, README prose, rewrites, rebuttals, captions, result narratives, and reviewer-facing edits.

### Figure engine

Any figure-making request must route through:

```text
figure_engine
→ inspect ext/src/figures/ first
→ S621 / S622 / S623 as needed
→ coding_engine only when execution or repair is required
```

This covers scientific figures, workflow or architecture diagrams, figure repair, plotting-code adaptation, and export requests.

The figure engine is **figures4papers-backed**. Contributors must preserve the following behavior:
- inspect `ext/src/figures/` before drawing;
- reuse the closest existing plotting pattern when practical;
- preserve source-code-first generation;
- keep CSV / table / dataframe input logic unless there is a documented reason to change it;
- treat SVG as an export target, not as permission to hand-draw a brittle figure.

## Skill authoring rules

New routable skill files must be placed under the correct canonical directory and must be named as:

```text
skills/<category>/S###_<short_name>.md
```

The YAML front matter must include at least:

```yaml
id: S###
name: short_descriptive_name
category: research_core | experiments | reproducibility | paper_ops | research_writing_integrated | figure_design_integrated | s340_integrated | reproducibility_integrated
triggers:
  - example trigger
inputs_required:
  - required input
outputs_required:
  - required output
quality_gates:
  - acceptance check
```

Use the current canonical ranges unless a maintainer explicitly reserves a new range:

| Range | Category |
|---|---|
| `S2xx` | `research_core` |
| `S3xx` | `experiments` |
| `S4xx` | `reproducibility` |
| `S5xx` | `paper_ops` |
| `S6xx` | integrated research-writing, figure, S340, and release-validation skills |

## Integrated source policy

External or user-authored source materials must be preserved under `ext/src/` and cited through wrapper skills or attribution documents. Do not turn every upstream file into a routable skill. Since v1.6.5, the key integrated backends are:

- `ext/src/rpws/` for Research-Paper-Writing-Skills;
- `ext/src/awesome/` for supplementary writing prompts and examples;
- `ext/src/figures/` for figures4papers;
- `skills/rwf_s340/` for the integrated S6xx/S640/S650 wrappers.

Do not recreate removed compatibility directories such as the old research-writing or figure wrapper aliases. New routable writing/figure logic must go through the current engine bindings and integrated wrappers.

## In-place upgrade cleanup

If you update an existing Git checkout by copying files from a release ZIP, stale files may remain from older path layouts. Before validating, run:

```bash
python tools/cleanup_legacy_duplicate_paths_v1_6_5.py
```

This removes known duplicate aliases such as `skills/experiments/` and older long-name skill files when canonical replacements are present.

## Validation before a pull request

Run the following commands from the repository root:

```bash
python -m pip install -r requirements.txt
python tools/cleanup_legacy_duplicate_paths_v1_6_5.py
python tools/build_all.py
python tools/validate_v7_2.py
python tools/drift_audit_v1_3.py
```

For release-package or integrated-backend changes, also run:

```bash
python tools/validate_no_omission.py
python tools/validate_integrated_sources.py
python router/route.py "paper writing RPWS S340 logic audit"
python router/route.py "figure engine figures4papers plotting code png pdf"
python router/route.py "ZIP release no omission checksum path length"
```

A pull request should not be marked ready until all applicable commands pass or the failure is explicitly documented with its impact.

## Pull request checklist

- [ ] No duplicate `S###` IDs were introduced.
- [ ] New routable skills include `inputs_required`, `outputs_required`, and `quality_gates`.
- [ ] Canonical short paths are used.
- [ ] `README.md`, `skills_manifest.yaml`, and generated indexes are consistent when affected.
- [ ] Builders and validators pass.
- [ ] Any unverified claim, command, or external dependency is labeled honestly.
- [ ] Release-facing changes include a changelog entry when appropriate.
- [ ] Idea/method/storyline-facing changes preserve the `proof_engine` → S203/S226/S227/S230 chain.
- [ ] Writing-facing changes preserve the `writing_engine` → RPWS → S6xx/S640 chain.
- [ ] Figure-facing changes preserve the `figure_engine` → figures4papers → S621/S622/S623 chain.

## Review standard

Maintainers should review contributions with a failure-first mindset. The first blocking issue should be fixed before polishing language or expanding scope. A contribution that looks fluent but weakens evidence tracking, routing discipline, validation reliability, or the writing/figure engine bindings should be rejected or revised.
