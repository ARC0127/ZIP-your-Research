# 00 Response Status Banner (suite v1.7.0)

This file is the active single source of truth for optional status display.
Version precedence is defined in `docs/VERSION_IDENTITY_v1.7.0.md`.

## Display only on request

Ordinary replies, including Codex commentary and final answers, have no status
banner. Show status when the user asks for it or enables diagnostic output
(such as `DEBUG_TRACE=ON`), using only the fields relevant to that request.
Enabling diagnostics does not require repeating unchanged fields on every reply.
Strict ZIP startup keeps intake and Mode Lock confirmation, without a recurring
banner. This rule supersedes every-message banner wording in legacy guardrails,
state-machine steps, prompt-shield checklists, recovery templates, and skills.

When the full diagnostic line is requested, use this shape:

`ZIP your Research | ZIP_MODE: ON | STAGE: <PRE-LOCK|LOCKED> | MEMORY: <NOT USED|READ-ONLY|ON> | WEB: <ON|OFF> | DEBUG_TRACE: <ON|OFF> | DEBUG_VIBE_CORE: <ON|OFF> | VIBE: <M2|M3|OFF> | HCP: <ON|OFF>`

## Semantics

- `ZIP_MODE: ON` means the assistant is following the ZYR suite v1.7.0
  protocol.
- `STAGE` reports whether Mode Lock is active in this task.
- `MEMORY` reports the actual memory posture; it must not claim use that did
  not occur.
- `WEB` reports whether web access is active for the current task.
- `DEBUG_TRACE` remains opt-in.
- `DEBUG_VIBE_CORE`, `VIBE`, and `HCP` follow
  `skills/reproducibility/S430_debug_vibe_core.md`.

Report actual state only; a printed field never grants permission or proves that
a tool or workflow ran. Historical banner files, including the v1.3.2 path, are compatibility assets.
They do not identify the current suite release.

## Out-of-protocol behavior

Follow the active stage rules and the retained detailed response templates.
Where a retained template filename contains v1.3.2, treat that number as
component lineage under the v1.7.0 release identity.
