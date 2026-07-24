# Dynamic Skill Promotion Evaluation

Freeze the same holdout denominator, model, tools, source snapshot, budget, and
grader policy for `NO_SKILL`, `CHAMPION`, and `CHALLENGER`.

```yaml
schema_version: 1
evaluation_id: eval-example-v1
skill_id: dyn-contradiction-aware-literature-triage
candidate_version: 1
grader_id: independent-grader-id
grader_public_key_sha256: <pinned-host-ed25519-key-fingerprint>
grader_signature: <base64-ed25519-signature-over-this-record-without-this-field>
champion_version: null
protocol:
  model_id: model-and-revision
  runtime_artifact:
    path: /absolute/path/runtime-manifest.json
    sha256: <sha256>
  toolset_artifact:
    path: /absolute/path/toolset-manifest.json
    sha256: <sha256>
  source_snapshot_artifact:
    path: /absolute/path/source-snapshot.json
    sha256: <sha256>
  scoring_policy_artifact:
    path: /absolute/path/scoring-policy.json
    sha256: <sha256>
  budget_id: fixed-budget-id
case_results:
  - case_id: H-001
    no_skill_result: FAIL
    champion_result: FAIL
    candidate_result: PASS
    no_skill_artifact:
      path: /absolute/path/H-001-no-skill.json
      sha256: <sha256>
    champion_artifact:
      path: /absolute/path/H-001-no-skill.json
      sha256: <same-as-no-skill-for-first-promotion>
    candidate_artifact:
      path: /absolute/path/H-001-candidate.json
      sha256: <sha256>
  - case_id: H-002
    no_skill_result: FAIL
    champion_result: FAIL
    candidate_result: PASS
    no_skill_artifact:
      path: /absolute/path/H-002-no-skill.json
      sha256: <sha256>
    champion_artifact:
      path: /absolute/path/H-002-no-skill.json
      sha256: <same-as-no-skill-for-first-promotion>
    candidate_artifact:
      path: /absolute/path/H-002-candidate.json
      sha256: <sha256>
negative_mutations:
  - mutation_id: M-001
    detected: true
    artifact:
      path: /absolute/path/M-001-result.json
      sha256: <sha256>
artifact_manifest_sha256: <canonical-hash-of-protocol-cases-and-mutations>
fatal_vetoes: []
verdict: PROMOTE
claim_level: BEHAVIORAL
```

The evaluation harness, not prose generation, must produce the per-arm
artifacts, hash their actual bytes, calculate the canonical manifest hash, and
sign the complete record with the pinned grader/host key. The promotion plan
re-reads every artifact, verifies its hash and signature, and includes every
artifact in `source_sha256`. The host's separate short-lived user-consent
attestation then binds the exact evaluation and artifacts into the mutation.

For the first promotion, `champion_version` is `null` and every CHAMPION result
and artifact hash must equal NO_SKILL. For updates, `champion_version` must
equal the current ACTIVE version. Aggregate pass counts and regressions are
derived from the case rows; self-reported aggregate fields are not accepted.

This record cannot establish scientific improvement by itself.
