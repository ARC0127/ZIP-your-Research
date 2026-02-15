# Workflows (v1.3.2)

These are **copy/paste** workflow recipes that chain multiple skills. Each workflow is designed to produce a **2-hour deliverable** by default.

## WF-1 Paper reading → claim map → 2-hour validation → write-up snippet

**When to use**
- You just read a paper (or a few) and want to quickly turn that into a testable idea + first results + text for your draft.

**Steps**
1) Use **S204 literature_triage_pipeline** to narrow to 3–5 key papers and extract core claims.
2) Use **S203 claim_evidence_matrix** to formalize what each paper claims and what evidence supports it.
3) Use **S211 related_work_delta_table** to define *your* delta in one sentence and a table.
4) Use **S301 minimal_decidable_experiment** to design a 2-hour experiment that can falsify your hypothesis.
5) Use **S309 error_analysis_playbook** if results are negative/unstable.
6) Use **writing_engine (MASTER_v1.3.2.md)** to convert the outcome into a paper-ready paragraph.

**Deliverables**
- Claim-evidence matrix
- Delta table
- 2-hour experiment plan + acceptance criteria
- One draft paragraph (method/experiment or intro)

---

## WF-2 Rebuttal pipeline (reviewer #2 edition)

1) **S502 reviewer_simulator**: steelman the strongest criticism.
2) **S519 response_matrix_builder**: convert all comments into a response table with evidence links.
3) **S501 rebuttal_generator**: write responses with commitments and precise edits.
4) **writing_engine**: apply edits to the manuscript sections, diff-only.

Deliverables: response matrix + rebuttal text + edit list.

---

## WF-3 Dataset/spec → release checklist

1) **S403 dataset_spec**: define schema, leakage checks, metadata.
2) **S419 data_versioning_and_checksum**: add checksums and version tags.
3) **S424 citation_and_attribution_audit**: ensure licenses/credits.
4) **S524 open_source_release_note_generator**: write release notes.
5) `python tools/make_release.py --version v1.3.2`: produce a clean zip without `.git`.

Deliverables: dataset spec + checksums + release notes + release zip.

---

## WF-4 “I feel stuck” → decision in 2 hours

1) **S222 idea_prioritization_matrix**: rank ideas by impact × feasibility.
2) **S301 minimal_decidable_experiment**: pick the top idea and validate quickly.
3) **S310 compute_cost_reporting_template**: record compute/time properly.
4) **S503 submission_readiness_gate**: decide whether to write now or iterate.

Deliverables: decision + plan + next actions.


---

## WF-5 Correctness-first audit (logic → method → calculation → proof → paper arc)

**When to use**
- You want to maximize *quality upper bound* by catching wrong reasoning, wrong derivations, and over-claims early.
- Typical triggers: “逻辑核查 / 方法正确性核查 / 计算正确性核查 / 证明思路核查 / 论文整体思路核查”.

**Inputs**
- Your current draft (outline or sections) OR the specific paragraphs/derivations you worry about.
- A bullet list of your **core claims** (3–8 items).

**Steps (default 2h)**
1) **Logic graph + contradictions**
   - Run **S226 logic_consistency_audit**
   - Deliverable: claim graph + contradictions + minimal repair plan.
2) **Method correctness + assumption sufficiency**
   - Run **S227 method_correctness_audit**
   - Deliverable: objective↔method alignment table + missing assumptions + edge cases.
3) **Calculation/unit sanity (if math/code involved)**
   - Run **S326 calculation_correctness_check**
   - Deliverable: step-by-step check + falsification tests + minimal corrections.
4) **Proof plan check (if you have theorems/guarantees)**
   - Run **S230 proof_idea_check**
   - Deliverable: proof structure + missing lemmas + counterexample search plan.
5) **Paper-level arc coherence**
   - Run **S229 paper_storyline_integrity_check**
   - Deliverable: 5-beat arc + Move audit + reordered outline.

**Acceptance criteria**
- Every “issue” is accompanied by a concrete “repair action”.
- Any uncertain part is explicitly labeled **UNKNOWN** with a verification plan.
- Core claims are rewritten to match the evidence (no overclaiming).

---

## WF-6 Novelty + innovation stress test (audit → search plan → delta table)

**When to use**
- You need to verify novelty, search prior art, and avoid “already done” traps before investing in experiments.

**Steps (default 2h)**
1) **Atomic novelty decomposition + safe claim rewrite**
   - Run **S228 innovation_novelty_audit**
2) **Prior-art search plan**
   - Run **S231 innovation_point_search_plan**
3) **Related-work delta table**
   - Run **S211 related_work_delta_table**
4) (Optional) **Novelty verification protocol**
   - Run **S224 novelty_verification_protocol**

**Acceptance criteria**
- Novelty is decomposed into atomic components with falsification-oriented screening rules.
- You end with a shortlist of papers + a delta table + a safe (non-overclaiming) contribution statement.
