# LONG_TERM_MEMORY

Authoritative user-approved Markdown records for one project namespace.

```yaml
schema_version: visible-memory-v1
project_scope: ""
storage_target: ""
created_at: ""
updated_at: ""
derived_cache: NONE | APPROVED
```

## Storage policy

| Field | Value |
|---|---|
| Intended purpose | |
| Default retention | |
| Review cadence | |
| Allowed sensitivities | `PUBLIC / INTERNAL / SENSITIVE` |
| Cross-project retrieval | `DENY_BY_DEFAULT` |
| Secret storage | `PROHIBITED` |

## Record index

| Memory ID | Type | Short label | Status | Validity | Source | Consent ID | Review after |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

## Record template

Copy for each record.

```yaml
memory_id: ""
record_type: FACT | INFERENCE | HYPOTHESIS | DECISION | FAILED_PATH | OPEN_QUESTION | PREFERENCE
project_scope: ""
content: ""
source_refs: []
created_at: ""
valid_from: ""
valid_to: ""
verification_status: VERIFIED | PLAUSIBLE | NOT_RUN | REFUTED
status: ACTIVE | HISTORICAL | DISPUTED | SUPERSEDED | REVOKED | EXPIRED | QUARANTINED
sensitivity: PUBLIC | INTERNAL | SENSITIVE
consent_id: ""
supersedes: []
conflicts_with: []
review_after: ""
retention: ""
```

### Evidence and boundary

- Exact source span or artifact:
- Assumptions:
- Scope where the record is valid:
- Counterevidence:
- Reverification action:

## Conflicts and current view

| Conflict ID | Record IDs | Conflict type | Current handling | User decision required |
|---|---|---|---|---|
| | | correction/scope/contradiction/duplicate/unverifiable | | |

Do not remove conflicting source records merely to simplify the current view.
