---
id: S650
name: integrated_pack_no_omission_validation
category: reproducibility_integrated
version: v2.0
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
---

# S650 Integrated Package No-Omission Validation

Use whenever building, repairing, or distributing this integrated skills package.

Procedure: verify ZIP CRC; copy each source file byte-for-byte; generate manifest with source zip, original path, packed path, size, SHA-256 and kind; generate script inventory; run `tools/validate_no_omission.py`; check ZIP integrity and maximum internal path length; diagnose path-length/openability before guessing.

## Non-omission source rule

The complete source trees are preserved under `ext/src/`. This skill is a routing wrapper and logical reconstruction layer, not a replacement for the source files. For exact file-level coverage, inspect `manifests/src_manifest.json` and `manifests/src_FILE_integr_TABLE.md`.
