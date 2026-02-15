# Drift policy (v1.2)

This repo is designed to reduce **behavior drift** in chat usage.  
A common failure mode is **spec drift** inside the repo itself (docs reference tools that no longer exist).

## Policy
- If you add a backtick reference like `docs/DRIFT_POLICY.md`, you MUST ensure the file exists in the repo (or is explicitly generated).
- Prefer **shims** over breaking renames (e.g., keep `tools/validate_v7_2.py` as a wrapper).
- Keep normative MUST/SHALL rules in a single SSOT file whenever possible.

## Tooling
Run:
```bash
python tools/drift_audit_v1_3.py
python tools/validate_v7_2.py
```
