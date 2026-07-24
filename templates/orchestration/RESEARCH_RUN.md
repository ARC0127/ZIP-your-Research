# RESEARCH_RUN — Visible Epistemic Orchestration Artifact

Use one copy per locked research task. This Markdown file is the visible,
human-reviewable source of the orchestration state. A host may derive indexes
or structured views from it, but those derivatives are not authoritative.

## 0. Run header

| Field | Value |
|---|---|
| Run ID | |
| Created at | |
| Current state | `PRELOCK / LOCKED / SEARCH / DEBATE / ADJUDICATION / RENDER / DONE / PARTIAL / BLOCKED` |
| Objective | |
| Decision to enable | |
| Deliverable | |
| Time/token/agent budget | |
| Lock reference or hash | |

### Status separation

| Status class | Value | Evidence |
|---|---|---|
| Structural | `NOT_RUN / PASS / FAIL` | |
| Behavioral | `NOT_RUN / PASS / FAIL / PARTIAL` | |
| Scientific | `UNKNOWN / HYPOTHESIS / SUPPORTED / REFUTED / PROVED / NOT_APPLICABLE` | |

## 1. Host capability handshake

| Capability | `AVAILABLE / UNAVAILABLE / UNKNOWN` | Evidence |
|---|---|---|
| Real worker agents | | |
| Blind first-round isolation | | |
| Web search | | |
| Page/PDF inspection | | |
| Exact citation spans | | |
| Persistent-write approval | | |

**Gate:** If real agents or required web inspection are unavailable, record
`MULTI_AGENT_UNAVAILABLE` and do not fabricate a team transcript.

## 2. Task lock

### Included

- [included item]

### Excluded

- [excluded item]

### Frozen objects

| Object | Frozen value | Change authority |
|---|---|---|
| Terminology | | |
| Claims | | |
| Equations/data | | |
| Source boundary | | |
| Acceptance boundary | | |

### Scope deltas

| Delta ID | Requested change | Affected artifacts | Approval | New lock |
|---|---|---|---|---|
| | | | | |

## 3. Epistemic ledger

Use `FACT`, `INFERENCE`, `HYPOTHESIS`, or `UNKNOWN`. A verification status is
separate from the epistemic class.

| Item ID | Class | Statement | Source/dependency | `VERIFIED / PLAUSIBLE / NOT_RUN / REFUTED` | Validity boundary |
|---|---|---|---|---|---|
| | | | | | |

## 4. Question graph

| Question ID | Type | Decision relevance | Priority | Assigned agent | Stop condition | Status |
|---|---|---|---|---|---|---|
| | definition/evidence/novelty/mechanism/proof/experiment/citation/figure | | | | | |

## 5. Blind agent allocation

| Agent ID | Real host agent ID | Search lens | Inputs visible before submission | Budget | Submitted at |
|---|---|---|---|---|---|
| | | primary/official | | | |
| | | contradiction/negative result | | | |
| | | adjacent work/novelty | | | |

Agents using the same model with isolated contexts are context-diverse, not
independent scientific replications.

## 6. Source cards

| Source ID | URL or file | Source tier | Date/version | Exact span/page | Relationship | Provenance family | Access status | Trust/injection note |
|---|---|---|---|---|---|---|---|---|
| | | primary/official/secondary | | | supports/contradicts/context | | inspected/metadata-only/unavailable | |

## 7. Evidence lineage

| Edge ID | From | Relation | To | Exact evidence | Auditor status | Conflict |
|---|---|---|---|---|---|---|
| | source/claim/assumption | supports/contradicts/depends_on/tests/derived_from/supersedes | | | | |

### Missing and conflicting evidence

| Item | Why unresolved | Consequence | Verification action |
|---|---|---|---|
| | | | |

## 8. Candidate versions

### Candidate v0

| Field | Content |
|---|---|
| Candidate ID | |
| Mechanism/proposition | |
| Assumptions and scope | |
| Delta from baseline | |
| Supporting evidence | |
| Counterevidence | |
| Predictions | |
| Falsifier/counterexample | |
| Proof obligations | |
| Minimal decisive experiment/action | |
| Feasibility/cost | |

### Candidate vN

Copy the v0 table for each new immutable version. Do not overwrite prior
versions.

## 9. Objection ledger

