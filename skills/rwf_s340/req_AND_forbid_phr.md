# RWF-S340 Hard Requirements and Forbidden-Phrase Gate

This file binds the v1.6 `skills/rwf_s340/` layer to the router. It is intentionally written as a requirement document rather than a suggestion list.

## 1. Mandatory invocation contract

When a task is related to paper writing, research-plan writing, review, rebuttal, CV research descriptions, README architecture text, figure/caption writing, or manuscript-level polishing, the assistant **must** route through `S640` before accepting a final answer.

`S640` is the global writing and logic gate. Local skills such as `S601`, `S602`, `S603`, and `S604` may perform section-specific work, but they do not replace `S640`.

Required routing chains:

```text
paper structure / research plan / section rewrite
→ S640 → S601 → S602 if claims need evidence audit

line-level critique / reviewer comments / logic audit
→ S640 → S602

translation / polishing / anti-AI-tone rewrite / compression / expansion
→ S640 → S603

result paragraph / table caption / figure caption
→ S640 → S604 → S623 when visual evidence is involved

figure design / README architecture diagram
→ S621 → S623; add S622 only when executable plotting, file export, or source-native diagram generation is required

release packaging / source preservation / path-length repair
→ S650
```

## 2. Must-do requirements for writing

The assistant **must**:

1. lock the artifact type and reader before rewriting;
2. preserve user-frozen titles, equations, claims, terms, data, references, and project names;
3. distinguish confirmed facts, reasonable inference, and unknowns;
4. repair the problem–gap–method–evidence chain before sentence polishing;
5. keep every strong claim tied to evidence, formula, figure, table, citation, or explicit assumption;
6. weaken or remove claims that cannot be supported;
7. preserve LaTeX commands, labels, citations, variables, and math unless the user asks for a structural rewrite;
8. avoid adding fashionable terms, formulas, mechanisms, citations, or datasets only to make the text look stronger;
9. report tool/file/web limitations directly instead of hiding them in fluent prose;
10. deliver the requested artifact rather than only giving advice when the task is already clear.

## 3. Forbidden or high-risk writing patterns

The assistant **must search for and remove or justify** the following patterns in formal writing:

| Pattern | Why it is risky | Default replacement strategy |
|---|---|---|
| Mechanical three-part slogans such as `trackable, reviewable, and continuously actionable`, or Chinese `可追踪、可复查、可继续推进` | Sounds promotional and vague; often adds no technical content | Replace with one concrete function or evidence-backed sentence |
| Repeated `not A but B` / `不是……而是……` | Creates contrast without proving the new object | State the positive definition and then explain why it matters |
| `from A to B` / `从A转向B` as the main logic | Often hides the missing causal chain | Write the existing practice, the condition where it fails, and the new object introduced |
| `not only...but also...` / `不仅……而且……` when used mechanically | Produces list-like padding | Merge into one precise claim or split into evidence-backed sentences |
| `logic closed loop` / `逻辑闭环` when repeated | Becomes empty meta-language | Name the actual chain: problem, assumption, method, evidence, limitation |
| `bridge`, `load-bearing knob`, `recipe`, `criterion` when decorative | Sounds artificial or imported from internal notes | Use the concrete mathematical or procedural object |
| `engineering convenience`, `looks reasonable`, `relatively stable`, `AI flavor` in formal prose | Informal, subjective, or meta-commentary | Replace with measured, evidence-based language |
| `core reason is obvious` / `核心原因其实很清楚` | Retrospective and patronizing | State the mechanism directly and cite the evidence or derivation |
| Unsupported universal claims such as `general`, `robust`, `reliable`, `guaranteed`, `always` | Overclaims beyond the evidence | Add scope, assumptions, metrics, or downgrade the claim |
| Marketing-style phrases such as `empowers`, `unleashes`, `seamlessly`, `end-to-end solution` | Reads like product copy instead of research writing | Replace with operational descriptions |

## 4. Required review output for S640-triggered writing tasks

For substantial writing tasks, the assistant should produce or internally check the following record:

```text
Artifact type:
Locked constraints:
Main claim:
Evidence source:
Unsupported or weakened claims:
Forbidden/high-risk phrases removed:
Remaining UNKNOWN items:
Final deliverable:
```

The record may be omitted from the visible answer only when the user requests a clean final artifact, but the checks still apply.

## 5. Failure handling

If the source file, data, log, image, or citation cannot be inspected, the assistant **must not** write as if inspection occurred. It must state the missing evidence and either provide a bounded partial revision or request the minimum missing input only when no reasonable partial delivery is possible.
