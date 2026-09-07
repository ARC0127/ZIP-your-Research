---
name: theory-claim-audit
description: Audit a theoretical claim's assumptions, implication gaps, counterexamples, and proof obligations.
---

# Theory Claim Audit

## Mission

Convert a research idea into a falsifiable, non-vacuous theory program. Start from the paper claim, not from an existing algorithm or a convenient theorem.

Use this order:

```text
scientific problem -> claim -> implication bridges -> counterexample
-> minimal assumptions -> theorem ladder -> algorithm binding
-> falsification experiment -> verdict
```

Read `references/protocol.md` completely before producing a full Theory Specification, implication DAG, or paper-level theory audit.

## Non-negotiable rules

- Keep the scientific object, mathematical object, implementation object, and evaluation object distinct.
- Mark missing information `UNKNOWN`; never infer a favorable assumption from method intent.
- Require the human researcher to own the headline claim, acceptable assumptions, comparator, and failure rule.
- Treat theorem truth, applicability, and numerical usefulness as separate judgments.
- Do not let population properness, oracle sufficiency, optimization convergence, or proxy improvement stand in for finite-data deployment performance.
- Do not search for new theorems until the first fatal frontier is identified.
- Do not repair a failed claim by silently changing its domain, quantifier, checkpoint, comparator, or target quantity.
- Keep application-specific evidence separate from generic theory unless reproduced under the generic protocol.

## Required inputs

Obtain or mark `UNKNOWN`:

- domain and real scientific problem;
- current headline claim in plain language;
- input, output, target quantity, comparator, and deployment meaning;
- data, intervention, oracle, and validation access;
- intended domain, quantifiers, probability semantics, and scaling regime;
- allowed and forbidden assumptions;
- algorithm outputs and current evidence;
- falsification and stop/downgrade rules.

Ask at most three short questions at a time. Do not block progress when a field can be recorded as `UNKNOWN`.

## Workflow

### 1. Lock the construct

Map the real problem to explicit mathematical objects. Check units, information timing, privileged variables, intervention access, training distribution, deployment distribution, and comparator. Reject proxy/object substitution.

### 2. Write the claim contract

Express the headline claim with object, domain, quantifier, probability semantics, comparator, guaranteed quantity, exclusions, and failure boundary. Split a conjunctive claim into separately testable subclaims.

### 3. Build the implication DAG

Represent definitions, assumptions, evidence, lemmas, theorems, and the headline claim as nodes. Write every edge as:

> Under assumptions A, does X imply Y?

Classify each edge as one or more of `B0` through `B6` from the reference protocol. Do not use vague verbs such as "supports", "enhances", or "aligns" as logical implications.

### 4. Find the first fatal frontier

Traverse backward from the headline claim. Find the smallest unresolved edge cut that blocks every valid path from assumptions/evidence to the claim. Prioritize `REFUTED` and `VACUOUS`, then `UNKNOWN` and `CONDITIONALLY_VALID`.

Do not confuse the first flawed edge in one proof with the first fatal frontier of a DAG containing alternative proof routes.

### 5. Construct a minimal counterexample

Preserve all upstream premises and change only what is needed to falsify the downstream implication. State whether the failure comes from specification, identifiability, statistics, computation, composition/feedback, or deployment.

### 6. Audit the assumption budget

Add only assumptions that block known counterexamples. For each assumption record necessity, observability, realism, algorithm mechanism, removal counterexample, and status. Reject assumptions equivalent to the desired conclusion.

### 7. Design the minimal theorem ladder

Use only theorem layers needed to close the claim path. Prefer:

1. an impossibility or necessity proposition;
2. an oracle mechanism theorem;
3. a finite-sample or learnability theorem;
4. a composition, robustness, or deployment corollary.

Do not count definitions or immediate quotient constructions as central theoretical contributions unless they close a genuine fatal frontier.

### 8. Bind proof, algorithm, and experiment

For every theorem identify:

- the exact tensor, estimator, policy, or certificate produced by code;
- the experiment that can falsify applicability or usefulness;
- negative controls and assumption checks;
- the deployment quantity actually supported.

Downgrade any theorem whose mathematical object is not implemented.

### 9. Issue a verdict

Use exactly one route verdict:

- `PROVE`: the frontier appears closable under acceptable assumptions;
- `CONDITION`: retain an explicit conditional claim;
- `DOWNGRADE`: narrow the domain, quantifier, or guaranteed object;
- `STOP`: a fatal edge is refuted without an acceptable repair.

"Add more formulas, modules, or experiments" is not a verdict.

## Output contract

Return these sections in order:

1. **Problem statement v2** - one to three sentences.
2. **Construct lock** - object table, information access, comparator, in/out scope.
3. **Claim contract** - headline claim plus decomposed subclaims.
4. **Implication DAG** - numbered nodes and edges with bridge classes and statuses.
5. **First fatal frontier** - smallest unresolved cut and why it is fatal.
6. **Minimal counterexample** - premises preserved and conclusion falsified.
7. **Assumption budget** - accepted, forbidden, and `UNKNOWN` assumptions.
8. **Minimal theorem ladder** - only the required results.
9. **Proof-Algorithm-Experiment binding** - one row per result.
10. **Verdict and next decidable action** - include no more than three human decisions.

When the user explicitly selects an iterative framing discussion, stop at the
agreed construct/claim checkpoint. For a requested complete audit, work through
the applicable sections using provisional branches or UNKNOWN where human
decisions are missing; do not stop merely because the project is early-stage.
Previously accepted constructs and claims need no repeated confirmation.
Do not lock a method or accept assumptions on the researcher's behalf.

## Hard failures

Fail the audit and restart the construct/claim steps when any of these occurs:

- **Conditional-theorem laundering**: assuming a perfect oracle, sufficient statistic, or uniform bound that nearly restates the conclusion.
- **Proxy/object laundering**: proving a surrogate or internal certificate while claiming real return, safety, stability, or scientific truth.
- **Post-hoc assumption drift**: changing the claim after results without versioning and downgrading it.

Also mark a result `VACUOUS` when the feasible set is empty, acceptance is trivial, a bound is useless at actual sample size, or the oracle object is merely the full solution renamed.

## Human and AI boundary

Require the human to decide:

- the scientific question and headline claim;
- acceptable assumptions and risks;
- comparator, evaluation quantity, and stopping rule;
- whether the contribution is worth pursuing.

Use AI or a proof engine to formalize quantifiers, build the DAG, search and map theorems, construct counterexamples, check proof dependencies, audit implementation bindings, and maintain the `UNKNOWN/REFUTED/VACUOUS` ledger.

Never let proof automation certify that assumptions are realistic or that a numerically empty bound is useful.
