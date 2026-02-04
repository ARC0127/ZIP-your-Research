# Changelog

## v1.0.1
- Added machine-executable router CLI: `router/route.py`.
- Added strict validator: `tools/validate_v7_2.py` and CI workflow `ci_v7_2.yml`.
- Added release packaging script: `tools/make_release.py` and docs `docs/RELEASE.md`.
- Added workflow recipes: `docs/WORKFLOWS.md` and template `templates/workflow_chain_template.md`.
- Added 40 new skills across research_core/experiments/reproducibility/paper_ops (S216–S225, S316–S325, S416–S425, S516–S525).
- Generated updated skill map: `router/SKILL_MAP_v1.0.1.md` (v1.0.1 map retained).

## v1.0.1
- Added generated writing_engine master prompt: `skills/writing_engine/MASTER_v1.0.1.md`.
- Added v1.0.1 build pipeline: `tools/build_index.py`, `tools/build_all.py`.
- Added robust validator: `tools/validate_v7_1.py` (legacy `tools/validate.py` kept).
- Added deterministic router addendum and expanded taxonomy.
- Added documentation: docs/USAGE.md, docs/QUICKSTART.md, docs/SKILL_AUTHORING_GUIDE.md.
- Added agent guidance: AGENTS.md.
- Added CI workflow `CI (v1.0.1)` with build + validate + artifact sync checks.
- Added many new research skills (S2xx/S3xx/S4xx/S5xx), all copy/paste-ready.

## v1.0.1
- Initial modular skill structure and writing_engine wrapper.


## v1.0.1 (2026-02-02)
### Added
- Weighted router with configurable priorities: `router/weights_v1.0.1.yaml` + enhanced `router/route.py`
- New correctness-first skills: S226, S227, S229, S230, S232; calculation & experiment completeness: S326, S327; novelty: S228, S231; rewriting with retrieval: S526
- New workflows: WF-5 (correctness-first audit) and WF-6 (novelty stress test)
- New skill map artifact: `router/SKILL_MAP_v1.0.1.md` and updated manifest version

### Notes
- Incremental-only: no deletions; existing skills remain intact.


## v1.0.1 (session-first bootstrap & mode lock)
- Added v1.0.1 bootstrap protocol for zip-only startup (boot/).
- Added migration prompt template & detector.
- Added mode lock format and locked response templates.
- Added ROUTER_v8 session-first routing doc.

## v1.0.1 — 2026-02-02

### Added
- First-turn application guide and optional session overrides block.
- Configurable intake interview profile (`router/intake_profile_v8_1.yaml`) with default priorities:
  A_logic → B_method → C_calculation → E_innovation_correctness.
- MODE_LOCK JSON schema + template and migration prompt generator.
- New high-priority skills: S233 (innovation correctness), S234 (novelty search protocol), S235 (proof gap finder),
  S328 (experiment rigor scorecard), S527 (claim language risk linter).

### Notes
- This is an additive release: no existing files removed; only new files and appended addenda.

## v1.0.1 — 2026-02-02

### Added
- Deep intake default policy (`boot/09_INTAKE_DEPTH_POLICY_v8_2.md`) and v1.0.1 application guide.
- Authoritative deep intake profile (`router/intake_profile_v1.0.1.yaml`) and rendered checklist.
- Utility script to print intake questions (`tools/render_intake_questions_v8_2.py`).

### Notes
- Additive update: no existing files removed; only new files and appended addenda.

## v1.0.1 — 2026-02-02

### Added (major)
- Governance workflows: preregistration, DMS, systematic review, reporting checklists, ethics, replication package.
- New skills: S236, S238, S239, S336, S426, S427, S428, S429, S528, S529, S530.
- Extended intake profile: `router/intake_profile_v9_0.yaml` (optional governance modules).

### Notes
- Additive update: no existing files removed; only new files and appended addenda.

## 1.0.0 — 2026-02-02

### Added
- SemVer policy + `VERSION` file.
- Public extension layer (`interfaces/`) with provider contract + schemas + example config.
- Built-in providers: OpenAlex, Crossref, arXiv, Semantic Scholar.
- Hooks: deduplicate by DOI/title.
- CLI utility: `tools/ra_cli.py` (providers + repropack skeleton initializer).

### Compatibility
- Additive release: no existing files removed.

## 1.0.1 — 2026-02-02

### Fixed
- Added `interfaces/__init__.py` to improve import compatibility across Python setups.
