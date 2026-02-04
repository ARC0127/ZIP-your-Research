# Module 15 — Verification Record Template (to preserve honesty)

Use this template whenever you perform web verification.

---

## Verification Record
- Item: <what rule/fact is being asserted>
- Venue/Topic: <ICML/ICLR/NeurIPS or topic name>
- Source URL: <canonical>
- Source type: official_site / openreview / official_blog / uploaded_template / other
- Opened: true/false
- Status: VERIFIED / UNVERIFIED / UNKNOWN
- Last checked: YYYY-MM-DD
- Extracted lines/snippet: <short excerpt or paraphrase>
- Notes: <conflicts, caveats, etc.>

---

## Minimal policy
Never upgrade UNVERIFIED→VERIFIED without opening the source.
Never fabricate extracted lines.


---

## v4 ADDITIONS — Example records (Append-only)

### Example Record (VERIFIED)
- Item: ICML main body page limit is 8 pages
- Venue/Topic: ICML 2026
- Source URL: https://icml.cc/Conferences/2026/AuthorInstructions
- Source type: official_site
- Opened: true
- Status: VERIFIED
- Last checked: YYYY-MM-DD
- Extracted lines/snippet: “main body ... 8 pages” (paraphrased)
- Notes: References/appendix are outside the limit.

### Example Record (UNVERIFIED)
- Item: Some detail on OpenReview group settings
- Venue/Topic: ICML 2026 OpenReview group
- Source URL: https://openreview.net/group?id=ICML.cc/2026/Conference
- Source type: openreview
- Opened: false (JS rendered)
- Status: UNVERIFIED
- Last checked: YYYY-MM-DD
- Extracted lines/snippet: N/A
- Notes: Use official ICML call-for-papers as source of truth.

