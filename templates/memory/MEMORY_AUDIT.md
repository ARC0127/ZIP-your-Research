# MEMORY_AUDIT

Append content-minimized events. Do not copy secrets or full sensitive record
content into the audit log.

| Event ID | Memory/proposal ID | Action | Project scope | Actor/host | Consent ID | From status | To status | Target | Outcome | Time | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| | | propose/approve/save/read/supersede/dispute/revoke/export/delete/cache-rebuild | | | | | | | | | |

## Audit rules

- Record failed and partial operations.
- `READ` events identify the memory ID and reason, not hidden chain-of-thought.
- A hash is an integrity aid, not proof of truth or authorization.
- After verified deletion, retain only an opaque event when policy permits.
- If copies or backups were not inspected, record `DELETION_UNVERIFIED`.
