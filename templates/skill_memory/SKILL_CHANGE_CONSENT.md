# Dynamic Skill Change Consent

## Read-only plan

- Operation:
- Dynamic Skill ID:
- Candidate or rollback version:
- Absolute dynamic root:
- Before registry SHA-256:
- After registry SHA-256:
- Proposal/evaluation source SHA-256:
- Exact write paths and content hashes:
- Exact delete paths:
- Prepared journal path:
- Signed authorization receipt path:
- Full Skill preview inspected: YES / NO / NOT_APPLICABLE
- External copies or backups in scope:
- Consent ID:
- Pinned host Ed25519 public-key fingerprint:
- Host attestation ID:
- Host actor ID:
- Attestation issue/expiry time:

## Required user response

```text
APPROVE zyr-smc-...
```

The text response is a user-interface signal, not an authorization capability.
The trusted host must turn it into a short-lived Ed25519-signed JSON
attestation bound to the exact consent ID. The private key must remain outside
model and tool access. `apply` rejects missing, expired, forged, wrong-key, or
wrong-plan attestations.

After apply, the managed store retains the public key and the signed
attestation in the deterministic authorization receipt shown above. The private
key is never stored by ZYR.

```json
{
  "schema_version": 1,
  "kind": "ZYR_SKILL_MEMORY_USER_CONSENT",
  "attestation_id": "att-host-generated-id",
  "actor_id": "trusted-host:user-id",
  "decision": "APPROVE",
  "plan_consent_id": "zyr-smc-...",
  "public_key_sha256": "<pinned-key-fingerprint>",
  "issued_at": "2026-01-01T00:00:00Z",
  "expires_at": "2026-01-01T00:05:00Z",
  "nonce": "<at-least-16-url-safe-characters>",
  "signature": "<base64-ed25519-signature-over-canonical-json-without-signature>"
}
```

Approval is valid only for the exact plan above. It does not authorize Git
staging, commit, push, upload, sync, model changes, canonical ZYR changes, or a
different Skill operation.
