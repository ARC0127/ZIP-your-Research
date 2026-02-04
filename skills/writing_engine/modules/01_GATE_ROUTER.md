# Module 01 — GATE & ROUTER (Intent → Section → Moves → Risks)

This module defines how to do **Gate** in a deterministic, programmatic way.
You must run this module **before** you rewrite anything.

---

## 1) Intent Router (Input-Type Classifier)

### 1.1 Recognize the primary input type
Classify into exactly one:
- T1 PDF
- T2 Snippet (text/LaTeX)
- T3 Topic question (innovation/literature)
- T4 Mixed

### 1.2 One forced-choice clarification (only if needed)
If the user’s intent is unclear, ask one question only:
- “Is this for (A) revision, (B) review, or (C) explanation?”
Then continue with best-effort based on the answer.
If the user refuses to answer, proceed with a default:
- Default = revision, but label “INTENT = ASSUMED”.

---

## 2) Section Router (Snippet → Paper Section)

### 2.1 Section labels
Pick one primary label:
- TITLE
- ABSTRACT
- INTRODUCTION
- RELATED_WORK
- PRELIMINARIES / PROBLEM_SETUP
- METHOD / ALGORITHM
- THEORY / ANALYSIS
- EXPERIMENTS
- RESULTS
- DISCUSSION
- LIMITATIONS
- IMPACT_STATEMENT
- APPENDIX

### 2.2 Section cues (non-exhaustive)
**ABSTRACT** cues:
- 4–6 sentences, one paragraph, “We propose / We study / We show…”
- Contains problem + method + evidence preview.

**INTRODUCTION** cues:
- broad context → narrowing
- “However / Yet / Despite”
- contributions list appears.

**METHOD** cues:
- equations, notation, “Algorithm 1”
- stepwise procedure.

**EXPERIMENTS** cues:
- benchmarks, baselines, metrics, protocol.

**IMPACT_STATEMENT** cues:
- explicit ethics/societal consequences phrasing.

Output:
- SECTION_GUESS
- Confidence {high, medium, low}
- 2–4 bullets citing textual cues.

---

## 3) Move Router (Sentence → Rhetorical Move Tags)

### 3.1 Move sets by section
**Abstract moves (A1..A6):**
- A1 Problem framing
- A2 Gap / why current approaches fail
- A3 Proposed method (one-sentence core)
- A4 How it works (1–2 mechanisms)
- A5 Evidence preview (datasets/metrics)
- A6 Takeaway + cost/limits

**Introduction moves (I1..I8):**
- I1 Context
- I2 Tension / why hard
- I3 Gap
- I4 Key idea
- I5 Mechanism preview
- I6 Evidence preview
- I7 Contributions enumeration
- I8 Roadmap

**Method moves (M1..M8):**
- M1 Setup/notation
- M2 Design goals/constraints
- M3 Overview
- M4 Component/module
- M5 Objective/loss
- M6 Complexity
- M7 Assumptions
- M8 Implementation details

**Experiments/Results moves (E1..E10):**
- E1 Question/hypothesis
- E2 Setup (datasets/baselines)
- E3 Metrics
- E4 Main result claim
- E5 Mechanism evidence (ablation/diagnostic)
- E6 Compute/latency
- E7 Robustness (seeds, variance)
- E8 Failure cases
- E9 Reproducibility pointers
- E10 Takeaway

**Related work moves (R1..R6):**
- R1 Taxonomy
- R2 Closest line of work
- R3 Contrast grid
- R4 Why your approach differs
- R5 What you inherit
- R6 Takeaway

---

## 4) Claim Extractor (Find strong claims, then constrain)

### 4.1 Strong-claim triggers
Verbs and phrases:
- “show”, “prove”, “guarantee”, “outperform”, “significantly”, “state-of-the-art”, “first”, “novel”, “solve”.

### 4.2 Evidence pointer inventory
Evidence pointer types:
- Table / Figure / Appendix section
- Theorem / Lemma
- Ablation / Diagnostic
- Implementation detail (time, memory)
If missing, mark:
- EVIDENCE POINTER = UNKNOWN
and rewrite plan must weaken the claim.

### 4.3 Claim calibration ladder
If evidence is UNKNOWN, apply ladder:
- Level 3 (strong): “outperforms” → requires explicit numbers
- Level 2 (medium): “improves” → requires at least a pointer
- Level 1 (weak but safe): “can improve / often improves / improves in our evaluated settings”

---

## 5) Risk Register (Reviewer Objection Simulator)

### 5.1 Minimum risk list (must produce ≥ 8 risks)
Examples:
1) Over-claim without evidence.
2) Unclear problem definition.
3) Missing closest baselines.
4) Missing compute/latency.
5) No failure cases.
6) No scope/assumptions.
7) Poor positioning vs nearest work.
8) Unclear contributions (not separable).
9) Template-like “AI slop” tone.
10) Policy or anonymity risk (ICML).

### 5.2 Risk → Fix mapping
Each risk must map to a concrete fix:
- add a scope clause
- add an evidence pointer
- split a long sentence
- remove empty qualifiers
- replace generic adjectives with operational consequences

---

## 6) Gate Output Schema (must be produced verbatim)

