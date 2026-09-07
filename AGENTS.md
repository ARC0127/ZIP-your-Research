## Mandatory response banner

Every assistant message must start with the one-line banner defined in `boot/00_RESPONSE_STATUS_BANNER_v1.6.6.md` (which references the authoritative definition in `boot/01_GLOBAL_GUARDRAILS_v1.6.6.md`). Release/component version precedence is defined in `docs/VERSION_IDENTITY_v1.6.6.md`.

# AGENTS.md (suite v1.6.6)

## Active execution profile

Apply `boot/14_RESOURCE_PROPORTIONAL_EXECUTION_v1.md` before interpreting
retained workflow defaults. It scopes intake to ZIP-only/strict startup,
preserves existing locks and explicit approvals, treats same-objective
corrections as in-scope steering, and makes skill loading and verification
proportional to the requested result. Ordinary work starts with one agent.
The active resource-aware router is `router/route_v1_8.py`; v1_7 is retained
for compatibility regression. No historical module is removed.

## Mission
Maintain this repository as a **copy/paste-first** research assistant skill library.
Preserve existing content; only add incremental improvements.

## Non-negotiable policies
- No fabrication: if uncertain, label UNKNOWN and propose verification steps.
- Separate facts vs hypotheses.
- Outputs must match the Output Contract of the selected skill.

## Editing rules
- Never delete existing modules or skills.
- Prefer additive changes: preserve v1.3.2 compatibility assets and add or update active v1.6.6 entrypoints rather than rewriting history.
- If you must change behavior, add a new file (e.g., validate_v7_1.py) and update CI to use it.

## Repo conventions
- Keep one dated, concrete latest-update section near the top of README.md.
  Replace that section on each update; do not append a release-history list.
  State suite/component versions accurately and link supporting audit details.
- `skills/**/S*.md` must include YAML front matter and a copy/paste prompt body.
- `skills/writing_engine/modules/*` is verbatim; do not rewrite.
- Generated artifacts:
  - `skills/writing_engine/MASTER_v1.6.6.md`
  - `skills/coding_engine/MASTER_v1.6.6.md`
  - `router/SKILL_MAP_v1.6.6.md`

## Validation
- `tools/validate.py` is legacy.
- `tools/validate_v1_3.py` remains the structural compatibility core.
- `tools/validate_v7_2.py` is the v1.6.6 compatibility facade and also enforces release identity.
- CI should run `python tools/zyr.py build --check` plus `python tools/validate_v7_2.py`.

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

## Legacy v1.3.2 compatibility notes
- Router CLI: `router/route.py` is the machine-executable deterministic router.
- Validator: `tools/validate_v7_2.py` is the strict quality gate. Keep v1.3.2 validator for compatibility.
- Release packaging: `tools/make_release.py` produces a clean zip without `.git`.

## Coding standards (Python tools)
- Keep tools dependency-light (stdlib + PyYAML only).
- Every tool must have a CLI usage block at top-of-file.
- Tools must fail fast with clear error messages.


## Stage enforcement

These stage rules apply to an explicitly selected ZIP-only/strict workflow,
as scoped by the active execution profile. Ordinary repository maintenance and
atomic skill requests use current task authorization without restarting intake.

- PRE-LOCK: intake / mode lock / usage clarification only.
  - **Exception (convenience):** you may give a *quick best-effort answer* **only** if it is short, conservative, explicitly marked out-of-protocol, and followed by an immediate return to intake.
- LOCKED: execute tasks within Mode Lock scope only.

If a drift happens in PRE-LOCK, run `boot/02_PRELOCK_VIOLATION_RESPONSE_v1.3.2.md`.

For authorized implementation, complete the requested files, relevant checks,
and delivery. Review-only requests remain review-only. Existing explicit
authorization for the same action is sufficient unless a governing rule requires
action-time confirmation; a skill's suggestion is not a new approval gate.

---

## v1.2 maintainer note — drift elimination

As of v1.2:
- `tools/validate_v7_1.py` and `tools/validate_v7_2.py` exist again as shims.
- Strict gate is `tools/validate_v1_3.py` (called by v7_2).
- Additions that introduce new references MUST either:
  - include the referenced file, or
  - mark the reference as generated (and explain generation path).
