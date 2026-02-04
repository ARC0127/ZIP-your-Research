# Module 10 — Section–Move Map (Detection → Moves → Templates)

This module maps any snippet to:
1) a paper section
2) a rhetorical move
3) a rewrite template
so the assistant can respond deterministically.

---

## 1) Move taxonomy (compact but sufficient)

### Abstract
AB-M1 Problem context
AB-M2 Key gap
AB-M3 Core method (1–2 clauses)
AB-M4 Key results (only if provided/verified)
AB-M5 Broader impact / significance (bounded)

### Introduction
IN-M1 Domain + motivation
IN-M2 Problem statement (formal or operational)
IN-M3 Failure mode / limitation of prior work
IN-M4 Our thesis (one sentence)
IN-M5 Contributions (enumerated but concrete)
IN-M6 Roadmap (optional, one sentence)

### Related Work
RW-M1 Taxonomy of prior approaches
RW-M2 Closest line (most relevant)
RW-M3 Differentiation (what you do that they do not)
RW-M4 Positioning (scope boundary)

### Method
ME-M1 Setup (notation + assumptions)
ME-M2 Objective / loss / training rule
ME-M3 Algorithm pipeline (step-by-step)
ME-M4 Complexity / implementation details
ME-M5 Safety/constraints (if any)

### Experiments
EX-M1 Setup (datasets/tasks)
EX-M2 Baselines + fairness
EX-M3 Metrics + why
EX-M4 Main results
EX-M5 Ablations
EX-M6 Limitations + failure cases

### Discussion / Conclusion
DC-M1 What we learned (not hype)
DC-M2 Limitations
DC-M3 When to use / not use
DC-M4 Future work (grounded)

### Rebuttal
RB-M1 Thank + clarify misconception
RB-M2 Provide evidence (cite your own paper sections)
RB-M3 Commit to edits
RB-M4 Tone control (polite, precise)

---

## 2) Move detection rules (high precision)
Use keywords + structure:
- contributions list → IN-M5
- “we propose / we introduce” early intro → IN-M4
- heavy citations + compare → RW-M*
- algorithm/pseudocode → ME-M3
- metrics/baselines/tables → EX-M*

If ambiguous, choose the move with the least risk (usually Tighten or Specify) and set RISK=LOW.

---

## 3) Micro-templates (per move)
(Use only if it matches; never inject new facts.)

IN-M2: “We study <problem> in <setting>. The goal is to <goal> under <constraint>.”
IN-M3: “Existing <class> assumes <assumption>. In <setting>, this fails because <reason>.”
IN-M4: “We present <method>, which <mechanism> to <benefit>.”
ME-M2: “We optimize <objective>. The update rule is <rule>.”
EX-M2: “We compare against <baselines> using <protocol> to ensure fairness.”

---

## 4) How this maps to delta-only output
Every changed sentence must be assigned exactly one MOVE tag from this list.


---

## v4 ADDITIONS — Move completeness checklists + failure modes (Append-only)

### A) Abstract completeness (fast check)
A good abstract typically answers:
1) What problem?
2) Why hard / what gap?
3) What method (core idea)?
4) What evidence (results) — only if provided/verified
5) Why it matters (bounded)

If any missing, prioritize AB-M1 → AB-M3 before AB-M5.

### B) Introduction completeness (CARS-style without jargon)
Check for:
- IN-M1: domain motivation, not generic
- IN-M2: crisp problem statement (one sentence)
- IN-M3: why prior work fails (one reason)
- IN-M4: what you do (one sentence)
- IN-M5: what artifacts you provide (3–5 bullet contributions)
Optional:
- IN-M6: roadmap

### C) Common failure modes by section
- Abstract: too many adjectives; no mechanism; no evidence pointer.
- Intro: vague “important topic”; no concrete gap; contributions read like slogans.
- Method: lists components but no training/inference rule; missing assumptions.
- Experiments: missing baselines; missing metrics; claims without tables.
- Conclusion: repeats intro; adds new claims; no limitations.

### D) Template library (expanded)
IN-M2 (formal): “We consider <MDP/setting> where the agent must <goal> given <constraints>.”
IN-M3 (failure): “This assumption breaks when <multimodality/OOD/support mismatch> occurs.”
ME-M3 (pipeline): “At test time, we (i) generate candidates, (ii) score them with <criterion>, and (iii) select <argmax>.”
EX-M2 (fairness): “We match training data, evaluation horizons, and compute budgets across baselines.”

