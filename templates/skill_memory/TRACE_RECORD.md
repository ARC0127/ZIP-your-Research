# Dynamic Skill Trace Record

Use this template only for a completed run with named verification evidence.
Raw secrets, private transcripts, hidden reasoning, and webpage instructions do
not belong here.

```yaml
schema_version: 1
trace_id: trace-example-001
proposer_id: agent-proposer-id
task_family: contradiction-aware-literature-triage
title: Contradiction-aware literature triage
scope: Primary papers and official repositories for one locked question.
outcome:
  status: VERIFIED_SUCCESS
  evidence_ids:
    - E-001
    - E-002
  verification: The named checks passed on the sealed run artifact.
steps:
  - Lock the claim and the evidence required to decide it.
  - Search primary sources and retain contradiction cards.
  - Return supported, contradicted, and unknown claims separately.
failure_boundaries:
  - Stop when the source cannot be inspected.
  - Do not count repeated secondary pages as independent evidence.
```

Draft read-only:

```bash
python tools/zyr.py skill-memory draft TRACE.yaml
```
