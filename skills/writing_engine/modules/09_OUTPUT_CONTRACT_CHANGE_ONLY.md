# Module 09 — Output Contract: “Changed Sentences Only” (Strict)

This module enforces the required output formatting for revision tasks.

---

## 0) Non-negotiable rule
When rewriting user-provided text/LaTeX snippets: output ONLY the changed sentences.

No summaries. No “before/after paragraphs”. No meta talk.

---

## 1) Required schema (repeat for each changed sentence)

- ORIG: "..."
- SECTION: <abstract/introduction/related/method/experiments/discussion/conclusion/other>
- MOVE: <one tag from Module 10>
- PROBLEM: <one-line>
- NEW: "..."
- WHY: <one-line; tie to MOVE + constraints>
- RISK: <NONE/LOW/MED/HIGH> (why)
- STATUS: <VERIFIED/UNVERIFIED/UNKNOWN> for any factual/policy claim inside NEW

---

## 2) Edge cases

### 2.1 If you split one sentence into two
Represent as two items:
Item A: ORIG = original sentence; NEW = first new sentence
Item B: ORIG = "[SPLIT from previous ORIG]" ; NEW = second new sentence

### 2.2 If you delete a sentence
Represent as:
- ORIG: "..."
- MOVE: <tag>
- PROBLEM: <why it harms>
- NEW: "[DELETE]"
- WHY: "..."

### 2.3 If you add a new sentence
Represent as:
- ORIG: "[ADD after: <anchor phrase>]"
- NEW: "..."

But: additions that introduce new facts require VERIFIED sources or must be phrased as conditional.

---

## 3) Severity controls
If user says “light touch”:
- min_edit=true, deep_rewrite=false
If user says “aggressive”:
- deep_rewrite=true, but evidence_lock remains true unless explicitly disabled


---

## v4 ADDITIONS — Concrete examples (Append-only)

### Example 1 — Tighten + de-hype (Intro)
- ORIG: "Our method is novel and significantly outperforms prior work in many settings."
- SECTION: introduction
- MOVE: IN-M4
- PROBLEM: Overclaim without evidence; vague "many settings"
- NEW: "We introduce our method and evaluate it across the target settings in this paper."
- WHY: Removes unsupported performance claim; keeps thesis move.
- RISK: LOW (no new facts)
- STATUS: UNKNOWN

### Example 2 — Turn unverified claim into conditional (Abstract)
- ORIG: "We achieve state-of-the-art performance on AntMaze."
- SECTION: abstract
- MOVE: AB-M4
- PROBLEM: SOTA requires verified benchmark evidence
- NEW: "In our experiments, the method improves performance on AntMaze (see Table 1)."
- WHY: Contains claim to provided evidence location; avoids SOTA.
- RISK: MED (still needs Table 1 to exist)
- STATUS: UNKNOWN

### Example 3 — Anonymization (submission)
- ORIG: "We release code at https://github.com/<org>/<repo>."
- SECTION: experiments
- MOVE: EX-M1
- PROBLEM: De-anonymizing link; violates double-blind
- NEW: "Code will be released upon acceptance."
- WHY: Preserves intent without identity leak.
- RISK: LOW
- STATUS: VERIFIED (if venue requires anonymization; otherwise UNKNOWN)

### Example 4 — Split a compound claim (Method)
- ORIG: "We train the policy with EM updates and guarantee stability."
- SECTION: method
- MOVE: ME-M2
- PROBLEM: Two claims; “guarantee” is too strong
- NEW: "We train the policy with EM-style updates."
- WHY: Keeps supported mechanism; removes unsupported guarantee.
- RISK: LOW
- STATUS: UNKNOWN
- ORIG: "[SPLIT from previous ORIG]"
- SECTION: method
- MOVE: ME-M5
- PROBLEM: Guarantee claim unsupported
- NEW: "We empirically observe stable training under the reported settings."
- WHY: Downgrades to empirical observation.
- RISK: MED (requires evidence later)
- STATUS: UNKNOWN

### Example 5 — Delete a redundant sentence
- ORIG: "In conclusion, to conclude, our method is important."
- SECTION: conclusion
- MOVE: DC-M1
- PROBLEM: Pure filler; no content
- NEW: "[DELETE]"
- WHY: Removes padding.
- RISK: NONE
- STATUS: UNKNOWN

