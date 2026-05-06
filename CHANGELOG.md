# Changelog

## v1.6.5 - README professionalism, engine-binding consolidation, and package hygiene

This release consolidates the v1.6 line around a clearer public README and a stricter internal engine-binding contract.

### Added

- `skills/figure_engine/MASTER_v1.6.5.md` as the mandatory figures4papers-backed entry point for figure-making tasks.
- `docs/how_to_use/ZYR_ENGINE_BINDING_HOW_TO_USE_v1.6.5.md`.
- `docs/how_to_use/PLATFORM_SKILLS_integr_v1.6.5.md`.

### Changed

- Rewrote `README.md` into a professional release-facing document centered on:
  - task locking;
  - proof / writing / figure / coding / release engine bindings;
  - source-preserving execution;
  - validation before artifact acceptance.
- Strengthened the proof-first rule for idea, method, contribution, and paper-storyline tasks.
- Strengthened the writing route so visible prose tasks bind to `writing_engine`, Research-Paper-Writing-Skills, S601-S604, and S640.
- Strengthened the figure route so figure tasks bind to `figure_engine`, figures4papers, S621-S623, and source-code-first generation.
- Updated `docs/how_to_use/` to match the current engine-binding model.
- Updated router references to point to the v1.6.5 figure-engine master.

### Removed

- Older v1.6.4 how-to files that would duplicate or confuse the v1.6.5 usage guidance.
- Stale references to older figure-engine master filenames.


## v1.6.4 - unified engine bindings, cleanup, and release consolidation

This release consolidates the v1.6 line into a cleaner package layout. The ZYR state-machine logic is unchanged: bootstrap, intake, MODE_LOCK, locked execution, routing, verification, and artifact reporting remain the core workflow.

### Added

- `skills/figure_engine/MASTER_v1.6.4.md` as the mandatory composite entry point for figure-making tasks.
- Explicit README and CONTRIBUTING rules that bind:
  - writing tasks to `writing_engine` + `ext/src/rpws/` + S601-S604 + S640;
  - figure tasks to `figure_engine` + `ext/src/figures/` + S621-S623.
- A consolidated release audit at `manifests/RELEASE_AUDIT_v1.6.4.md`.

### Changed

- Unified the package release version to `1.6.4`.
- Rewrote README around task routing, engine selection, source-preserving execution, and validation.
- Rewrote CONTRIBUTING around unique skill IDs, engine-binding discipline, source-preservation policy, and release checks.
- Strengthened the figure workflow:
  - inspect `figures4papers` before drawing;
  - reuse the closest existing source pattern when practical;
  - preserve CSV / table / dataframe loading logic unless the data source is intentionally changed;
  - treat SVG, PNG, and PDF as exports rather than substitutes for generating source.
- Strengthened the writing workflow:
  - use Research-Paper-Writing-Skills through `writing_engine`;
  - keep S640 as the global writing and logic gate for visible prose.
- Updated router hints and weights so writing-like requests prefer `writing_engine`, and figure-like requests prefer `figure_engine`.

### Removed

- Obsolete repair and intermediate audit files from earlier v1.6 repair passes.
- Empty compatibility wrapper directories from prior research-writing and figure path layouts.
- Generated Python bytecode and temporary repair metadata.

### Preserved

- The original ZYR boot / proof / coding / migration discipline.
- External source trees under `ext/src/`:
  - Research-Paper-Writing-Skills;
  - awesome-ai-research-writing;
  - figures4papers;
  - the local S340 ruleset.
- Source manifests, checksum validation, route smoke tests, and no-omission validation.
