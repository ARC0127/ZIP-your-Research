## 2) Pessimistic Verification

Use `S240` semantics.

### Core workflow
1) Normalize theorem + assumptions.
2) Run multiple independent reviews on the same proof.
3) Each review must try to find a fatal flaw from a different angle:
   - theorem-condition mismatch
   - hidden assumption
   - invalid lemma application
   - algebra/derivation error
   - circularity / missing case
4) If **any** review reports a fatal error, set the global verdict to `verified_false`.
5) Keep majority vote only as `diagnostic_majority_vote`.

### Output requirements
- `review_matrix` with columns:
  - `review_id`
  - `angle`
  - `inspected_scope`
  - `local_verdict`
  - `fatality`
  - `error_anchor`
  - `error_explanation`
- `first_error_report`
- `proof_verdict`
- `verification_record`

### Error policy
- Harmless typo or corrected notation issue: do not reject the proof.
- Fatal flaw: reject and explain the harmful step, condition, or lemma mismatch.
- Missing evidence: return `verification_incomplete`, not `verified_true`.

### Required review angles
Unless clearly inapplicable, include these review angles:
1) theorem-condition match
2) hidden assumption scan
3) lemma application validity
4) local derivation / algebra check
5) completeness / missing case / circularity
