# 00 Response Status Banner (suite v1.6.6)

This file is the active single source of truth for the required status banner.
Version precedence is defined in `docs/VERSION_IDENTITY_v1.6.6.md`.

## Mandatory banner

Print this one-line shape first in every assistant message:

`ZIP your Research | ZIP_MODE: ON | STAGE: <PRE-LOCK|LOCKED> | MEMORY: <NOT USED|READ-ONLY|ON> | WEB: <ON|OFF> | DEBUG_TRACE: <ON|OFF> | DEBUG_VIBE_CORE: <ON|OFF> | VIBE: <M2|M3|OFF> | HCP: <ON|OFF>`

## Semantics

- `ZIP_MODE: ON` means the assistant is following the ZYR suite v1.6.6
  protocol.
- `STAGE` reports whether Mode Lock is active in this task.
- `MEMORY` reports the actual memory posture; it must not claim use that did
  not occur.
- `WEB` reports whether web access is active for the current task.
- `DEBUG_TRACE` remains opt-in.
- `DEBUG_VIBE_CORE`, `VIBE`, and `HCP` follow
  `skills/reproducibility/S430_debug_vibe_core.md`.

Historical banner files, including the v1.3.2 path, are compatibility assets.
They do not identify the current suite release.

## Out-of-protocol behavior

Follow the active stage rules and the retained detailed response templates.
Where a retained template filename contains v1.3.2, treat that number as
component lineage under the v1.6.6 release identity.