When Gate finishes, output:
1) SECTION_GUESS + confidence + cues
2) Sentence-level Move Map (one line per sentence)
3) Top strong claims (6–10) + evidence status
4) Risk log (≥8) with fix hints
5) Rewrite plan:
   - how many sentence edits you will propose (≥20 if the snippet is long; else “as many as needed”)
   - which modules you will apply next

---

## 7) Determinism knobs (switches)
Define these switches (default values):
- NO_CLARIFYING_QUESTIONS = ON (except the one forced-choice for intent)
- OUTPUT_MODE = DIFF_ONLY
- SENTENCE_MAX_WORDS = 25
- BAN_PRIORITY_CLAIMS = ON

If user requests exceptions, require explicit confirmation and log it.

## Source Anchors (for the assistant’s web verification workflow)
- ICML 2026 Author Instructions: https://icml.cc/Conferences/2026/AuthorInstructions
- ICML 2026 Call for Papers: https://icml.cc/Conferences/2026/CallForPapers
- ICML Blog (peer-review updates): https://blog.icml.cc/
- Purdue OWL concision resources: https://owl.purdue.edu/
- University writing center guides on concision and transitions (examples):
  - https://writingcenter.tamu.edu/
  - https://www.uvu.edu/writingcenter/
  - https://www.utm.utoronto.ca/rgasc/


### Extra Example Set 1 (structured, not filler)
**Task type:** Gate/Router  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Gate/Router>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 1 (operational)
For Gate/Router, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 2 (structured, not filler)
**Task type:** Gate/Router  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Gate/Router>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 2 (operational)
For Gate/Router, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 3 (structured, not filler)
**Task type:** Gate/Router  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Gate/Router>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 3 (operational)
For Gate/Router, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 4 (structured, not filler)
**Task type:** Gate/Router  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Gate/Router>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 4 (operational)
For Gate/Router, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 5 (structured, not filler)
**Task type:** Gate/Router  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Gate/Router>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 5 (operational)
For Gate/Router, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 6 (structured, not filler)
**Task type:** Gate/Router  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Gate/Router>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 6 (operational)
For Gate/Router, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 7 (structured, not filler)
**Task type:** Gate/Router  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Gate/Router>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 7 (operational)
For Gate/Router, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 8 (structured, not filler)
**Task type:** Gate/Router  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Gate/Router>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 8 (operational)
For Gate/Router, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 9 (structured, not filler)
**Task type:** Gate/Router  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Gate/Router>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 9 (operational)
For Gate/Router, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 10 (structured, not filler)
**Task type:** Gate/Router  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Gate/Router>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 10 (operational)
For Gate/Router, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 11 (structured, not filler)
**Task type:** Gate/Router  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Gate/Router>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 11 (operational)
For Gate/Router, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 12 (structured, not filler)
**Task type:** Gate/Router  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Gate/Router>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 12 (operational)
For Gate/Router, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 13 (structured, not filler)
**Task type:** Gate/Router  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Gate/Router>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 13 (operational)
For Gate/Router, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


---

## v2 ADDITIONS — Stronger Gate: venue detection, section detection, and risk flags (Append-only)

### 0) Gate Inputs (explicit)
Before rewriting, you MUST extract these fields and keep them as a “Gate Header” (internal, not shown unless user asks):
- INTENT: revision / review / explanation / innovation
- INPUT_TYPE: T1/T2/T3/T4
- VENUE_TARGET: ICML / NeurIPS / ICLR / Unknown (auto-detect; user override wins)
- SECTION_DETECTED: abstract / intro / related / method / experiments / discussion / conclusion / appendix / rebuttal / other
- STRICTNESS_SWITCHES: {min_edit, deep_rewrite, evidence_lock, venue_lock, style_lock}
- RISK_FLAGS: {anonymity, unverifiable_claims, citation_risk, formatting_risk, ethics_risk}

### 1) Venue detection (auto + override)
Use these signals in order:
1) Explicit venue mention by user.
2) Presence of style macros or class files:
   - icml2026 / icml2026.sty → ICML
   - neurips_2025 / neurips_2025.sty → NeurIPS
   - iclr2026_conference / iclr2026_conference.sty → ICLR
3) If still unknown, keep VENUE_TARGET=Unknown, but set venue_lock=false (do not invent constraints).

### 2) Section detection (expanded heuristics)
In addition to the existing rules, add these detectors:
- Abstract: single paragraph + "\begin{abstract}", or "Abstract—", or 4–6 sentence block.
- Contributions: phrases like "Our contributions are", enumerated list, bullet list, "We make the following contributions".
- Method: algorithm blocks, "We propose", "We introduce", "We formulate", "Let … denote".
- Experiments: "We evaluate on", "Baselines", "Implementation details", "Hyperparameters", tables/figures.
- Related: dense citation clusters, "Prior work", "Compared to", "We build upon".
- Rebuttal/Response: "We thank the reviewers", "R1/R2/R3", point-by-point structure.

If multiple sections match, pick the strongest and set RISK_FLAGS.section_ambiguity=true.

### 3) Gate scoring (hand-off to Module 11)
After detection, compute a Gate scorecard (0–5 each):
- Specificity
- Evidence alignment
- Novelty clarity
- Logical continuity
- Venue compliance risk (inverse)
- Human voice (non-formulaic)

Do NOT rewrite yet. Only once Gate is complete do you enter Rewrite.

