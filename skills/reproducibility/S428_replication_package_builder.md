---
id: S428
name: replication_package_builder
category: reproducibility
triggers:
- replication package
- artifact bundle
- reproducibility package
- 复现包
- camera-ready artifact
inputs_required:
- repo_structure
- data_locations
- target_artifacts
outputs_required:
- package_plan
- entrypoints
- verification_record
quality_gates:
- no_fabrication
- mark_UNKNOWN
- audit_first
- copy_paste_ready
---

> **Global invariant (ZIP your Research):** Truthfulness • Trustworthiness • Deep logical reasoning. If required info is missing → mark **UNKNOWN** and ask minimal questions.

# S428 Replication Package Builder (Artifact Bundle)

## Role
Design a minimal replication package: entrypoints, environment, data pointers, expected outputs.

## Input
- Repo structure (or list of scripts)
- Data location(s) (local / remote / to be released)
- Compute assumptions (GPU/CPU)
- What result must be reproducible (tables/figures/metrics)

## Output Contract
1) Reproduction entrypoints (commands) for each target artifact.
2) Environment spec plan (conda/pip/docker) + version pinning checklist.
3) Data manifest (what is required, where, checksums if available).
4) Expected outputs + tolerance (exact vs approximate).
5) Troubleshooting tree (common failure modes).
6) Verification record.

## Rules
- If you cannot inspect the repo, output a generic structure + UNKNOWN markers.
