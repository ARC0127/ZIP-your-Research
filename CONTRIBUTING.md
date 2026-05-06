# Contributing to ZIP-your-Research

Thank you for improving ZIP-your-Research (ZYR). Contributions are welcome when they preserve the repository's central purpose: task-boundary discipline, evidence-aware execution, and verifiable research artifacts.

This document defines the contribution rules for the v1.6 line.

## Contribution principles

A contribution is acceptable only if it preserves the following invariants:

1. **One skill ID maps to one canonical routable skill file.** Do not add alias files with the same `S###` identifier.
2. **Evidence boundaries must remain explicit.** New prompts or skills must not encourage unsupported claims, fabricated verification, or hidden uncertainty.
3. **Short paths are canonical.** Use `skills/exp/`, `skills/rwf_s340/`, `ext/src/`, `router/ext_router/`, and the current manifest filenames.
4. **Builders and validators must pass.** A change is not complete until the repository builds and strict validation succeeds.
5. **Historical material may be retained for attribution, but not as duplicate routable skills.** If a source is preserved, place it under `ext/src/` or a clearly non-routable reference path.

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
- documentation that says a command or check passed unless it was actually executed.

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

External or user-authored source materials must be preserved under `ext/src/` and cited through wrapper skills or attribution documents. Do not turn every upstream file into a routable skill. The v1.6 integrated routes are canonicalized under:

```text
skills/rwf_s340/
```

The directories `skills/rw/` and `skills/fig_ops/` are non-routable reference locations in v1.6.3. Do not add `S###_*.md` files there unless the validator and manifest are intentionally changed to support a new canonical route.

## In-place upgrade cleanup

If you update an existing Git checkout by copying files from a release ZIP, stale files may remain from older path layouts. Before validating, run:

```bash
python tools/cleanup_legacy_duplicate_paths_v1_6_3.py
```

This removes known duplicate aliases such as `skills/experiments/` and older long-name skill files when canonical replacements are present.

## Validation before a pull request

Run the following commands from the repository root:

```bash
python -m pip install -r requirements.txt
python tools/cleanup_legacy_duplicate_paths_v1_6_3.py
python tools/build_all.py
python tools/validate_v7_2.py
python tools/drift_audit_v1_3.py
```

For release-package changes, also run:

```bash
python tools/validate_no_omission.py
python tools/validate_integrated_sources.py
python router/route.py "paper writing S340 logic audit"
python router/route.py "matplotlib publication figure svg png"
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
- [ ] Release-facing changes include a changelog entry.

## Review standard

Maintainers should review contributions with a failure-first mindset. The first blocking issue should be fixed before polishing language or expanding scope. A contribution that looks fluent but weakens evidence tracking, routing discipline, or validation reliability should be rejected or revised.
