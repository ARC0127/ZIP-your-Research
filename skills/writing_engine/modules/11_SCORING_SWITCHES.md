# Module 11 — Scoring Switches (Fine-Grained, Deterministic)

This module defines how to score text quality and control rewrite aggressiveness.

---

## 1) Switchboard (defaults)
- min_edit = true
- deep_rewrite = false
- evidence_lock = true
- venue_lock = auto (true if venue detected)
- style_lock = true
- novelty_claims_allowed = false (unless VERIFIED)
- add_new_citations = false (unless user asks + web module used)

---

## 2) Sentence-level score (0–5 each)
S1 Specificity: concrete nouns, measurable statements
S2 Evidence alignment: does the sentence require data/citation?
S3 Logical continuity: does it connect to previous/next?
S4 Readability: short, active, one idea per sentence
S5 Risk: anonymity/policy/overclaim

Total score = S1+S2+S3+S4 - S5_penalty

---

## 3) Paragraph-level score (0–5 each)
P1 Move completeness (for that section)
P2 Information density (no padding)
P3 Technical correctness (within given info)
P4 Narrative flow
P5 Venue compliance

---

## 4) Automatic triggers
If S2 low and sentence asserts a result:
- require VERIFIED evidence or downgrade to conditional
If S5 high due to anonymity:
- rewrite to remove identifiers
If P1 low in Introduction:
- require at least IN-M1..IN-M5 coverage

---

## 5) Reporting (internal vs user-visible)
By default, you do NOT show scores.
If user asks “why did you change this?”, show the score deltas for that sentence only.


---

## v4 ADDITIONS — Scoring anchors (0–5) + switch interactions (Append-only)

### 1) Anchors for sentence scores
S1 Specificity:
- 0: purely generic (“important”, “various”)
- 3: names the object but not the condition/metric
- 5: names object + condition + scope

S2 Evidence alignment:
- 0: makes strong claim with no evidence path
- 3: claim is modest but still needs citation
- 5: either purely definitional OR explicitly tied to provided evidence (table/lemma)

S3 Logical continuity:
- 0: unrelated to neighbors
- 3: loosely connected by topic
- 5: causal/contrast link that advances the argument

S4 Readability:
- 0: long, multi-clause, unclear subject
- 3: acceptable but slightly heavy
- 5: one idea, clear subject, minimal filler

S5 Risk:
- 0: no risk
- 3: possible overclaim or minor anonymity leak
- 5: clear policy violation risk

### 2) Switch interactions (safety)
- evidence_lock=true overrides deep_rewrite: you may restructure, but cannot add facts.
- venue_lock=true overrides style preferences: policy compliance beats style.
- If user requests “sound more confident”, do not increase claim strength without evidence.

### 3) Stop conditions
If a sentence cannot be improved without new facts:
- keep it, or weaken it, or turn into conditional
Do not hallucinate supporting details.

