# ZYR v1.6.5 Engine-Binding How-To

This guide is the short operational entry point for ZYR v1.6.5.

## 1. Research idea / method / storyline tasks

Use this route when the user asks whether a research idea is valid, how a method should be designed, whether a contribution is real, how a paper storyline should be formed, or whether a theorem/proof/derivation is sound.

```text
proof_engine
→ S203 claim_evidence_matrix
→ S226 logic_consistency_audit
→ S227 method_correctness_audit
→ S230 proof_idea_check
→ S237 theorem_assumption_normalizer when assumptions matter
→ S240 / S241 for pessimistic or progressive verification
→ writing_engine only after the logic is stable
```

Required behavior:
- separate facts, assumptions, inferences, and UNKNOWN items;
- identify the first logical failure before polishing language;
- construct a claim-evidence matrix for any research claim;
- do not let fluent writing hide an unsupported method rationale.

## 2. Writing tasks

Use this route when the user asks to write, rewrite, polish, translate, compress, expand, redline, or structure prose.

```text
writing_engine
→ ext/src/rpws/ (Research-Paper-Writing-Skills)
→ S601 / S602 / S603 / S604 as needed
→ S640 global writing and logic gate
```

If the prose still depends on an unstable idea, method, contribution, or claim-evidence chain, run `proof_engine` first.

## 3. Figure tasks

Use this route when the user asks to draw, redesign, repair, or export a figure.

```text
figure_engine
→ inspect ext/src/figures/ first (figures4papers)
→ S621 / S622 / S623 as needed
→ coding_engine only when execution or code repair is required
```

Required behavior:
- do not start from scratch if a close figures4papers pattern exists;
- preserve source-code-first generation;
- do not replace CSV / table / dataframe input logic with ad hoc hard-coded arrays unless the data source is intentionally changed and documented;
- treat SVG / PNG / PDF as output formats, not substitutes for source generation.

## 4. Code and release tasks

Use this route for debugging, repository repair, package validation, and release checks.

```text
coding_engine
→ smallest sufficient patch
→ closed-loop verification
→ S650 for integrated package / no-omission release validation
```

## 5. Prompt template

```text
Call ZYR v1.6.5 and execute under MODE_LOCK.
Task type: [idea construction / method design / paper audit / Word revision / code repair / experiment analysis / README rewrite / ZIP validation / migration prompt / figure generation].
Control engine / skills: [proof_engine / writing_engine / figure_engine / coding_engine / S203 / S226 / S227 / S230 / S237 / S240 / S241 / S640 / S650 / S601-S604 / S621-S623].
Input materials: [files, text, ZIP, figures, logs, tables, experiment outputs].
Target deliverable: [revised Word, Markdown report, runnable CLI, repaired ZIP, LaTeX, figure, migration prompt].
Hard constraints: [preserve template, redline edits, no fabricated checks, no unsupported claims, preserve figures4papers data-loading logic, etc.].
Final validation: report passed checks, failed checks, unverified items, and the next minimal action.
```
