## 7) Long-Proof Audit Examples

These are canonical output examples for GPT-5.4 / Codex style execution. Reuse the structure; do not collapse it into a paragraph.

### Example A: Fatal Flaw (theorem-condition mismatch)
```text
[THEOREM_NORMALIZATION]
claim_id: THM1
normalized_statement: For every continuous function f on [0,1], ...
goal_kind: theorem_verification
domain_scope: continuous functions on a compact interval
target_rigor: paper-level rigorous proof
notation_ambiguities: N/A
success_criterion: every theorem use must match the stated assumptions
```

| assumption_id | assumption | source | type | necessity | status | used_by |
|---|---|---|---|---|---|---|
| A1 | f is continuous on [0,1] | explicit | regularity | required | supported | L2, D4 |
| A2 | f is differentiable on (0,1) | inferred | regularity | required | unsupported | L2 |

| lemma_id | node_kind | short_statement | depends_on | supports | source | status |
|---|---|---|---|---|---|---|
| L1 | theorem | Extreme value theorem | A1 | D2 | external | available |
| L2 | theorem | Mean value theorem | A1, A2 | D4 | inferred | unavailable |

| review_id | angle | inspected_scope | local_verdict | fatality | error_anchor | error_explanation |
|---|---|---|---|---|---|---|
| R1 | theorem-match | whole proof | false | fatal | L2 / D4 | The proof invokes MVT but differentiability is never established. |
| R2 | hidden-assumption | whole proof | false | fatal | A2 | The proof silently upgrades continuity to differentiability. |
| R3 | derivation | D1-D5 | incomplete | unknown | D4 | Local derivation depends on an unsupported theorem call. |

```text
[VERIFICATION_RECORD]
proof_verdict: verified_false
first_failing_step: D4
first_failing_reason: unsupported use of the mean value theorem
annotation_or_rigor_mismatch: none
majority_diagnostic: non_binding; even if some reviews look acceptable, one fatal flaw is sufficient
reverify_required: no
formal_adapter_status: not_requested
remaining_unknowns: whether a differentiability assumption was omitted from the theorem statement
```

### Example B: Rigor Mismatch (cannot force a fake pass)
```text
[THEOREM_NORMALIZATION]
claim_id: THM2
normalized_statement: If sequence x_n converges and a subsequence argument is used, prove uniqueness of the limit.
goal_kind: proof_audit
domain_scope: real analysis
target_rigor: thesis/paper-level
notation_ambiguities: N/A
success_criterion: hidden steps must be justified, not just sketched
```

| step_id | claim_or_transition | required_support | local_verdict | fatality | explanation |
|---|---|---|---|---|---|
| S1 | Assume x_n -> a and x_n -> b | definition of convergence | pass | nonfatal | Assumptions are clear. |
| S2 | “It is obvious that a=b.” | epsilon argument or standard uniqueness lemma | unknown | major | The needed justification is omitted. |

```text
[FIRST_FAILING_STEP]
step_id: S2
reason: rigor target requires an explicit uniqueness argument, but the proof supplies only an assertion
```

```text
[VERIFICATION_RECORD]
proof_verdict: verification_incomplete
first_failing_step: S2
first_failing_reason: omitted justification under current rigor target
annotation_or_rigor_mismatch: dataset-style grading may allow this; paper-level audit does not
majority_diagnostic: non_binding; permissive grading norms cannot override the locked rigor target
reverify_required: yes, after the missing epsilon argument is supplied
formal_adapter_status: not_requested
remaining_unknowns: whether the user wants contest-grade or paper-grade rigor
```

### Example C: Repair Then Re-verify
```text
[THEOREM_NORMALIZATION]
claim_id: THM3
normalized_statement: For all n in N, sum_{i=1}^n i = n(n+1)/2.
goal_kind: proof_repair_and_reverify
domain_scope: natural numbers
target_rigor: classroom-to-paper rigorous
notation_ambiguities: N/A
success_criterion: induction base case and induction step must both be explicit
```

| segment_id | source_span | claimed_transform | required_rule | local_check | verdict | notes |
|---|---|---|---|---|---|---|
| D1 | lines 1-2 | base case omitted | induction base | direct inspection | fail | No base case supplied. |
| D2 | lines 3-6 | k -> k+1 algebra | induction hypothesis + algebra | checked | pass | Algebra is fine once the base case exists. |

```text
[FIRST_ERROR_REPORT]
review_id: R1
error_anchor: D1
reason: the proof claims induction but omits the base case
```

```text
[REPAIR_PROPOSAL]
repair_target: D1
minimal_change_set: add the base case n=1 before invoking the induction hypothesis
corrected_steps:
1. Base case: n=1 gives 1 = 1(2)/2.
2. Assume sum_{i=1}^k i = k(k+1)/2.
3. Then sum_{i=1}^{k+1} i = k(k+1)/2 + (k+1) = (k+1)(k+2)/2.
why_this_addresses_the_fatal_flaw: the repaired proof closes the missing induction anchor and preserves the valid step case
reverify_next: yes
```

```text
[VERIFICATION_RECORD]
proof_verdict: verified_true
first_failing_step: D1 (original proof only)
first_failing_reason: missing base case in the original proof
annotation_or_rigor_mismatch: none
majority_diagnostic: non_binding
reverify_required: completed
formal_adapter_status: not_requested
remaining_unknowns: none after repaired proof is re-verified
```
