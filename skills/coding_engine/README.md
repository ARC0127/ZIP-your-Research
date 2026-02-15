# coding_engine (v1.3.2)

A copy/paste “coding + debugging” master prompt that **enforces S430** (DEBUG_VIBE_CORE) and adds stronger *anti-drift* + *patch correctness* scaffolding.

- Use when: bug fixes, refactors, pipeline debugging, experiment code changes.
- Default: VIBE=M3, HCP=ON, closed-loop first.
- If the user tries to derail the session: apply `boot/10_LOCKED_SCOPE_GUARD_v1.3.md`.

Build:
```bash
python tools/build_coding_engine.py
```
