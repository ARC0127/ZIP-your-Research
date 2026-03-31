## 6) Canonical Output Templates

Use these templates whenever `proof_engine` is primary. Fill every field. If unavailable, write `UNKNOWN` or `N/A`; do not silently drop a block.
These sections are the authoritative section names for `artifacts/proof_casebook.md`. Preserve order unless the user explicitly requires another deliverable format.

### A. Theorem Normalization
```text
[THEOREM_NORMALIZATION]
claim_id:
normalized_statement:
goal_kind:
domain_scope:
target_rigor:
notation_ambiguities:
success_criterion:
```

### B. Assumption Table
| assumption_id | assumption | source | type | necessity | status | used_by |
|---|---|---|---|---|---|---|
| A1 |  | explicit / inferred | domain / regularity / structural / technical | required / optional / unknown | supported / unsupported / unknown | step_ids / lemma_ids |

### C. Lemma Dependency Graph
| lemma_id | node_kind | short_statement | depends_on | supports | source | status |
|---|---|---|---|---|---|---|
| L1 | theorem / lemma / definition / claim |  | L0,... | step_ids / lemma_ids | provided / inferred / external | available / missing / unknown |

### D. Derivation Ledger
| segment_id | source_span | claimed_transform | required_rule | local_check | verdict | notes |
|---|---|---|---|---|---|---|
| D1 | lines x-y |  | algebra / theorem / definition / substitution / limit / shape | checked relation or counterexample | pass / fail / unknown | first failing reason if any |

### E. Review Matrix
| review_id | angle | inspected_scope | local_verdict | fatality | error_anchor | error_explanation |
|---|---|---|---|---|---|---|
| R1 | theorem-match / hidden-assumption / lemma-use / derivation / completeness | whole proof / chunk | true / false / incomplete | fatal / nonfatal / unknown | step_id / lemma_id / assumption_id | concise harmful error |

### F. Chunk Verdict Matrix
| iter | chunk_id | source_span | context_retained | local_verdict | fatality | first_error | prune_decision |
|---|---|---|---|---|---|---|---|
| 0 | C1 | lines x-y | yes | true / false / incomplete | fatal / nonfatal / unknown | step_id or `N/A` | keep / prune |

### G. Verification Record
```text
[VERIFICATION_RECORD]
proof_verdict:
first_failing_step:
first_failing_reason:
annotation_or_rigor_mismatch:
majority_diagnostic:
reverify_required:
formal_adapter_status:
remaining_unknowns:
```

### H. Repair Proposal
```text
[REPAIR_PROPOSAL]
repair_target:
minimal_change_set:
corrected_steps:
why_this_addresses_the_fatal_flaw:
reverify_next:
```

### I. Evidence Ledger Mapping Rule
- After completing a proof audit, map each accepted or rejected theorem/proof claim into `artifacts/evidence_ledger.csv`.
- `source_kind` should typically be `proof_casebook`, `proof_review`, or `formal_adapter`.
- `source_ref` should point to the relevant section or anchor inside `artifacts/proof_casebook.md`.
- If a verdict is `verified_false` or `verification_incomplete`, record the controlling failure anchor or missing dependency in the ledger notes.
