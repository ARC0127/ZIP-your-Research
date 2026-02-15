# Changelog

## v1.3.2 (2026-02-15)

### Goal
A **system-level normalization + audit pass**: remove legacy v1.0.1-named artifacts, make prompt-regression checks schema-driven (not heuristic), and add a reproducible system-audit command that verifies end-to-end logical consistency.

### Removed
- Legacy v1.0.1-named artifacts (superseded by v1.3.2 equivalents; changelog history retained):
  - `boot/*_v1.0.1.*`, `router/*_v1.0.1.*`, `router/weights_v1.0.1.yaml`, `router/intake_profile_v1.0.1.yaml`
  - `docs/AUDIT_REPORT_v1.0.1.*`, `docs/archive/*`, duplicated How-to-use PDF under `tools/how_to_use/`
- Outdated generated artifacts from v1.3.1 (re-generated under v1.3.2 naming).

### Changed
- Canonical master prompts bumped to v1.3.2:
  - `skills/writing_engine/MASTER_v1.3.2.md`
  - `skills/coding_engine/MASTER_v1.3.2.md`
- Router now targets the v1.3.2 masters + weights/profile naming (`router/route.py`, `router/weights_v1.3.2.yaml`, `router/intake_profile_v1.3.2.yaml`).
- Drift audit now ignores historical logs (`CHANGELOG.md`, `INCREMENTAL_UPDATE_*`) to avoid false positives on removed legacy artifacts.

### Added
- Prompt regression schema + validator:
  - `tests/prompt_regression/corpus_schema_v1_3.json`
  - `tools/validate_corpus_v1_3.py`
  - `docs/PROMPT_REGRESSION.md`
- LOCKED simulator upgraded to **label-driven** pass/fail (heuristics kept only as diagnostics):
  - `tools/simulate_locked_regression_v1_3.py` → writes `artifacts/locked_regression/report_v1.3.2.md`
- Reproducible system audit command:
  - `tools/system_audit_v1_3.py` → writes `artifacts/system_audit/report_v1.3.2.md`

### Fixed
- GitHub Actions CI now installs `PyYAML` via `requirements.txt`, preventing `ModuleNotFoundError: yaml` during `tools/build_all.py` and strict validation.

---

## v1.3.1 (2026-02-15)

### Goal
Tighten v1.3 into a **clean, non-redundant** release: remove unused archives and legacy v1.2 artifacts, canonicalize validator/audit names, and add a deterministic **LOCKED perturbation simulator** based on `corpus_v1_3`.

### Removed
- Unused embedded archive: `ZIP-your-Research_v1.3_release.zip` (was ~68KB and not referenced).
- Legacy v1.2 artifacts kept only in CHANGELOG history (files deleted):
  - `boot/*_v1.2.md`, skills/coding_engine/MASTER_v1.2.md, `tests/prompt_regression/*_v1_2.*`, INCREMENTAL_UPDATE_v1.2.md, AUTOBOOT_v1.0.1.md.

### Changed
- Release packager `tools/make_release.py` now excludes archive suffixes to prevent nested zips.
- Canonical maintainer tools renamed to v1.3:
  - `tools/validate_v1_3.py` (shims `validate_v7_1.py` / `validate_v7_2.py` updated)
  - `tools/drift_audit_v1_3.py` (CI + docs updated)
- Routing + coding_engine canonicalized to v1.3:
  - `router/route.py` now points to `skills/coding_engine/MASTER_v1.3.md`
  - coding_engine module header cleaned to avoid conflicting v1.2 headings.

### Added
- LOCKED perturbation simulation:
  - `tools/simulate_locked_regression_v1_3.py` → writes `artifacts/locked_regression/report_v1.3.1.md`

---

## v1.3 (2026-02-15)

### Goal
Agentic‑style **single‑conversation research closure** (ONECHAT_LOOP) + stronger onboarding + explicit attribution to public agentic research systems.

### Added
- ONECHAT protocol (single chat agentic loop):
  - `boot/12_ONECHAT_DEEP_LOOP_v1.3.md`
  - `docs/ONECHAT_PLAYBOOK_v1.3.md`
  - `docs/ONBOARDING_FASTPATH_v1.3.md`
- Onboarding & skill discoverability:
  - `docs/SKILLS.md` (human‑first catalog)
  - `tools/gen_skills_catalog_v1_3.py` (generates `docs/SKILLS_INDEX_GENERATED_v1.3.md`)
- Agentic architecture & attributions:
  - `docs/AGENTIC_ARCHITECTURE_v1.3.md`
  - `docs/HELLO_AGENTS_ADAPTATION_v1.3.md`
  - `docs/ATTRIBUTION_v1.3.md`
- Coding minimalism module:
  - `skills/coding_engine/modules/05_MINIMALISM.md`

- Expanded prompt regression suite:
  - `tests/prompt_regression/corpus_v1_3.jsonl`
  - `tests/prompt_regression/fuzz_payloads_v1_3.bin`
  - generator: `tools/gen_fuzz_payloads_v1_3.py`

### Changed
- Version bump to 1.3 (`VERSION`, `skills_manifest.yaml`, README/INDEX headers).
- LOCKED scope guard + per‑turn requirements loop updated to v1.3:
  - `boot/10_LOCKED_SCOPE_GUARD_v1.3.md`
  - `boot/11_REQUIREMENTS_LOCK_LOOP_v1.3.md`

---

## v1.2 (2026-02-15)

### Goal
System-level hardening for **instruction adherence under conversation perturbations**, and a stronger **vibe coding** workflow with closure-first scaffolding.

### Added
- LOCKED drift firewall:
  - `boot/10_LOCKED_SCOPE_GUARD_v1.3.md`
  - `boot/11_REQUIREMENTS_LOCK_LOOP_v1.3.md`
- New reproducibility skills:
  - `S431_closed_loop_verification` (template for S430 PASS closure)
  - `S432_scope_drift_firewall` (maps user perturbations into an explicit state machine)
- New composite prompt:
  - `skills/coding_engine/MASTER_v1.3.md` (+ build tool tools/build_coding_engine.py)
- Maintainer tooling:
  - `tools/validate_v1_3.py` (strict), plus shims `tools/validate_v7_1.py` / `tools/validate_v7_2.py`
  - `tools/drift_audit_v1_3.py` + `docs/DRIFT_POLICY.md`
  - compatibility aliases: `boot/09_INTAKE_DEPTH_POLICY_v8_2.md`, `router/intake_profile_v8_1.yaml`, `router/intake_profile_v9_0.yaml`, `tools/render_intake_questions_v8_2.py`
- Prompt regression corpus:
  - tests/prompt_regression/corpus_v1_2.jsonl
  - tests/prompt_regression/fuzz_payloads_v1_2.bin

### Changed
- CI now runs build + strict validation + drift audit.

---

## v1.0.1
- Added machine-executable router CLI: `router/route.py`.
- Added strict validator: `tools/validate_v7_2.py` and CI workflow `.github/workflows/ci_v7_2.yml`.
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
