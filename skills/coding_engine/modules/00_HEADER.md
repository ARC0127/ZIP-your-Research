## Coding Engine: Operating Rules

> **Normative rules:** `skills/reproducibility/S430_debug_vibe_core.md` + `boot/10_LOCKED_SCOPE_GUARD_v1.3.md`.

This section defines the default operating posture for code tasks: minimal viable implementation, diff-first patches, and closure-first verification.

- Always produce a runnable command path (one command, no hidden steps).
- Prefer deleting redundant code over adding new flags.
- If evidence is missing, mark UNKNOWN and request the minimal missing artifact.

