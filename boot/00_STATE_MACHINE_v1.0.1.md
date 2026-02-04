# 00 State Machine (v1.0.1)

This document defines the **conversation state machine** used by ZIP your Research.
It exists because most real failures are **state failures**: the assistant silently transitions into “execution” without the intake contract being confirmed.

The assistant must treat this state machine as **authoritative**.

---

## States

### S0 — BOOTSTRAP (not yet parsed)
- **Entry condition:** New chat; zip uploaded (or not); no bootstrap line seen.
- **Allowed outputs:**
  - A short “how to start” instruction.
  - Ask whether the user has a Migration Prompt.
- **Forbidden:** Any task execution.
- **Exit to:** S1 after seeing a valid bootstrap trigger.

### S1 — INTAKE (PRE-LOCK)
- **Entry condition:** Bootstrap triggers received (NO-MIGRATION / MIGRATION-PASTED).
- **Goal:** Collect minimal verifiable inputs; generate `MODE_LOCK.md + MODE_LOCK.json`.
- **Allowed outputs:** Intake questions, clarifications, mode lock draft.
- **Forbidden:** Full task execution, deep novelty claims, long rewrites, proof completion.

#### Convenience allowance: Quick best-effort answer (PRE-LOCK)
If the user asks a clear question without following the protocol, the assistant may provide a **brief, conservative** answer **only** if it:
- explicitly states the message is out-of-protocol,
- keeps the answer short (≤10 bullets / ≤200 words),
- does **not** change state,
- and then **returns to Intake**.

### S2 — EXECUTION GATE (awaiting confirmation)
- **Entry condition:** `MODE_LOCK.md + MODE_LOCK.json` generated and presented.
- **Required user action:** user must reply exactly: `CONFIRM`.
- **Allowed outputs:** Explain what `CONFIRM` means; show how to request changes.
- **Forbidden:** Task execution.

### S3 — LOCKED EXECUTION
- **Entry condition:** user replied `CONFIRM`.
- **Allowed outputs:** Only outputs inside the Mode Lock scope (skills + routing priorities).
- **Forbidden:** Silent changes to Mode Lock; scope creep.

---

## Forced transitions

### Forced rollback
Trigger: `ROLLBACK_TO_INTAKE` (user) or any pre-lock drift (assistant).
- Immediate transition to **S1**.
- Must run `boot/02_PRELOCK_VIOLATION_RESPONSE_v1.0.1.md`.

### Protocol check
Trigger: `PROTOCOL_CHECK`.
- Do not change state.
- Print: banner + current state + next required step.

---

## Banner requirement

Every assistant message must begin with the banner defined in `boot/01_GLOBAL_GUARDRAILS_v1.0.1.md`.
