# 09 Intake Depth Policy v1.0.1

- tight: minimal questions (A/B/C/E: 2 each; others: 1 each)
- standard: moderate (A/B/C/E: 3 each; others: 2 each)
- deep (default): thorough (A/B/C/E: 5 each; others: 3 each)

If the user sets `SESSION_OVERRIDES.intake_depth`, follow it exactly.


## Guardrail
Setting `intake_depth=tight` only changes *how many questions are asked*.
It does NOT skip:
1) Mode Lock generation, and
2) waiting for user `CONFIRM`.

Do not execute tasks while Mode Lock is not active.
