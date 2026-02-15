---
id: S430
name: debug_vibe_core
category: reproducibility
status: stable
triggers:
- vibe coding
- debug
- debugging
- 报错
- traceback
- crash
- 修复
- 回归
- pipeline
- regression
- 代码审计
inputs_required:
- repo_root_or_artifact
- entrypoints_or_commands
- error_trace_or_symptoms
- success_criteria
outputs_required:
- evidence_ledger
- diagnosis_plan
- minimal_patch_plan
- closed_loop_verification
- regression_matrix
quality_gates:
- no_fabrication
- mark_UNKNOWN
- cross_file_check
- closed_loop_first
- minimize_new_files
- copy_paste_ready
---

> **Global invariant (ZIP your Research):** Truthfulness • Trustworthiness • Deep logical reasoning.
> Missing required info → mark **UNKNOWN** and ask minimal questions.

# S430 DEBUG_VIBE_CORE (SSOT)

## Authority
- **S430 is the only normative source** for: `DEBUG_VIBE_CORE`, `VIBE(M2/M3)`, `HCP`, evidence/closure rules, and anti-bloat constraints.
- All other files may provide **templates / examples / navigation**, but MUST NOT introduce new MUST/SHALL-level requirements.
- **Conflict rule:** if any doc/tool/script contradicts S430, treat it as stale and follow S430.

## Requirement keywords
In this repository, the capitalized words **MUST / MUST NOT / SHOULD / SHOULD NOT / MAY** are interpreted in the sense of RFC 2119 (and its update RFC 8174).

---

## 0) Always-on output header requirements
Any response that involves code/debug/experiments MUST include the status banner fields:
- `DEBUG_VIBE_CORE: ON` (always)
- `VIBE: M3` by default; `M2` is optional only if user explicitly selects it
- `HCP: ON` (always; keep short)

If the session is PRE-LOCK, a brief answer is allowed, but if code is involved, **apply M3 discipline** (§3).

---

## 1) Minimal glossary (single-source)
- **DEBUG_VIBE_CORE**: always-on protocol for AI-assisted debugging/coding with strong evidence and closure.
- **VIBE**: operating mode selector.
  - **M3 (default)**: closure-first, minimal change, strong regression.
  - **M2 (optional)**: exploratory refactor/prototyping with explicit complexity budget and cleanup plan.
- **HCP**: Hallucination Check Protocol (always-on, short).
- **Evidence Ledger**: a concrete list of what was actually checked/run + produced artifacts.
- **Closed-loop**: entry → run → artifacts → persistence invariant → reload/val.
- **Regression Matrix**: baseline + main variant + second variant (at minimum) under the same closure gates.

---

## 2) HCP — short but mandatory

> `boot/09_HCP_MINI_v1.3.2.md` is a **display template**. The normative meaning is defined here.

### HCP-1 Evidence Ledger (what was actually checked)
- List file paths that were read/verified (at minimum: modified files + entrypoints + artifact save/load + eval path).
- If a relevant file was not checked: mark **UNKNOWN** (do not guess).

### HCP-2 Cross-file consistency
Any suggested change MUST be checked against:
1) entrypoint(s) / CLI
2) runtime callsites
3) artifact persistence (save/checkpoint)
4) reload/validation path

### HCP-3 Claim discipline
No “it works / improves / fixed” claims unless the closed-loop PASS criteria are met (§4).

---

## 3) VIBE modes

### M3 (default) — minimal change, strong closure
Use when:
- writing/modifying/debugging code
- building experiment pipelines
- anything with saved artifacts (models/checkpoints/results)

M3 output MUST contain:
1) **Problem framing**: symptom, scope, repro command
2) **3 competing hypotheses** + how to disprove each
3) **Minimal patch plan** (prefer modify over new files)
4) **Exact patch** (diff or full file blocks)
5) **Closed-loop verification commands** (§4)
6) **Regression matrix**: baseline + main variant + second variant

**Complexity budget (M3):**
- Do NOT assume `new_files=0`.
- Propose the **minimum** additional units needed.
- User decides the cap in-dialog; if exceeded, explain why the existing structure cannot close the loop.

### M2 (optional) — exploratory refactor / prototyping
Allowed only if user explicitly opts in.
M2 MUST additionally include:
- explicit complexity budget (new files/scripts)
- debt removal plan (what will be merged/deleted after closure)
- milestones (each with closure criteria)

---

## 4) Closed-loop PASS criteria (project-agnostic)
A run is “valid” only if ALL hold:
1) **Change entered the execution graph** (not just “preflight prints”)
2) **Core pipeline completes** (train/infer minimal step)
3) **Artifacts exist** (e.g., ckpt / logs / metrics)
4) **Artifacts persist the change** (e.g., state_dict contains new params; or an equivalent invariant)
5) **Reload path works** (load + val/infer runs without custom monkey-patch errors)

If any fails: mark run INVALID; do not compare metrics.

---

## 5) Minimal debug workflow (generic)
### Step A — Minimal repro (MR)
- Provide the shortest command to reproduce.
- Freeze obvious degrees of freedom (seed/version flags) when possible.

### Step B — Define PASS precisely
- State what “fixed” means in observable terms.

### Step C — Find the evidence breakpoint
Split the system:
- Entry → Build graph → Run → Save → Reload → Eval
Locate the first stage where evidence breaks.

### Step D — Minimal patch
- Prefer single-point change.
- If wrappers are needed, ensure serialization/import paths are stable.

### Step E — Regression
Always re-run:
- baseline (origin)
- main variant
- second variant

---

## 6) Anti-bloat constraints (Occam-first)
- Do not duplicate scripts to “make it work”.
- Any new script MUST either:
  - replace an existing entrypoint (and explicitly deprecate it), or
  - be strictly temporary with a deletion/merge rule after closure.
- Always state: how many files are modified, how many new files are added.

---

## 7) Maintenance & conflict handling
- If you discover duplicated or drifting requirements in other docs, **do not rewrite everything**.
  - Add a short “Non-normative / Refer to S430” banner to that file.
  - Move canonical requirements into S430.
- If a user requests an exception, record it as an explicit “local override” and scope it to the smallest surface.

---

## 8) Executor-agnostic (ChatGPT/Codex/IDE agents)
This protocol is independent of who edits the code.
If a user enables a dedicated executor (e.g., Codex), keep the same closure rules and evidence ledger.
