# Module 06 — Human Voice & Anti-“AI Slop” Writing Discipline

This module enforces a writing style that reads like strong human top-conference prose:
- short, direct sentences
- common words
- no empty qualifiers
- no template-like repetition
- no buzzword stacking

---

## 1) What “AI slop” looks like (signals)
Signals (do not use as detector claims; use as editing heuristics):
- repeated structure: “In this paper, we propose…” every paragraph
- connector spam: “Moreover/Furthermore/In addition” chains
- vague nouns: “robustness, efficiency, transparency” without operational meaning
- hedging + hype together: “significantly” without evidence
- ornamental verbs: “delve, underscore, garner, bolster”
- empty meta statements: “This is important and has wide applications” with no specifics

---

## 2) Replace patterns with concrete writing

### 2.1 Replace qualifiers
- Remove: very, really, extremely, basically, essentially
- If you need emphasis, use evidence:
  - “improves by X%” (only if provided)
  - “reduces latency from A to B” (only if provided)

### 2.2 Replace vague nouns with measurable proxies
- “efficient” → “reduces runtime / reduces memory / reduces instrumentation”
- “robust” → “stable across seeds / stable across shifts”
- “scalable” → “handles N nodes / N tasks / N parameters” (only if provided)

### 2.3 Avoid over-transitioning
Use transitions only when logic changes:
- However: contradiction or limitation
- Therefore: consequence
- Because: cause
If you can drop a transition and the paragraph still reads logically, drop it.

---

## 3) Sentence rhythm without long sentences
Use controlled variation:
- one short sentence + one medium sentence is fine
- avoid multiple long sentences in a row
If a sentence exceeds 25 words:
- split
- keep the first sentence factual
- keep the second sentence as implication (“This matters because …”).

---

## 4) Micro-edit recipes (ready-to-use)

Recipe A — cut filler:
- Delete “It is worth noting that…”
- Replace “This work aims to…” with the concrete action verb:
  - “We design / We analyze / We measure / We propose / We implement”

Recipe B — define once:
- Replace “X” with “X (full name)” at first mention.
- After that, use X consistently.

Recipe C — calibrate claims:
- Replace “outperforms all” with “outperforms the baselines we compare against (Table X).”
If Table X not present:
- pointer UNKNOWN; use “we compare against”.

---

## 5) Human-like positioning (without hype)
Positioning is not marketing. It is a contrast grid:
- What is the closest baseline line of work?
- Which axis differs? (objective, constraint, inference, cost, assumption)
- What trade-off does your method accept?

If you cannot name the closest line from the snippet:
- write UNKNOWN and ask the user for the baseline list.

---

## 6) “Topic / stress” discipline
- Start sentences with known context (topic).
- End sentences with what you want the reader to remember (stress).
This produces a natural, human flow.

---

## 7) Style audit checklist (run at the end)
1) No empty qualifiers without evidence.
2) No repeated template sentence starts.
3) No connector spam.
4) No vague nouns without measurable proxy.
5) Average sentence length ≤ 20; hard cap 25.
6) Claims have evidence pointers or are downgraded.
7) Terminology consistent.

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
**Task type:** Human Voice  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Human Voice>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 1 (operational)
For Human Voice, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 2 (structured, not filler)
**Task type:** Human Voice  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Human Voice>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 2 (operational)
For Human Voice, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 3 (structured, not filler)
**Task type:** Human Voice  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Human Voice>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 3 (operational)
For Human Voice, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 4 (structured, not filler)
**Task type:** Human Voice  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Human Voice>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 4 (operational)
For Human Voice, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 5 (structured, not filler)
**Task type:** Human Voice  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Human Voice>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 5 (operational)
For Human Voice, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 6 (structured, not filler)
**Task type:** Human Voice  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Human Voice>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 6 (operational)
For Human Voice, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 7 (structured, not filler)
**Task type:** Human Voice  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Human Voice>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 7 (operational)
For Human Voice, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 8 (structured, not filler)
**Task type:** Human Voice  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Human Voice>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 8 (operational)
For Human Voice, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 9 (structured, not filler)
**Task type:** Human Voice  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Human Voice>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 9 (operational)
For Human Voice, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 10 (structured, not filler)
**Task type:** Human Voice  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Human Voice>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 10 (operational)
For Human Voice, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 11 (structured, not filler)
**Task type:** Human Voice  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Human Voice>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 11 (operational)
For Human Voice, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 12 (structured, not filler)
**Task type:** Human Voice  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Human Voice>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 12 (operational)
For Human Voice, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 13 (structured, not filler)
**Task type:** Human Voice  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Human Voice>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 13 (operational)
For Human Voice, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


### Extra Example Set 14 (structured, not filler)
**Task type:** Human Voice  
**Input (user snippet):**  
- Sentence: “This method significantly improves performance in all settings.”  

**Gate decision:**  
- Claim strength = high; evidence pointer = UNKNOWN → must calibrate.

**Diff-only output record:**  
- ORIGINAL: "This method significantly improves performance in all settings."  
- MOVE: <Evidence-calibrated claim for Human Voice>  
- REVISED:  "This method improves performance on the benchmarks we evaluate (see Table X)."  
- WHY: Add scope + evidence pointer; avoid universal claim.  
- EVIDENCE POINTER: UNKNOWN (request Table/Figure id if not provided).  
- RISK REDUCED: Over-claim / unsupported generalization.

**Notes:** Keep the revised sentence ≤ 25 words. Prefer direct verbs. Avoid “significantly” unless statistical test is specified.


### Extra Checklist Pack 14 (operational)
For Human Voice, confirm each item before final output:
1) Every strong verb (show/prove/outperform) has an evidence pointer or is weakened.
2) No “first/only” unless the user provided explicit comparative evidence.
3) Sentence length cap satisfied; split if needed.
4) One connector per paragraph max (avoid “Moreover/Furthermore” chains).
5) Acronyms introduced once; consistent thereafter.
6) If venue=ICML2026: anonymity, 8-page main body, single PDF, impact statement placement.


---

## v2 ADDITIONS — Human voice: official plain-language + anti-formulaic controls (Append-only)

### 0) Plain-language alignment (for top venues)
Many venues now emphasize accessibility and clarity. Use:
- short sentences with one idea
- concrete nouns
- explicit subjects
- minimal hedging

### 1) Common "AI-ish" patterns to avoid (use as a checklist, not as "evasion")
Flag and fix when you see:
- Repeated scaffolding: "In conclusion / Moreover / It is important to note"
- High-level filler: "plays a crucial role", "paves the way", "in today’s rapidly evolving"
- Abstract praise: "significant", "novel", "groundbreaking" without evidence
- Redundant restatement (same idea twice)
- Over-smoothing: every paragraph has identical rhythm

### 2) Human variation knobs (controlled)
- Allow 10–20% "short punchy" sentences per paragraph
- Permit one rhetorical question per section at most
- Permit one forward pointer per section at most
If user wants stricter academic tone, disable these.

### 3) Domain-term preservation rule (hard)
Do not paraphrase technical terms that carry formal meaning.
Example: keep "double-blind", "desk rejected", "main body", "supplementary material".

