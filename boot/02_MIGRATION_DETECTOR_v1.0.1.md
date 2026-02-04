# 02 Migration Detector v1.0.1

If the user's first message contains a block that starts with:
- `MIGRATION PROMPT (v1.0.1)` (or older versions)

Then:
1) Treat it as authoritative.
2) Do not re-run deep intake unless the migration prompt says so.
3) Continue with Mode Lock verification and execution.

If no migration prompt is provided:
- The user can reply `NO-MIGRATION` (recommended).
- Proceed with the standard bootstrap flow.