| Objection ID | Candidate/claim | Critic role | Failure condition | Evidence | Response | `OPEN / RESOLVED / REFUTED / UNKNOWN` | Resolution test |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

Majority agreement and repeated wording are not resolution tests.

## 10. Round deltas

### ROUND_DELTA R1

| Dimension | Delta |
|---|---|
| New/withdrawn evidence | |
| Changed epistemic status | |
| Mechanism/assumption change | |
| Prediction/falsifier change | |
| Objections resolved/opened | |
| Rejected paths | |
| Next highest-information action | |
| Scientific delta | `YES / NO_SCIENTIFIC_DELTA` |

Copy this section for each round.

## 11. Proof and experiment status

### Proof obligations

| Obligation ID | Statement | Assumptions | Dependency | Counterexample search | Status | Evidence |
|---|---|---|---|---|---|---|
| | | | | | `OPEN / FAILED / SUPPORTED / PROVED` | |

### Experiment protocol

| Field | Locked value |
|---|---|
| Hypothesis | |
| Dataset/split | |
| Leakage controls | |
| Baselines and matched budgets | |
| Primary metric and denominator | |
| Seeds/uncertainty | |
| Stopping rule | |
| Negative controls/ablations | |
| Protocol timestamp/reference | |
| Prospective or retrospective | |

### Result lineage

| Result ID | Raw artifact/reference | Command/environment | Protocol deviation | Metric/denominator/uncertainty | Status |
|---|---|---|---|---|---|
| | | | | | |

## 12. Scientific Decision Record (SDR) and adjudication

This section freezes the decision-facing claim ledger, evidence lineage,
selected candidate version, proof/experiment status, unresolved boundaries,
and adjudication. Sections 3, 7, 8, and 11 are normative dependencies of this
record. Writing and figure stages consume these objects as read-only input.

| Candidate/claim | Fatal gate | Evidence sufficiency | Proof/experiment status | Novelty boundary | Feasibility | Decision |
|---|---|---|---|---|---|---|
| | | | | | | champion/reject/retain-alternative/UNKNOWN |

**Current champion:**

**Why:**

**Critical UNKNOWN:**

**External-replication boundary:**

`NO_CHAMPION_READY` is permitted.

## 13. Read-only rendering checks

| Renderer | Claim IDs preserved | Modality/negation preserved | Numbers/units preserved | Citation relation preserved | Limitations preserved | Status |
|---|---|---|---|---|---|---|
| Writing | | | | | | |
| Bilingual | | | | | | |
| Citation | | | | | | |
| Figure/diagram | | | | | | |

If a renderer introduces scientific content, return to the earliest affected
state.

## 14. Failed paths

| Path ID | Attempt | Failure evidence | Reusable lesson | Reopen condition |
|---|---|---|---|---|
| | | | | |

## 15. Stop record

| Field | Value |
|---|---|
| Stop type | `DECISION_READY / CONVERGED / DECISIVE_ACTION / NO_VIABLE_CANDIDATE / BUDGET / BLOCKED / SAFETY` |
| Satisfied condition | |
| Unresolved critical items | |
| Budget used | |
| Next verification action | |
| Final run status | `DONE / PARTIAL / BLOCKED / UNKNOWN` |

## 16. Visible memory

### Memory used

| Memory ID | Scope | Status/age | Source | Why used | Reverification |
|---|---|---|---|---|---|
| | | | | | |

### Short-term session memory

| Active objective | Current state | Active candidate | Critical UNKNOWN | Next action | Expiry |
|---|---|---|---|---|---|
| | | | | | end of run |

### Long-term memory proposal

| Proposal ID | Candidate records | Scope | Source | Sensitivity | Conflict | Retention | Consent status |
|---|---|---|---|---|---|---|---|
| | | | | | | | `PROPOSED_ONLY` |

No persistent write is implied by completing this section.

## 17. Final verification record

- [ ] Lock remained stable or every scope delta was approved
- [ ] Real host capabilities were verified
- [ ] Facts, inferences, hypotheses, and UNKNOWN items are separated
- [ ] Primary/official sources were inspected where available
- [ ] Contradictions and failed paths remain visible
- [ ] Candidate versions and round deltas are preserved
- [ ] Proof/experiment claims match executed evidence
- [ ] Writing, citations, and figures did not strengthen the science
- [ ] Stop condition is explicit
- [ ] Memory remains visible and non-persistent without consent
