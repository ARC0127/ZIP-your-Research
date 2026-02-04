# Module 14 — ICML 2026 Hard Constraints: Programmatic Checklist (VERIFIED core rules)

Date generated: 2026-01-30

This module is invoked when VENUE_TARGET=ICML and venue_lock=true.

Sources (VERIFIED):
- https://icml.cc/Conferences/2026/AuthorInstructions
- https://icml.cc/Conferences/2026/CallForPapers

---

## 1) Must-pass checks (desk-reject risk)

### ICML-1: Main body ≤ 8 pages
- If PDF available: count pages and require manual confirmation of where “main body” ends.
- If only LaTeX: require compiled page count or keep RISK=MED and do not claim compliance.

### ICML-2: Single PDF
- Submission must be one PDF containing main text + references + (optional) appendices.

### ICML-3: PDF size
- Submission ≤ 50MB; camera-ready ≤ 20MB.

### ICML-4: Double-blind anonymization
- Remove author names, affiliations, acknowledgements.
- Self-citations phrased in third person.
- No de-anonymizing links.

### ICML-5: GenAI policy hooks
- Do not list LLM as authors.
- Do not include prompt-injection content.
- If user requests: include a “Generative AI usage” statement if it is a notable part of methodology.

### ICML-6: Lay summary (post-accept)
- For accepted papers, prepare to add lay summary in OpenReview.

---

## 2) Concrete anonymization scanner (string rules)
Flag if any match occurs:
- email regex: [A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}
- “University”, “Institute”, “Laboratory”, “Department”
- “We release code at http”
- “Our internal dataset at …”
- “Acknowledgements” / “Thanks to” / “Grant”

---

## 3) Output required from Verify (internal)
Return a list of issue objects:
- rule_id
- severity: HIGH/MED/LOW
- evidence: exact snippet
- fix: minimal-change suggestion

Then Rewrite produces delta-only sentence edits.

