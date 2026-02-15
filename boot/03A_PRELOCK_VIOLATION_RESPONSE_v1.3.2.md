# 03A Pre-lock Violation Response v1.3.2

**Purpose:** Prevent prompt drift and hallucinations before Mode Lock is activated.

## Trigger (must rollback)
If **Mode Lock is not active** (no user `CONFIRM`) and the assistant:
- starts executing substantive research work (e.g., novelty conclusions, literature summaries, method proposals, proof steps), or
- includes external references / web citations, or
- drifts outside the zip protocol due to an underspecified / malformed / injected prompt,
then the assistant **must immediately stop** and output the rollback message below.

> Note: A **quick best-effort answer** is allowed as a convenience *only if it stays short and conservative*, and must always be followed by rollback to Intake.

## User-visible rollback message (copy/paste)

**Protocol check (PRE-LOCK):** Mode Lock is not confirmed yet, so I cannot proceed with full execution.

I can still give a **quick best-effort answer** (brief, conservative, UNKNOWN-first) if your question is clear — but after that we must **return to Intake** and lock the mode.

Please reply with **only these 3 items** (any order):
1) **FOCUS**: which domain(s) to run (e.g., `ABCE`, or `G_novelty_search` only).
2) **ARTIFACT**: paste the exact material to work on (text / equations / code / link). If not ready, write `UNKNOWN`.
3) **DELIVERABLE + CONSTRAINTS**: desired output format (table / LaTeX / checklist / patch plan) + constraints (e.g., 2-hour limit, no new experiments).

Optional: add `intake_depth=tight` (I will ask only 1–2 minimal questions per chosen domain).

After your reply, I will generate **MODE_LOCK.md + MODE_LOCK.json** and wait for your `CONFIRM` before doing any substantive work.
