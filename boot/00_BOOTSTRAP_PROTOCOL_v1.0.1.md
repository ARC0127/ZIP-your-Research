# 00 Bootstrap Protocol v1.0.1

This repository is designed for **ZIP-only startup**: the user uploads the ZIP and the assistant boots the workflow.

## Hard constraints
- **No fabrication.** If a required fact is missing: label **UNKNOWN** and request the minimal missing input.
- **Readability-first.** User-visible answers must be natural and professional (no YAML/debug dumps).
- **Execution Gate:** Before Mode Lock activation, do NOT execute substantive research tasks.

- **Pre-lock violation rollback:** If any pre-lock output violates the Execution Gate (substantive work or external references), immediately output: `boot/03A_PRELOCK_VIOLATION_RESPONSE_v1.0.1.md` and return to Intake → Mode Lock generation.

- **Pre-lock scope freeze:** During Steps 0–3 (Bootstrap/Intake/Mode Lock generation), output MUST contain only:
  1) the Application Guide, and
  2) the Intake questions / Mode Lock artifacts.
  Do NOT add “extra commentary”, background explanations, literature summaries, or any external references.
- **Pre-lock web browsing: OFF.** Even if the default policy is ALLOW, web browsing is only permitted AFTER user confirms Mode Lock.
  (Rationale: prevent drift/hallucinations before the contract is locked.)
- **Noncompliant input handler:** If the user reply does not follow the expected intake format (e.g., only a partial override like “intake_depth=tight”,
  or a task request like “help me search world models”), DO NOT execute the task. Instead:
  - Parse any obvious overrides (intake_depth / domains / web policy / debug_trace).
  - Ask ONLY the minimal missing intake questions needed to generate Mode Lock for the requested scope.
  - Then generate Mode Lock and request CONFIRM.


## Step 0 — Migration detection (required)
Ask the user:

1) Did you paste a MIGRATION PROMPT (English) from a previous chat?
- If yes: load it and treat it as authoritative.
- If no: proceed with `NO-MIGRATION`.

## Step 1 — Show the Application Guide (required)
Print (user-visible): `boot/07_FIRST_TURN_APPLICATION_GUIDE_v1.0.1.md`

## Step 2 — Intake interview (required)
Run the intake interview profile:
- File: `router/intake_profile_v1.0.1.yaml`
- Defaults:
  - web_browsing_policy: **ALLOW**
  - intake_depth: **deep** (unless user overrides)

## Step 3 — Generate Mode Lock (required)
Generate:
- `MODE_LOCK.md` + `MODE_LOCK.json`
- Using: `boot/04_MODE_LOCK_FORMAT_v1.0.1.md`

Then ask the user to reply: **CONFIRM**.

## Step 4 — Locked execution
Only after CONFIRM:
- Execute tasks using the locked contracts and routing priorities.
- Hide routing/debug metadata unless the user explicitly writes: `DEBUG_TRACE=ON`.
