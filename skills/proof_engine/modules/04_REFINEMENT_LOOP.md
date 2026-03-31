## 4) Reviewer-Feedback Refinement Loop

This engine supports proof repair, but repair is never confused with verification.

### Rules
- If the current proof is `verified_false`, you MAY propose a corrected self-contained proof.
- The corrected proof MUST address the recorded fatal flaw, not merely paraphrase the old proof.
- The corrected proof MUST be re-verified before any completion claim.
- If you provide a repair, emit it under `REPAIR_PROPOSAL` and keep `VERIFICATION_RECORD` separate.

### State machine
- `verified_true`: proof passed the current verification profile.
- `verified_false`: a fatal flaw was found.
- `verification_incomplete`: evidence, assumptions, or rigor target are insufficient.

### Non-negotiable boundary
- `repair proposal` is not `verified proof`.
- `gap list` is not `verification complete`.
- `formal sketch` is not `verified proof`.
- `corrected proof draft` is not `verified_true` until re-check is recorded.
