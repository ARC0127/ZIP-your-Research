# Changelog

## v1.7.0 — 2026-09-07

- Route ordinary tasks to one primary skill and the current agent; preserve
  full requested workflows, explicit approvals and scientific evidence rules.
- Remove recurring status banners. Show diagnostics only on request.
- Unify active engine entries, strict bootstrap, Mode Lock Markdown/JSON,
  migration prompts and installed skill metadata at v1.7.0. The release gate
  rejects old session-version values; historical sources remain reproducible.
- Remove 46 obsolete document/report copies, consolidate current guides, and
  provide three practical usage paths with inputs and expected outputs in README.
- Update existing local ZYR installations with backups; separately remove only
  unchanged retired copies, with restore receipts. Model settings are unchanged.

## v1.6.6 - agentic research evolution, visible memory, and governed Skill learning

This release turns ZYR's self-evolution goal into an inspectable research
protocol: agents may broaden authoritative retrieval, challenge candidate
ideas, and improve the next research action, while claims, evidence, memory,
and persistent changes remain under explicit human control.

### Added

- `S660 epistemic_research_champion` for capability-gated multi-agent research,
  blind first-round retrieval, evidence lineage, candidate versioning,
  cross-examination, and scientific adjudication.
- `S661 dynamic_skill_memory` for proposal-only Skill generation from verified
  traces and governed create, promote, update, rollback, deprecate, and delete
  operations in an external `dyn-*` store.
- A visible Scientific Decision Record in
  `templates/orchestration/RESEARCH_RUN.md`, plus short-/long-term memory,
  consent, audit, and export templates.
- Host capability and provider contracts, including explicit failure behavior
  when real worker contexts, authoritative retrieval, approval channels, or
  local persistence are unavailable.
- Stable `tools/zyr.py` commands, deterministic v1.7 routing, release
  allowlisting/auditing, compatibility and capability manifests, and integrity,
  security, router, evolution, release, and dynamic-memory tests.

### Changed

- Reworked the README opening around concrete Agentic LLM research workflows,
  clearer onboarding, and stronger public positioning while retaining the
  scientific-evidence boundary.
- Strengthened proof-first paper logic, scientific writing, rhetoric
  refinement, source-code-first figure design, figure/claim consistency, and
  integrated package validation.
- Extended CI to exercise the stable facade, generated-file drift checks,
  deterministic routing, security boundaries, and release closure.
- Replaced the extra Python cryptography dependency with a standard-library
  Ed25519 verifier anchored to the RFC 8032 test vector; host private keys and
  signing remain outside the agent.

### Safety and evidence boundaries

- Automatic Skill drafting does not authorize save, registration, activation,
  update, or deletion. Every mutation requires a content-bound plan and a
  short-lived signed host attestation.
- The dynamic store persists detached signed authorization receipts and the
  pinned public key, allowing verification to reject post-consent registry or
  payload rewrites even when derived hashes are rebuilt without the host key.
- Structural tests do not claim independent scientific replication or LLM
  behavioral superiority. Unrun or unavailable checks remain explicit.
- The complete pre-existing README acknowledgments and reference section was
  retained byte-for-byte during the final v1.6.6 clarity and promotion pass.

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
- A consolidated release audit, retained in [Git history](https://github.com/ARC0127/ZIP-your-Research/blob/b290a2a650b2e0f4dab55ff613697ae1fdcfe86f/manifests/RELEASE_AUDIT_v1.6.4.md).

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
