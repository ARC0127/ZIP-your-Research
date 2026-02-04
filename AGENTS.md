## Mandatory response banner

Every assistant message must start with the one-line banner defined in `boot/00_RESPONSE_STATUS_BANNER_v1.0.1.md` (which references the authoritative definition in `boot/01_GLOBAL_GUARDRAILS_v1.0.1.md`).

# AGENTS.md (v1.0.1)

## Mission
Maintain this repository as a **copy/paste-first** research assistant skill library.
Preserve existing content; only add incremental improvements.

## Non-negotiable policies
- No fabrication: if uncertain, label UNKNOWN and propose verification steps.
- Separate facts vs hypotheses.
- Outputs must match the Output Contract of the selected skill.

## Editing rules
- Never delete existing modules or skills.
- Prefer additive changes: append v1.0.1 addenda rather than rewriting history.
- If you must change behavior, add a new file (e.g., validate_v7_1.py) and update CI to use it.

## Repo conventions
- `skills/**/S*.md` must include YAML front matter and a copy/paste prompt body.
- `skills/writing_engine/modules/*` is verbatim; do not rewrite.
- Generated artifacts:
  - `skills/writing_engine/MASTER_v1.0.1.md`

## Validation
- `tools/validate.py` is legacy.
- `tools/validate_v7_1.py` is authoritative in v1.0.1.
- CI should run build + validate_v7_1.

## Adding a new skill
1) Copy `templates/skill_template.md`
2) Assign the next appropriate segmented ID
3) Add at least one Example
4) Add entry to `skills_manifest.yaml` (append only)
5) Ensure `python tools/validate_v7_1.py` passes

## PR acceptance checklist
- validate passes
- no deletion of existing content
- new skills are copy/paste-ready
- UNKNOWN policy present

## v1.0.1 additions
- Router CLI: `router/route.py` is the machine-executable deterministic router.
- Validator: `tools/validate_v7_2.py` is the strict quality gate. Keep v1.0.1 validator for compatibility.
- Release packaging: `tools/make_release.py` produces a clean zip without `.git`.

## Coding standards (Python tools)
- Keep tools dependency-light (stdlib + PyYAML only).
- Every tool must have a CLI usage block at top-of-file.
- Tools must fail fast with clear error messages.


## Stage enforcement

- PRE-LOCK: intake / mode lock / usage clarification only.
  - **Exception (convenience):** you may give a *quick best-effort answer* **only** if it is short, conservative, explicitly marked out-of-protocol, and followed by an immediate return to intake.
- LOCKED: execute tasks within Mode Lock scope only.

If a drift happens in PRE-LOCK, run `boot/02_PRELOCK_VIOLATION_RESPONSE_v1.0.1.md`.
