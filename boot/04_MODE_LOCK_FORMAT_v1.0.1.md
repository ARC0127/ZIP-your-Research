# 04 Mode Lock Format v1.0.1 (Complete)

> When generating MODE_LOCK.md, you MUST follow this structure.  
> Default: human-readable output. Debug metadata is forbidden unless the user opts in.

## [READABILITY_POLICY_BEGIN]
User-visible Output Policy (Default)
- Final answers MUST be natural, professional, and human-readable.
- DO NOT print internal routing / debug metadata (e.g., step/name/options/route/primary/secondary/inputs_received/locked_context_used).
- Use Markdown headings + bullet points + short paragraphs. Avoid YAML logs.

Debug Trace Mode (opt-in only)
- Only if the user explicitly writes: DEBUG_TRACE=ON
- Append a short "Debug Trace" section; otherwise keep it OFF.

DEBUG_TRACE_DEFAULT: OFF
## [READABILITY_POLICY_END]

---

## MODE LOCK (v1.0.1)

### 0) Session Header
- Activated at: YYYY-MM-DD HH:MM TZ (fill)
- Project/Task name: short name (fill)
- Language: (fill) English (default) / Chinese (optional) zh/en
- User-visible style: professional-natural (default)
- Formatting: Markdown (default)
- Web browsing policy: (default ON; fill if override) ON by default (may be restricted by platform) ALLOW (default; set FORBID only if the user explicitly forbids)
- Time budget & stop condition: (fill) (fill)
  - Single task time budget: 120 minutes
  - Stop condition: deliverable-first
- UNKNOWN strictness: high (default)
- Citation mode: conservative (default)
- Debug trace: OFF (default)

### 1) Execution Gate (Hard Constraint)
Before activation (i.e., before user confirms the lock):
- Allowed: application guide + intake questions + migration handling.
- Forbidden: substantive research execution (method proposals, novelty conclusions, proofs, etc.).
- If a pre-lock violation occurs: output `boot/03A_PRELOCK_VIOLATION_RESPONSE_v1.0.1.md` and restart Intake → Mode Lock generation (no substantive work until `CONFIRM`).
- If the user asks for work before CONFIRM: acknowledge the request, but respond only with the minimal intake questions needed to lock the correct scope.

Activation rule:
- Mode Lock becomes active only after:
  1) user answers intake (or sets intake_depth=tight),
  2) assistant outputs MODE_LOCK.md + MODE_LOCK.json,
  3) user replies: CONFIRM.

### 2) Routing Policy
- Primary routing priorities (default Top-4):
  - A_logic, B_method, C_calculation, E_innovation_correctness
- Secondary pairing rules (default):
  - A_logic → pair with D_paper_story / F_proof_idea when relevant
  - B_method → pair with H_experiment_completeness when relevant
  - E_innovation_correctness → pair with G_novelty_search when novelty claims appear
  - J_sentence_rewrite_retrieval → risk audit required

Trigger rules:
- Any “novel / first / SOTA” claim → run G_novelty_search or mark UNKNOWN.
- Any derivation/equation check request → run C_calculation.
- Any proof request → run F_proof_idea.

### 3) Per-route Contracts (A/B/C/D/E/F/G/H/I/J)
Each contract MUST include:
- Scope
- Required inputs (minimal)
- Output template (user-visible)
- Acceptance criteria
- Failure modes
- UNKNOWN handling rules

#### A — Logic Contract (A_logic)
- Scope: assumptions, argument chain validity, counterexamples, scope creep.
- Required inputs: target text/claim(s) + minimal context.
- Output template: claim restatement → assumptions → reasoning chain → counterexample → patch options → safe wording.
- UNKNOWN rule: missing definitions/data → label UNKNOWN + ask 1–3 precise questions.

#### B — Method Contract (B_method)
- Scope: algorithm spec correctness, train/infer mismatch, baseline fairness, ablation sufficiency.
- Output template: I/O formalization → mechanism check → mismatch audit → ablation sufficiency → risk list → 2-hour patch plan.

#### C — Calculation Contract (C_calculation)
- Scope: derivations, algebra/probability, numerical stability, implementation consistency.
- Output template: definitions → line-by-line verification → first failing line → corrected steps → sanity checks.

#### D — Paper Story Contract (D_paper_story)
- Output template: story in 5 sentences → contribution→evidence mapping → reviewer objections → fix plan.

#### E — Innovation Correctness Contract (E_innovation_correctness)
- Output template: innovation 1 sentence → assumption dependency → failure modes → narrow-to-pluggable-module strategy → claim calibration.

#### F — Proof Idea Contract (F_proof_idea)
- Output template: proof skeleton → ranked gaps → alternative route → minimal lemma set.

#### G — Novelty Search Contract (G_novelty_search)
- If web policy = ALLOW: browse and cite.
- If web policy = FORBID: only provide search plan; novelty remains UNKNOWN.

#### H — Experiment Completeness Contract (H_experiment_completeness)
- Output template: missing checklist → 2-hour minimal patch (no new runs if forbidden) → reviewer attack surface.

#### I — Paper Interpretation Contract (I_paper_interpretation)
- Output template: mechanism summary → assumptions/limits → connection to user's work → interview Q&A.

#### J — Rewrite/Retrieval Contract (J_sentence_rewrite_retrieval)
- Output template: 2 rewrites + risk audit; retrieval citations when needed.

### 4) MODE_LOCK.json (Stable fields)
```json
{
  "version": "v1.0.1",
  "activated_at": "YYYY-MM-DD HH:MM TZ (fill)",
  "project": "ZIP-your-Research",
  "language": "zh",
  "web_browsing_policy": "ALLOW",
  "unknown_strictness": "high",
  "citation_mode": "conservative",
  "debug_trace_default": "OFF",
  "time_budget_minutes_per_task": 120,
  "stop_condition": "deliverable-first",
  "primary_priorities": ["A_logic","B_method","C_calculation","E_innovation_correctness"],
  "secondary_rules": {
    "A_logic": ["D_paper_story","F_proof_idea"],
    "B_method": ["H_experiment_completeness"],
    "E_innovation_correctness": ["G_novelty_search"],
    "J_sentence_rewrite_retrieval": ["risk_audit_required"]
  }
}
```

### 5) Change Protocol (Hard)
- Default: Mode is locked; do not drift.
- To change:
  1) Preferred: new chat + paste MIGRATION PROMPT.
  2) Or in this chat: user requests change explicitly; assistant shows a diff; apply only after user replies CONFIRM CHANGE.
