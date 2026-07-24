# ZYR Dynamic Skill Memory Protocol v1

Status: normative P0 protocol for user-generated procedural memory

Canonical implementation: `tools/zyr_lib/skill_memory.py`

Canonical operator skill: `skills/research_orchestrator/S661_dynamic_skill_memory.md`

## 1. Purpose

Dynamic Skill memory turns a verified task trace into a reusable procedural
candidate without changing model weights. It supports governed creation,
evaluation, promotion, versioned update, rollback, deprecation, retrieval, and
deletion.

The governing equation is:

```text
automatic candidate generation
!= automatic persistence
!= automatic registration
!= automatic activation
!= automatic deletion
```

A completed task is only evidence that a candidate may be worth evaluating.
It is not evidence that the workflow caused the success, generalizes to new
tasks, improves scientific quality, or is safe to activate.

This protocol extends
`docs/memory/VISIBLE_MEMORY_PROTOCOL_v1.md`. If the two conflict, the stricter
consent, deletion, privacy, or evidence boundary wins.

## 2. Research basis and DojoAgents audit

The implementation was informed by first-party papers, repositories, package
metadata, and documentation inspected on 2026-07-24.

| Source | Useful idea | Boundary adopted by ZYR |
|---|---|---|
| [DojoAgents 0.1.8 on PyPI](https://pypi.org/project/dojoagents/) | Treat reusable workflows as procedural Skill memory; expose create, edit, and delete operations. | Concept only. The current PyPI release has no source distribution or declared project URL. ZYR does not treat its marketing claim as behavioral evidence. |
| [MemSkill paper](https://arxiv.org/abs/2602.02474) and [official code](https://github.com/ViktorAxelsen/MemSkill) | Controller selects memory skills; executor applies them; designer uses hard cases to refine or add skills. | Hard-case learning and selection are separated from activation. MemSkill's “memory skills” are meta-memory operations, not automatically equivalent to ZYR task-workflow Skills. |
| [Memento-Skills](https://github.com/Memento-Teams/Memento-Skills) | `Read -> Execute -> Reflect -> Write`, utility-aware retrieval, repair, and persistent versions. | Reflection proposes a challenger; it does not overwrite the champion. |
| [Acontext](https://github.com/memodb-io/Acontext) | Human-readable Skill files, progressive disclosure, and portable downloads. | Markdown remains inspectable authority; derived search structures are disposable. |
| [OpenAI Agents SDK memory](https://openai.github.io/openai-agents-js/guides/sandbox-agents/memory/) | Separate extraction from consolidation; use progressive disclosure; isolate layouts; allow read-only memory. | Candidate extraction and registry consolidation remain separate phases. Namespaces cannot silently share memory. |
| [Agent Skills specification](https://agentskills.io/specification) | `SKILL.md` is a portable capability format and may include executable support files or preauthorized tools. | P0 permits declarative Markdown only. Generated scripts, executable assets, runtime installs, and `allowed-tools` are rejected. |

### 2.1 Static DojoAgents wheel observation

The official PyPI JSON reported version `0.1.8` and wheel SHA-256:

```text
42de5f64bbfd5cded328cf15e3342185ca79db5bce1d700d5fd0771ff9c05988
```

The wheel was downloaded, hash-verified, unpacked, and inspected without
installation or execution. The inspected implementation:

- configured a generated-Skill directory under `~/.dojo/skills/generated`;
- wrote a session message summary into a generated `SKILL.md`;
- exposed list/create/edit/patch/delete and support-file operations;
- loaded generated and user Skills into a lazy Skill catalog.

In the inspected path, ZYR did not find a reliable success classifier,
baseline/challenger evaluation, immutable version chain, rollback record,
write-specific user consent, deletion receipt, or promotion gate. The generated
directory and the management tool's main write root were also distinct.

Therefore, DojoAgents is a useful product-direction reference but not a safe
implementation template. ZYR uses a clean-room design and copies no package
code.

## 3. Memory classes

ZYR keeps four objects distinct:

1. **episodic trace** — what happened in one run;
2. **factual memory** — stable facts, decisions, source locators, and open
   questions governed by the visible-memory protocol;
3. **procedural Skill memory** — a reusable “when and how” workflow;
4. **meta-memory policy** — rules for extraction, retrieval, consolidation,
   evaluation, forgetting, and deletion.

Dynamic Skill memory is class 3. It may reference trace and evidence IDs but
must not copy raw transcripts, credentials, private source content, hidden
reasoning, or untrusted webpage instructions.

## 4. Authority and storage boundary

The built-in ZYR repository and the user's dynamic Skill store are physically
and logically separate.

```text
ZYR source repository
  skills_manifest.yaml        # built-in canonical Skills; immutable here
  skills/...                  # Sxxx and composite Skills

explicit user-selected dynamic root
  registry.yaml               # machine authority for dynamic state
  skills/<dyn-id>/versions/   # immutable version payloads
  active/<dyn-id>/SKILL.md    # derived active projection
  audit/events.jsonl          # content-free projection of registry events
  audit/authorizations/       # signed plan/attestation receipts per event
  trust/consent_public_key.pem # pinned public verification key
  index/skill_catalog.json    # rebuildable retrieval index
  journal/PREPARED.json       # transient crash-recovery marker
  journal/quarantine/         # same-volume reversible delete staging
```

Hard rules:

- the root must be explicit, outside the ZYR source repository, and not a
  filesystem root or home directory;
- only IDs matching `dyn-*` are accepted;
- `Sxxx`, composite engines, manifests, validators, system prompts, and host
  policy are protected canonical objects;
- dynamic operations accept object IDs, not arbitrary target paths;
- symlinks, junctions, path traversal, hardlinks, and non-canonical stores fail
  closed;
- user-generated stores, traces, registries, audit logs, indexes, and
  embeddings are never release-package inputs.

## 5. Lifecycle

```text
trace
  -> PROPOSED_ONLY
  -> user-approved CREATE
  -> PILOT
  -> independent three-arm evaluation
  -> user-approved PROMOTE
  -> ACTIVE
  -> UPDATE creates a new PILOT while ACTIVE remains unchanged
  -> PROMOTE, ROLLBACK, or DEPRECATE
  -> user-approved DELETE
  -> DELETED tombstone
```

### 5.1 `PROPOSED_ONLY`

`draft` is read-only. It accepts one structured trace only when the outcome is
`VERIFIED_SUCCESS`, then renders:

- a stable `dyn-*` ID;
- portable `SKILL.md` content with only `name` and `description` front matter;
- retrieval terms and a bounded scope;
- procedure, evidence limits, and failure boundaries;
- a content-bound `proposal_id`.

A failed, unverified, injected, secret-bearing, executable, or destructive
trace is rejected. Drafting does not create a directory or registry.

### 5.2 `PILOT`

`create` and `update` require an exact read-only plan and a second,
operation-specific consent. A created version enters `PILOT`. An update adds an
immutable challenger version and does not change the current `ACTIVE` pointer.

PILOT content is not returned by normal active retrieval.

### 5.3 `ACTIVE`

Promotion requires an independent evaluation record over one frozen
denominator:

```text
NO_SKILL   # dynamic Skill disabled
CHAMPION   # current ACTIVE version, or NO_SKILL for first promotion
CHALLENGER # candidate PILOT version
```

The same cases, model, tools, source snapshot, budget, and scoring policy must
be used for all arms. P0 requires:

- at least two unique holdout cases;
- grader identity different from proposer identity, with the complete
  evaluation signed by the pinned host Ed25519 key;
- a frozen protocol containing model, runtime, toolset, source-snapshot,
  scoring-policy, and budget identities;
- one row per case with PASS/FAIL plus an external artifact path and verified
  byte-level SHA-256 for all three arms;
- challenger passes derived from those rows and greater than both NO_SKILL and
  CHAMPION;
- all declared negative mutations detected with inspected artifact paths and
  byte-level hashes;
- zero derived CHAMPION-to-CHALLENGER regressions;
- a content-bound artifact-manifest hash, all artifact hashes included in the
  mutation plan's source binding, and no fatal vetoes;
- verdict `PROMOTE`;
- claim level exactly `BEHAVIORAL`.

Any fabricated citation, unsupported claim strengthening, data leak, secret
write, unapproved persistence, consent bypass, or canonical-Skill mutation is
a fatal veto. A behavioral promotion is not evidence of scientific
improvement.

### 5.4 `ROLLBACK` and `DEPRECATED`

Rollback changes the active pointer to an existing immutable prior version.
It creates no new content.

Deprecation removes the active projection and all normal retrieval visibility
while retaining version payloads for inspection or later deletion. Low usage
alone is not a deletion criterion.

### 5.5 `DELETED`

Delete is distinct from deprecate and rollback. The plan shows every exact
dynamic payload and active-projection directory that will be removed.

On apply:

1. the consent ID, Ed25519 host attestation, source hashes, registry hash, and
   root identity are checked;
2. an exclusive store lock with a random ownership token is held and the plan
   is recomputed;
3. a `PREPARED` journal records before/after hashes, planned writes, exact
   delete identities, and quarantine mappings;
4. target directories are atomically moved on the same volume into
   `journal/quarantine/`, then their identity and tree hash are rechecked;
5. registry, audit projection, and retrieval index are rebuilt, with registry
   authority committed last;
6. the registry keeps only a content-free `DELETED` tombstone;
7. closed-loop verification runs before quarantine and the journal are
   cleared.

If execution stops, ordinary plans fail closed. A separately planned,
host-attested `recover` operation deterministically rolls back when the
registry still has the before-hash, or rolls forward when it has the
after-hash. It refuses any third state.

The tombstone prevents accidental ID reuse and does not retain the Skill body,
description, scope, retrieval terms, or source trace. Previously exported
bundles, Git history, backups, cloud copies, and third-party indexes are outside
the local deletion proof. If they were not inspected, report
`DELETION_UNVERIFIED`.

## 6. Two-phase consent

All mutations use:

```text
PLAN  -> read-only exact paths, hashes, preview, deletes, and consent ID
APPLY -> same operation and sources plus exact consent ID and host attestation
```

The consent ID binds:

- operation;
- absolute dynamic root and root identity;
- Skill ID and version;
- before/after registry hashes;
- proposal or evaluation source hashes;
- every planned write path, content hash, and size;
- every planned delete path;
- prepared-journal destination;
- event sequence, event hash, and deterministic authorization-receipt path.

If any source, registry, root identity, target, operation, or version changes,
the ID changes and apply fails before mutation. A generic earlier `CONFIRM`
does not authorize a Skill operation. The trusted host must show the plan,
receive the exact `APPROVE zyr-smc-...` response from the user, and issue a
short-lived Ed25519 attestation over that exact plan. The key fingerprint is
pinned when the store is created. Subsequent operations reject another key.

The consent ID is an integrity binding, not an authentication secret. The host
private key must remain inaccessible to the proposing model and its tools.
Missing, expired, forged, wrong-key, and wrong-plan attestations fail closed.

Apply persists the public verification key and one detached signed
authorization receipt per lifecycle event. `verify` recomputes each consent ID,
verifies every Ed25519 signature, rejects attestation-ID or nonce reuse, binds
the latest signed plan to the complete current registry hash, and then checks
payload, active projection, audit, index, and whole-store closure. This detects
post-consent edits even when an attacker rebuilds visible hashes and derived
files without the host private key.

No local-only design can detect restoration of a complete earlier valid store
snapshot when the attacker can replace every file. Hosts that require
anti-rollback guarantees must externally anchor the latest consent ID or
registry hash in an append-only or monotonic system.

## 7. CLI contract

Read-only commands:

```bash
python tools/zyr.py skill-memory draft TRACE.yaml
python tools/zyr.py skill-memory plan create \
  --root ROOT \
  --proposal PROPOSAL.yaml \
  --trusted-consent-public-key HOST_PUBLIC_KEY.pem
python tools/zyr.py skill-memory list --root ROOT
python tools/zyr.py skill-memory search --root ROOT --query "query"
python tools/zyr.py skill-memory verify --root ROOT
```

Mutating commands:

```bash
python tools/zyr.py skill-memory apply create \
  --root ROOT \
  --proposal PROPOSAL.yaml \
  --trusted-consent-public-key HOST_PUBLIC_KEY.pem \
  --consent-id zyr-smc-... \
  --consent-attestation HOST_SIGNED_CONSENT.json

python tools/zyr.py skill-memory apply promote \
  --root ROOT \
  --skill-id dyn-example \
  --version 1 \
  --evaluation EVALUATION.yaml \
  --trusted-consent-public-key HOST_PUBLIC_KEY.pem \
  --consent-id zyr-smc-... \
  --consent-attestation HOST_SIGNED_CONSENT.json
```

`update`, `rollback`, `deprecate`, and `delete` use the same `plan` then
`apply` contract. An interrupted transaction uses `plan recover` and `apply
recover`, with a new host attestation. Plan is always the default mental model;
no mutation command may infer approval from task execution.

## 8. Retrieval

P0 uses a deterministic lexical metadata index and progressive disclosure:

```text
query
-> ACTIVE-only metadata filter
-> term match over ID, description, and approved retrieval terms
-> whole-store closure plus active/version hash verification
-> return exact active SKILL.md path
-> load the body only when selected
-> recheck registry state and content hash
```

The index is derived. `registry.yaml` plus immutable version payloads are the
authority.

### 8.1 Transformer retrieval adapter for P1

An optional fast Transformer path may be added without changing authority:

```text
namespace and ACTIVE filter
-> sparse lexical recall
-> bi-encoder approximate recall
-> reciprocal-rank fusion
-> cross-encoder rerank for the small candidate set
-> policy and version filter against registry.yaml
-> progressive disclosure of selected SKILL.md
```

Required safeguards:

- embeddings contain approved Skill text only, never raw traces or secrets;
- namespace, user, project, model, encoder version, and content hash are part
  of index identity;
- deleted/deprecated IDs are filtered after retrieval, not only removed from
  the vector database;
- all dense indexes are rebuildable and receive deletion cascade tests;
- similarity is a routing signal, not evidence of truth or utility;
- lexical retrieval remains a deterministic fallback;
- model or encoder changes trigger re-evaluation, not silent utility carryover.

## 9. Web and Agentic App behavior

### Web host

- generate the proposal, evaluation, or export as a user-triggered UTF-8
  Markdown/YAML/ZIP download;
- do not write to server-local persistent memory in the background;
- do not upload it elsewhere without a separate destination-specific consent;
- deletion can only cover server-side objects the host can identify and verify.

### Codex or another local Agentic App

- show the full Skill preview, exact absolute dynamic root, write/delete list,
  hashes, and consent ID;
- wait for write-specific approval;
- apply locally through the governed manager;
- verify registry, payload, active projection, audit, index, and journal state;
- do not stage, commit, push, sync, or publish the store unless separately
  requested.

## 10. Security gates

P0 rejects:

- prompt-override and authority-escalation text;
- known credential/private-key patterns;
- executable code fences, runtime package installation, preauthorized tools,
  and download-to-shell patterns;
- destructive root-delete instructions;
- embedded approval UI or approval-spoofing content;
- NUL bytes, excessive field sizes, duplicate IDs, and oversized stores;
- source-repository targets, filesystem roots, home directories, traversal,
  symlinks, junctions, hardlinks, or stale locks;
- unsigned/expired consent, lock replacement, unexpected support files,
  ambiguous YAML, and unresolved PREPARED transactions;
- missing, forged, replayed, or registry-mismatched persisted authorization
  receipts;
- updates to deleted IDs and reuse of deleted tombstones;
- promotion without host-bound, per-case, fixed-denominator behavioral
  artifacts.

Relevant threat references include the
[OWASP Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html),
[CWE-22 Path Traversal](https://cwe.mitre.org/data/definitions/22.html),
[CWE-59 Link Following](https://cwe.mitre.org/data/definitions/59.html), and
[CWE-367 TOCTOU](https://cwe.mitre.org/data/definitions/367.html).

## 11. Evidence and release boundary

Report the following separately:

- `STRUCTURAL`: schemas, paths, hashes, state transitions, tests, and package
  checks;
- `BEHAVIORAL`: outcomes on named executed cases, including negative mutations
  and deletion cascade;
- `SCIENTIFIC`: evidence that a Skill improves a bounded scientific outcome
  under a frozen independent protocol.

Passing P0 tests establishes structural and named-case behavioral properties.
It does not establish general research improvement, independent replication,
or model self-improvement.

## 12. P0 and P1

P0:

- verified-trace candidate drafting;
- Markdown-only Skills;
- external registry and immutable versions;
- plan/apply consent;
- pinned-key Ed25519 host attestation;
- PILOT/ACTIVE separation;
- three-arm promotion gate;
- update, rollback, deprecate, and deletion;
- content-free event projection and tombstone plus signed authorization
  receipts;
- lexical progressive-disclosure retrieval;
- owner-checked held lock, root identity, reversible delete quarantine,
  roll-forward/rollback recovery, hash, closure, link, secret, and injection
  checks;
- temporary-directory behavioral tests.

P1:

- repeated hard-case clustering and held-out transfer evaluation;
- candidate deduplication and merge evaluation over the union of obligations;
- counterfactual utility, environment-aware decay, and canary rollout;
- sparse plus Transformer retrieval and deletion cascades;
- encrypted multi-user stores and richer retention policy;
- executable Skills only under a separate code-review and sandbox protocol;
- multi-model blind grading and domain-expert arbitration;
- scheduler-driven re-evaluation with `NO_DECIDABLE_MUTATION` stop conditions.
