# Module 07 — Venue Rules (ICML 2026 / NeurIPS 2025 / ICLR 2026) — Programmatic, Official-First

This module turns **venue requirements** into **checkable rules**.
It is invoked during Verify when `venue_lock=true`.

**Source priority (hard):**
1) Official venue site (VERIFIED if opened)
2) OpenReview venue group (only if readable; otherwise UNVERIFIED)
3) Official venue blog (policy clarifications)
4) Local templates (PDF/TeX) as UNVERIFIED backups

---

## 0) How to use this module
1) Set `VENUE_TARGET` = ICML / NeurIPS / ICLR / Unknown
2) If Unknown, do not enforce venue-specific constraints. Use generic academic constraints only.
3) If a rule is not verifiable in an opened official source, mark it UNVERIFIED.

---

## 1) ICML 2026 — VERIFIED rules (official: icml.cc)

### 1.1 Submission format & page limits (VERIFIED)
Rule ICML-R1:
- Main body ≤ 8 pages (strict). References and appendices can follow with no page limit.
- All in a **single PDF**.
- If main body > 8 pages → automatic rejection.

Rule ICML-R2:
- PDF size limit: submission ≤ 50MB; camera-ready ≤ 20MB.

Rule ICML-R3:
- Submissions must be anonymized and follow the required format; non-compliance → automatic rejection.

Rule ICML-R4:
- Submission is handled via OpenReview.

Implementation check (pseudo):
- detect `\usepackage{icml2026}` or `icml2026.sty`
- locate page count (if PDF is given) or require user to confirm
- scan for author names/affiliations/acknowledgements; flag

