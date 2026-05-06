# ZYR v1.6.5 CI Fix Release Audit

## Fixed issue

GitHub Actions failed at:

```text
python tools/cleanup_legacy_duplicate_paths_v1_6_4.py
```

because the workflow still called the v1.6.4 cleanup script while the package had already moved the cleanup implementation to:

```text
tools/cleanup_legacy_duplicate_paths_v1_6_5.py
```

## Changes

- Updated `.github/workflows/ci.yml` to call `tools/cleanup_legacy_duplicate_paths_v1_6_5.py`.
- Updated `.github/workflows/ci_v7_2.yml` to call `tools/cleanup_legacy_duplicate_paths_v1_6_5.py`.
- Added `tools/cleanup_legacy_duplicate_paths_v1_6_4.py` as a backward-compatible wrapper so stale local workflows do not fail before validation.
- Fixed cleanup-script usage text to reference v1.6.5.
- Kept version as `1.6.5`.

## Static validation

```json
{
  "ci_workflow_refs": {
    ".github/workflows/ci.yml": {
      "exists": true,
      "uses_v1_6_5_cleanup": true,
      "uses_missing_v1_6_4_cleanup": false
    },
    ".github/workflows/ci_v7_2.yml": {
      "exists": true,
      "uses_v1_6_5_cleanup": true,
      "uses_missing_v1_6_4_cleanup": false
    }
  },
  "cleanup_scripts": {
    "tools/cleanup_legacy_duplicate_paths_v1_6_5.py": true,
    "tools/cleanup_legacy_duplicate_paths_v1_6_4.py": true
  },
  "figure_engine_master": {
    "v1_6_5_exists": true,
    "v1_6_4_exists": false
  }
}
```

## Stale-reference scan

```json
{
  "cleanup_legacy_duplicate_paths_v1_6_4.py": [
    "manifests/src_FILE_integr_TABLE.md"
  ],
  "MASTER_v1.6.4.md": [
    "CHANGELOG.md",
    "manifests/src_FILE_integr_TABLE.md",
    "docs/integrated_external_skills/README_integrated_stack_v1.0.md",
    "artifacts/integration/integr_manifest.json"
  ],
  "v1.6.4": [
    "CHANGELOG.md",
    "manifests/RELEASE_AUDIT_v1.6.4.md",
    "manifests/src_FILE_integr_TABLE.md",
    "manifests/src_manifest.json",
    "docs/integrated_external_skills/README_integrated_stack_v1.0.md",
    "artifacts/integration/integr_manifest.json"
  ]
}
```

## Note

The exact reported CI failure is fixed by both updating the workflow and preserving a compatibility wrapper. This release does not use canvas.
