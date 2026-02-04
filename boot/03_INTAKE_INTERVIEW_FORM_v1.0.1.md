# 03 Intake Interview Form v1.0.1

**Purpose:** collect minimal, verifiable inputs before executing research tasks.

## Rules
- Ask questions in natural language (no YAML logs).
- Keep questions precise and actionable.
- If the user is time-constrained, offer `intake_depth: tight`.

## Interview source of truth
- The exact interview questions are defined in: `router/intake_profile_v1.0.1.yaml`
- A printable checklist is in: `router/INTAKE_CHECKLIST_v1.0.1.md`


## Robust intake parsing (important)
Users often reply in free-form (not following the numbered questions). Before Mode Lock is confirmed:

- Treat ANY task request as *scope selection*, not execution.
- Extract overrides if present (examples):
  - `intake_depth=tight|standard|deep`
  - `DEBUG_TRACE=ON`
  - `FOCUS=G_novelty_search` (or any domain key)
  - `web_browsing_policy=FORBID` (explicit only)
- If the user provides partial answers, do NOT guess missing fields. Mark them as UNKNOWN and ask the minimal questions needed.

## Minimal-questions rule (pre-lock)
If the user says they only want one domain (e.g., `FOCUS=G_novelty_search`):
- Ask ONLY that domain’s minimal questions according to intake_depth.
- Generate MODE_LOCK for that narrow scope.
- Wait for `CONFIRM` before doing the actual work.
