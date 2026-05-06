# ZYR v1.6.3 CI and Documentation Repair Report

## Failure class

The GitHub CI failure was caused by three independent issues:

1. stale duplicate files left by in-place upgrades, especially old long paths such as `skills/experiments/` alongside the canonical `skills/exp/`;
2. duplicate S6xx integrated wrapper skills under `skills/rw/` and `skills/fig_ops/` while the same IDs also existed under `skills/rwf_s340/`;
3. incomplete front matter and stale source-path references in integrated S6xx skills.

## Repair actions

- Canonicalized integrated skills under `skills/rwf_s340/`.
- Removed duplicate routable S6xx files from `skills/rw/` and `skills/fig_ops/`.
- Added non-routable README notes to `skills/rw/` and `skills/fig_ops/`.
- Added `inputs_required`, `outputs_required`, and `quality_gates` to S601-S604, S621-S623, S640, and S650.
- Fixed source references to `ext/src/`.
- Added `tools/cleanup_legacy_duplicate_paths_v1_6_3.py` for existing Git repositories that still contain stale aliases.
- Added `requirements.txt`.
- Rewrote README and CONTRIBUTING in formal English.
- Updated CI to run cleanup before build and validation.

## Important upgrade note

A release ZIP cannot delete stale files already present in an existing Git checkout. If the repository was updated by copying new files over old files, run:

```bash
python tools/cleanup_legacy_duplicate_paths_v1_6_3.py
```

before running validation.
