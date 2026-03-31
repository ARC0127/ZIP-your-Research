# 02 Migration Detector v1.3.2

If the user's first message contains a block that starts with:
- `MIGRATION PROMPT (v1.5)`
- `MIGRATION PROMPT (v1.3.2)` (or older versions)

Then:
1) Treat it as authoritative.
2) Do not re-run deep intake unless the migration prompt says so.
3) If it is v1.5, recover:
   - locked constraints
   - artifact inventory
   - completed checks
   - open issues
   - next executable step
4) Continue with Mode Lock verification and execution.

If no migration prompt is provided:
- The user can reply `NO-MIGRATION` (recommended).
- Proceed with the standard bootstrap flow.
