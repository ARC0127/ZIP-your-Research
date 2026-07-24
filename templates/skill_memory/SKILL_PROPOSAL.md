# Dynamic Skill Proposal

`proposal_id` is content-bound. Do not invent it manually. Generate the
proposal with `skill-memory draft`, then show the complete result to the user.

```yaml
schema_version: 1
proposal_id: smp-generated-by-cli
proposer_id: agent-proposer-id
source_trace_ids:
  - trace-example-001
skill:
  id: dyn-contradiction-aware-literature-triage
  name: dyn-contradiction-aware-literature-triage
  description: Procedural memory candidate; requires evaluated promotion.
  retrieval_terms:
    - literature
    - contradiction
    - evidence
  scope: Primary papers and official repositories for one locked question.
  body: |
    # Contradiction-aware literature triage

    ## When to use

    [...]

    ## Procedure

    [...]

    ## Evidence and limits

    [...]

    ## Failure boundaries

    [...]
```

The proposal is `PROPOSED_ONLY`. It is not saved, registered, or active.
