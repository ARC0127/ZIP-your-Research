# Public Evolution Mutation Fixtures v1

This directory contains public, deterministic fixtures for testing whether a
research orchestrator preserves epistemic boundaries while an idea moves
through retrieval, candidate generation, proof, experiment, writing, figures,
and memory.

## Fixture design

`public_mutations_v1.jsonl` contains 12 paired cases:

- one `mutation` that introduces a specific scientific or governance defect;
- one `clean` twin that preserves the same topic while removing that defect.

The clean twin is part of the oracle. It prevents an evaluator from rewarding
an implementation that rejects every input. Passing these public fixtures
means distinguishing the paired cases and taking the expected bounded action;
it does not establish scientific validity or general performance.

The 12 mutation families cover:

1. primary-source downgrade;
2. false agent independence and suppressed disagreement;
3. cosmetic candidate diversity;
4. scope or denominator drift;
5. silent assumption deletion;
6. circular or non-universal proof;
7. data leakage or unfair baseline comparison;
8. post-hoc result selection;
9. claim escalation during rendering;
10. topical but non-entailing citation;
11. visually attractive but misleading figure;
12. unauthorized or instruction-bearing memory.

## JSONL schema

Each line is one JSON object with these fields:

| Field | Meaning |
|---|---|
| `schema_version` | Fixture schema version. |
| `case_id` | Unique case identifier. |
| `pair_id` | Identifier shared by the mutation and clean twin. |
| `variant` | `mutation` or `clean`. |
| `domain` | Earliest research state affected by the case. |
| `title` | Short description for maintainers. |
| `input` | The only field that should be shown to the system under test. |
| `expected_action` | Bounded oracle action. |
| `must_detect` | Concepts required in a correct evaluation. |
| `must_not_claim` | Claims forbidden in a correct evaluation. |
| `oracle` | Human-readable reason for the expected action. |

Do not expose `variant`, `expected_action`, `must_detect`, `must_not_claim`, or
`oracle` to the system under test. These are evaluator-side labels. A semantic
runner should pass only `input`, capture the resulting artifact, and let a
separate oracle score the artifact.

## Action vocabulary

- `REOPEN`: return to the earliest affected research state, retain the defect
  in the objection or failed-path ledger, and withhold the affected claim.
- `PROCEED`: continue without inventing a defect, while preserving the
  explicitly stated boundary or limitation.

An implementation must not infer that `PROCEED` means a scientific claim is
verified. Structural conformance, behavior on these fixtures, and scientific
validity are separate statuses.

## Reporting

Report results per pair and per mutation family. Include false negatives on
mutations and false positives on clean twins. The fixed 12/12 set is a public
regression fixture, not a universal zero-error guarantee. Add private
paraphrases, changed numbers, and domain-specific cases when using these
fixtures in a serious evaluation.

Run the deterministic fixture and boundary checks with:

```bash
python3 -m unittest tests.evolution.test_public_mutations_v1
```
