# Module 16 — Known Gaps & Next Verification Targets (Explicit)

Date: 2026-01-30

This module is intentionally honest: it lists what is still incomplete or depends on sources we could not reliably read.

---

## 1) OpenReview group pages (JS rendering)
Status: UNVERIFIED  
Reason: Some group pages render key details dynamically; if unreadable, we cannot claim their content.

Action:
- Always verify critical constraints on the official venue site.
- If OpenReview becomes readable, create Verification Records (Module 15).

---

## 2) Future-year constraints (temporally unstable)
NeurIPS 2026+ and beyond: UNKNOWN/UNVERIFIED until official pages are published.

Action:
- Re-check official pages at time-of-use.

---

## 3) Template-vs-official drift
User-uploaded LaTeX templates may drift over time.

Action:
- Treat templates as UNVERIFIED backup; obey official rules.

---

## 4) Style advice vs “policy advice”
Style modules (human voice, rewrite recipes) are not policies. They do not override official constraints.

---

## 5) Domain-specific constraints
If the user’s paper is in a regulated domain (medicine, safety, industrial control), additional ethical/release constraints may apply.

Action:
- Require user context; do not invent constraints.



---

## v4 ADDITIONS — Re-check checklist (Append-only)

Before each major milestone (abstract deadline, full paper deadline, rebuttal):
1) Re-open official venue pages (call-for-papers, author instructions, LLM policy).
2) Update Verification Records (Module 15) for any changed rule text.
3) Scan the manuscript for:
   - page limit
   - anonymity leaks
   - unverified claims
   - missing required sections (e.g., impact statement for ICML)
4) Freeze a “submission snapshot” and do not introduce new results after freeze unless user provides them.