(VERIFIED source: https://icml.cc/Conferences/2026/AuthorInstructions)

### 1.2 Double-blind & anonymization (VERIFIED)
Rule ICML-A1:
- Double-blind is mandatory.
- Refer to prior work in third person where possible.
- Do not include acknowledgements, grant numbers, or links to public code repositories.
- Papers revealing identity (explicitly or implicitly) → rejected.

Rule ICML-A2 (rebuttal/response):
- Response must not contain identifying info.
- Do not include non-anonymized URLs / personal websites / shortened URLs.

(VERIFIED source: https://icml.cc/Conferences/2026/AuthorInstructions)

### 1.3 Generative AI considerations (VERIFIED)
Rule ICML-G1:
- Authors may use generative AI tools, but must take full responsibility for paper content.
- LLMs are not eligible for authorship.
- Prompt injection is strictly forbidden and can cause desk rejection.
- Authors are encouraged to explain notable AI usage.

(VERIFIED source: https://icml.cc/Conferences/2026/CallForPapers)

### 1.4 Impact & lay summary (VERIFIED)
Rule ICML-I1:
- Accepted papers require a lay summary in OpenReview at camera-ready time.

(VERIFIED source: https://icml.cc/Conferences/2026/CallForPapers)

---

## 2) NeurIPS 2025 — VERIFIED rules (official: neurips.cc)
**Note:** This is the latest NeurIPS official content we verified now. If user targets NeurIPS 2026+, you must re-check the official site and mark this section as UNVERIFIED-TRANSFER.

### 2.1 Double-blind reviewing (VERIFIED)
Rule NIPS-A1:
- Submissions must be anonymized; no identifying info in main or supplementary.
- No acknowledgements at submission.
- Self-citations must preserve anonymity (third-person phrasing).

(VERIFIED source: https://neurips.cc/Conferences/2025/CallForPapers)

### 2.2 LLM policy for authors (VERIFIED)
Rule NIPS-G1:
- LLMs are allowed; if LLM usage is part of methodology, it should be described.
- Authors are responsible for all content (text, figures, references).
- LLM used only for editing/formatting typically need not be declared.
- LLMs cannot be listed as authors.

(VERIFIED source: https://neurips.cc/Conferences/2025/LLM)

---

## 3) ICLR 2026 — VERIFIED rules (official: iclr.cc)
### 3.1 Paper length (VERIFIED)
Rule ICLR-R1:
- At submission: main text ≤ 9 pages.
- During rebuttal/camera-ready: limit increases to 10 pages.
- References do not count; appendices allowed after bibliography (reviewers not required to read).

(VERIFIED source: https://iclr.cc/Conferences/2026/AuthorGuide)

### 3.2 Double-blind & desk rejection (VERIFIED)
Rule ICLR-A1:
- Double blind; identity revealed in main or supplementary → desk rejected.
- Related arXiv papers by same authors do not break anonymity if cited in third person.

(VERIFIED source: https://iclr.cc/Conferences/2026/AuthorGuide)

### 3.3 LLM usage disclosure (VERIFIED via official ICLR blog)
Rule ICLR-G1:
- Any use of an LLM must be disclosed; authors remain responsible for content.
- Non-disclosure can trigger desk rejection.

(VERIFIED source: https://blog.iclr.cc/2025/08/26/policies-on-large-language-model-usage-at-iclr-2026/)

---

## 4) Programmatic compliance checks (shared templates)

### 4.1 Page-limit risk scanner
If input is LaTeX:
- detect venue class/style
- estimate pages if PDF is given; else require user confirmation
- flag likely overflow (too many figures/tables early)

### 4.2 Anonymity scanner
Search for:
- author names, affiliations, emails
- acknowledgements section
- grant numbers
- links to non-anonymized repositories
Then recommend edits that remove identifying signals without losing meaning.

### 4.3 Policy disclosure helper
If the user asks "should we disclose LLM usage?":
- follow venue policy (ICML allows; NeurIPS allows; ICLR requires disclosure per blog)
- never provide advice that violates policy


---

## v3 ADDITIONS — More VERIFIED “hard constraints” + programmatic checks (Append-only)

### A) ICML 2026 — make the “hard constraints” checkable (VERIFIED)
Add these explicit checks (some are directly stated on the official site; others are safe operationalizations of those statements):

**ICML-PAGE-LIMIT**  
- If the user provides a PDF: count pages; ensure the *main body* is ≤ 8.  
- If only LaTeX is provided: require a compiled page count or user confirmation; otherwise keep risk=MED.

**ICML-ANONYMITY-RED-FLAGS**  
Flag and require revision if you detect:
- \author / \thanks / affiliations / email patterns
- acknowledgements section
- “We release code at …” with a real repository link
- “In our lab / at <institution>” phrases
- grant numbers

**ICML-SINGLE-PDF**  
Ensure the submission is a single PDF, not split files.

**ICML-SIZE-LIMIT**  
If user provides the PDF file size, ensure ≤ 50MB for submission.

These checks are grounded in the official author instructions and call-for-papers constraints.

(VERIFIED sources:  
- https://icml.cc/Conferences/2026/AuthorInstructions  
- https://icml.cc/Conferences/2026/CallForPapers )

### B) NeurIPS 2025 — Paper Formatting Instructions (VERIFIED)
Add explicit rules from the official “Call for Papers” page:

Rule NIPS-R1:
- Submissions must be a single PDF that includes, in suggested order:
  (1) paper content, (2) references, (3) NeurIPS paper checklist.
- Main text limited to **nine content pages** including figures/tables.
- References/checklist/optional technical appendices do not count as content pages.
- Accepted papers can add **one additional content page** for camera-ready.
- Max file size for main paper submission: **50MB**.
- Must use the official NeurIPS 2025 LaTeX style; violations may be rejected.

Rule NIPS-R2:
- Mandatory abstract deadline: avoid placeholder abstracts; placeholder risk removal without consideration.
- After abstract deadline, adding/removing authors not allowed.

(VERIFIED source: https://nips.cc/Conferences/2025/CallForPapers )

### C) ICLR 2026 — Expanded “desk reject” triggers (VERIFIED)
From the official Author Guide:
- Identity revealed in main text or supplementary → desk rejection.
- Main text length limit at submission: 9 pages; rebuttal/camera-ready: 10 pages.

(VERIFIED source: https://iclr.cc/Conferences/2026/AuthorGuide )

### D) Cross-venue compliance engine (pseudo-code)
Use this skeleton when venue_lock=true:

1) Load ruleset by VENUE_TARGET
2) Run:
   - anonymity_scan()
   - page_limit_check()
   - formatting_scan()
   - policy_disclosure_check()
3) For every violation:
   - create an issue object: {rule_id, severity, evidence_snippet, fix_hint}
4) During Rewrite:
   - only apply fixes that do not introduce new factual claims



---

## v4 ADDITIONS — ICML 2026 policies (impact statements, ethics, deadlines) (Append-only)

### ICML 2026 — Impact Statement (VERIFIED; enforce when venue_lock=true)
Rule ICML-I2:
- Authors are required to include an Impact Statement discussing broader impacts and ethical aspects.
- It should be a separate section at the end of the paper (co-located with Acknowledgements, before References).
- It does not count toward page limit.

Operationalization:
- If the user has no domain-specific ethical concerns, allow the minimal boilerplate statement, but do not invent impacts.
- If the paper touches safety/industrial control, require a more specific statement grounded in the paper.

(VERIFIED source: https://icml.cc/Conferences/2026/CallForPapers )

### ICML 2026 — Deadlines & “placeholder abstract” risk (VERIFIED)
Rule ICML-D1:
- Abstract and paper deadlines are strict; no extensions.
- Submissions with placeholder abstracts that are substantially rewritten risk being removed without consideration.
- Author list cannot be changed after the abstract deadline.

Operationalization:
- If user asks for a major abstract rewrite after abstract deadline, warn (as policy) and suggest minimal edits that preserve substance.

(VERIFIED source: https://icml.cc/Conferences/2026/CallForPapers )

### ICML 2026 — Ethical conduct + prompt injection ban (VERIFIED)
Rule ICML-E1:
- Plagiarism and prompt injection are forbidden; unethical behavior can lead to rejection and sanctions.
- Advertising work as under ICML submission during review is forbidden.

Operationalization:
- Do not insert hidden instructions, steganography, or review-manipulating text.
- Do not suggest “evading detection”; style guidance is for clarity, not concealment.

(VERIFIED source: https://icml.cc/Conferences/2026/CallForPapers )

---

## v4 ADDITIONS — NeurIPS 2025: deadlines and abstract rules (Append-only)

### NeurIPS 2025 — Abstract deadline risk (VERIFIED)
Rule NIPS-D1:
- Mandatory abstract deadline; abstracts should be accurate and non-placeholder.
- Submissions with placeholder abstracts that are substantially rewritten risk being removed without consideration.
- After abstract deadline, adding/removing authors is not allowed.

Operationalization:
- If user requests major abstract rewrite after deadline, warn about risk; recommend minimal edits.

(VERIFIED source: https://nips.cc/Conferences/2025/CallForPapers )

