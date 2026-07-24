---
id: S650
name: integrated_pack_no_omission_validation
category: reproducibility_integrated
version: v1.6.5
triggers:
- validate integrated pack
- no omission
- checksum
- source manifest
- path length
- 压缩包无法打开
- 文件名过长
- 完整性验证
- 禁止遗漏
inputs_required:
- release tree or ZIP package
- source manifests/checksum files when available
- expected canonical path layout
- CI failure log when available
outputs_required:
- missing/duplicate/stale path report
- repair actions
- validation command results
- release ZIP or patch instructions when requested
quality_gates:
- duplicate skill IDs are eliminated
- all referenced paths resolve or are explicitly external/ignored
- CI validation commands pass before release is accepted
---

# S650 Integrated Package No-Omission Validation

Use whenever building, repairing, or distributing this integrated skills package.

Procedure: verify ZIP CRC; copy each source file byte-for-byte; generate manifest with source zip, original path, packed path, size, SHA-256 and kind; generate script inventory; run `tools/validate_no_omission.py`; check ZIP integrity and maximum internal path length; diagnose path-length/openability before guessing.

## Non-omission source rule

The complete source trees are preserved under `ext/src/`. This skill is a routing wrapper and logical reconstruction layer, not a replacement for the source files. For exact file-level coverage, inspect `manifests/src_manifest.json` and `manifests/src_FILE_integr_TABLE.md`.

## v1.7 safe-release profile addendum

“Complete source trees” above describes the full development checkout, not the
default safety release. For a release audit, the authoritative closure is the
required set and capability state in `manifests/release_policy.yaml` and
`manifests/RELEASE_CAPABILITIES.yaml`. A policy-excluded source must be
reported as `SOURCE_UNAVAILABLE`; it must not be reclassified as present merely
because its wrapper skill or historical inventory remains in the archive.
