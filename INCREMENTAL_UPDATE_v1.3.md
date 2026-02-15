# Incremental Update v1.3

> Maintainer-facing summary of changes since v1.2.  
> Additive-first; no deletions of prior logs.

## 0) Primary objectives
1) **One-chat agentic research closure** (no external framework): emulate multi-agent flow via phase gating + artifacts.
2) **Onboarding clarity**: a newcomer can find focus skills and common entry points in <5 minutes.
3) **Explicit attribution**: cite public descriptions of FARS / Hello-Agents as design inspirations.
4) **Regression against perturbations**: stronger prompt disturbance corpus (including high-entropy fuzz payloads).

## 1) New SSOT additions
- `boot/12_ONECHAT_DEEP_LOOP_v1.3.md`
- `docs/ONBOARDING_FASTPATH_v1.3.md`
- `docs/ONECHAT_PLAYBOOK_v1.3.md`
- `docs/SKILLS.md`
- `docs/AGENTIC_ARCHITECTURE_v1.3.md`
- `docs/HELLO_AGENTS_ADAPTATION_v1.3.md`
- `docs/ATTRIBUTION_v1.3.md`

## 2) Expanded regression suite
- `tests/prompt_regression/corpus_v1_3.jsonl`
- `tests/prompt_regression/fuzz_payloads_v1_3.bin` (3 MiB; mostly-uncompressible)
- generator: `tools/gen_fuzz_payloads_v1_3.py`

## 3) Version & references
- Updated to 1.3: `VERSION`, `skills_manifest.yaml`, README/INDEX headers.
- Added v1.3.1 variants of LOCKED firewall docs:
  - `boot/10_LOCKED_SCOPE_GUARD_v1.3.md`
  - `boot/11_REQUIREMENTS_LOCK_LOOP_v1.3.md`

## 4) Recommended release commands
```bash
python tools/build_all.py
python tools/validate_v7_2.py
python tools/drift_audit_v1_3.py
python tools/gen_skills_catalog_v1_3.py
python tools/make_release.py --version v1.3
```
