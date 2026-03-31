# Release Packaging (v1.5.0)

This document describes the current packaging workflow for the formal `v1.5.0` release line.

`v1.5.0` is the formal release that closes the alignment work started from `v1.4.4`, with stricter validation and a stronger artifact/proof stack.

## Current recommended flow

From the repository root:

```bash
python3 tools/build_all.py
python3 tools/validate_v7_2.py
python3 tools/drift_audit_v1_3.py
python3 tools/validate_corpus_v1_3.py
python3 tools/simulate_locked_regression_v1_3.py --n 25 --seed 0
python3 tools/validate_completion_corpus_v1_5.py
python3 tools/simulate_completion_compliance_v1_5.py
python3 tools/validate_scientific_discipline_corpus_v1_5.py
python3 tools/simulate_scientific_discipline_v1_5.py
python3 tools/validate_proof_verification_corpus_v1_5.py
python3 tools/simulate_proof_verification_v1_5.py
python3 tools/system_audit_v1_3.py
python3 tools/make_release.py
```

## What this produces

- regenerated composite prompts and indexes
- refreshed deterministic reports under `artifacts/`
- a clean zip named from `VERSION`

With the current `VERSION`, the default package name is:

- `ZIP-your-Research_v1.5.0_release.zip`

## Version source of truth

- `VERSION` is the packaging source of truth
- `tools/make_release.py` reads `VERSION` by default
- `skills_manifest.yaml`, `README.md`, and `CHANGELOG.md` should agree with `VERSION`

If you need to override the version explicitly:

```bash
python3 tools/make_release.py --version v1.5.0
```

## Release expectations for this line

Before packaging, ensure all of the following are true:

- `README.md` reflects the `v1.5.0` release posture
- `CHANGELOG.md` has the latest `1.4.4 -> v1.5.0` summary at the top
- `proof_engine` has been rebuilt into `skills/proof_engine/MASTER_v1.5.md`
- proof/completion/scientific-discipline regressions all pass
- `artifacts/system_audit/report_v1.3.2.md` reflects the current workspace rather than the old `v1.4.4` copy

## Why package without `.git`

- smaller distribution size
- cleaner copy/paste usage for end users
- lower risk of shipping irrelevant local history

Do not rely on the release zip as a substitute for proper git history or reproducible release tagging.
