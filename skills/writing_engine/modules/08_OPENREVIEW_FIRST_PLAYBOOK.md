# Module 08 — OpenReview-First Playbook (Search → Verify → Fallback)

This module operationalizes “OpenReview-first” while staying honest about failure modes.

---

## 0) Why OpenReview-first is tricky
Some OpenReview pages render critical content via JavaScript. If you cannot read the content, you must label it **UNVERIFIED** and fall back to the official conference site.

---

## 1) OpenReview-first workflow (deterministic)

### Step 1 — Identify the target group id
If venue is known:
- ICML 2026: `ICML.cc/2026/Conference`
- ICLR 2026: `ICLR.cc/2026/Conference`
- NeurIPS 2025: `NeurIPS.cc/2025/Conference`

### Step 2 — Attempt to open the group page
Outcomes:
- SUCCESS (content readable): treat as VERIFIED for the opened lines.
- FAIL (JS “Loading…” or blank): mark as UNVERIFIED, do NOT guess.

### Step 3 — Cross-check with official site
Always open:
- icml.cc / iclr.cc / neurips.cc pages for author instructions/call-for-papers
Treat the official site as the source of truth.

### Step 4 — Store a Verification Record (required)
For each critical rule, store:
- rule_id
- venue
- statement
- source_url
- opened? (true/false)
- status: VERIFIED/UNVERIFIED
- last_checked: YYYY-MM-DD

---

## 2) “Hard constraints” list (always verify)
- page limits
- anonymity requirements (what causes desk rejection)
- supplementary rules
- LLM policies affecting authorship/disclosure
- file size limits
- ethics / prompt injection bans

---

## 3) If the user’s uploaded template conflicts with official
Do:
- Keep template content (do not delete)
- Mark it as: UNVERIFIED / possibly outdated
- Replace operational rules with the official version


---

## v4 ADDITIONS — Practical OpenReview search & verification templates (Append-only)

### 2) Finding rules and submission details (workflow)
When you need venue rules:
1) Open official venue page first (VERIFIED).
2) Attempt OpenReview group open (if readable, use as corroboration).
3) Record everything in Module 15.

### 3) Finding papers on OpenReview (for literature search)
Use these query strategies (do not assume OpenReview returns results without opening a canonical page):

- Strategy OR-1 (venue group → list):
  Open the conference group, then locate “Submissions” / “Papers” listing if available.

- Strategy OR-2 (keyword search via web):
  Use site-limited search:
  `site:openreview.net <keyword> <venue> <year> pdf`
  Then open the canonical OpenReview forum page and confirm:
  - title
  - authors (if available; note anonymity during review)
  - PDF link exists
  - decision/status if visible

- Strategy OR-3 (fallback to arXiv/publisher):
  If OpenReview is unreadable, switch to arXiv/publisher pages and mark OpenReview as UNVERIFIED.

### 4) OpenReview identity & account constraints (from official venues)
Some venues require all authors to have OpenReview accounts and recommend institutional emails.
Treat these as venue rules only when VERIFIED on official sites.

### 5) Failure modes and honesty contract
If any OpenReview page:
- shows “Loading…”
- provides no readable text
- blocks content
then:
- do not infer hidden content
- mark as UNVERIFIED
- rely on official venue pages

