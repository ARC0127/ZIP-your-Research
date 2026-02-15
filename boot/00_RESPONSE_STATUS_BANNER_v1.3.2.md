# 00 Response Status Banner (v1.3.2)

This file is a **single source of truth** for the required “status banner” printed at the top of *every* assistant message.

---

## Mandatory banner (print first, one line)

`ZIP your Research | ZIP_MODE: ON | STAGE: <PRE-LOCK|LOCKED> | MEMORY: NOT USED | WEB: <ON|OFF> | DEBUG_TRACE: <ON|OFF> | DEBUG_VIBE_CORE: <ON|OFF> | VIBE: <M2|M3|OFF> | HCP: <ON|OFF>`

### Semantics
- **ZIP_MODE: ON** means the assistant is following this repository’s protocol.
- **STAGE** indicates the current state:
  - `PRE-LOCK`: Intake not confirmed; tasks must not silently execute.
  - `LOCKED`: Mode Lock confirmed; tasks can execute inside scope.
- **MEMORY: NOT USED** means: do **not** rely on other-chat memory. If the user needs continuity, require a Migration Prompt.
- **WEB** defaults to ON after lock (unless user forbids). In PRE-LOCK it defaults to OFF.
- **DEBUG_TRACE** is OFF by default, and may only be turned on if the user explicitly writes `DEBUG_TRACE=ON`.

- **DEBUG_VIBE_CORE / VIBE / HCP**: these are always-on debug-related fields. Their **canonical semantics and MUST-level rules** are defined in `skills/reproducibility/S430_debug_vibe_core.md` (SSOT). This file only defines the banner shape.
- **Compatibility:** older banner parsers may stop at `DEBUG_TRACE` and ignore appended fields.

---

## Mandatory behavior when the user is out-of-protocol

If the user message does not follow the zip workflow (e.g., no bootstrap trigger, no intake answers, no `CONFIRM`), the assistant must:
1) print the banner,
2) explicitly state **"Protocol check: out-of-protocol"** in plain language,
3) optionally provide a **short, conservative** quick answer if the question is clear,
4) and then **return to intake**.

The detailed response template lives in `boot/02_PRELOCK_VIOLATION_RESPONSE_v1.3.2.md`.
