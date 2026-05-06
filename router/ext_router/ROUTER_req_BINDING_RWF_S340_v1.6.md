# Router Addendum: RWF-S340 Integrated Skills v1.6

This addendum binds the v1.6 research-writing, figure, and S340 requirement layer into ZYR routing. The integration is mandatory for matching tasks, not a loose recommendation.

## Mandatory engine bindings

| User request | Primary engine | Mandatory companion |
|---|---|---|
| research idea, method design, contribution definition, theoretical framing, paper storyline | `proof_engine` | `S203` + `S226` + `S227` + `S230`; add `S237`/`S240`/`S241` when assumptions, theorem sketches, or derivations matter |
| paper structure, Introduction, Method, Experiments, research-plan prose | `proof_engine` when logic is being formed, then `writing_engine` | `ext/src/rpws/` + `S601` + `S640` |
| reviewer critique, line-level audit, claim-evidence matrix | `writing_engine` + `proof_engine` | `ext/src/rpws/` + `S602` + `S640` |
| polishing, translation, anti-AI-tone rewrite, compression, expansion | `writing_engine` | `ext/src/rpws/` + `S603` + `S640` |
| result paragraph, table caption, figure caption, ablation narrative | `writing_engine` | `ext/src/rpws/` + `S604` + `S640`; add `S623` for visual evidence |
| figure design, README figure, visual explanation, workflow or architecture diagram | `figure_engine` | inspect `ext/src/figures/` first, then `S621` + `S623`; add `S622` only for executable plotting, file export, or code repair |
| plotting script, Matplotlib figure, SVG/PNG/PDF export | `figure_engine` + `coding_engine` | inspect `ext/src/figures/` first, then `S622` + `S621` + `S623` |
| integrated package, source preservation, zip repair, path-length issue | `S650` | none unless writing/release notes are also edited |

## Proof hard gate

For idea-like and method-like tasks, `proof_engine` is mandatory. This gate must run before writing polish when the user asks for research direction construction, method design, contribution framing, paper storyline construction, or theorem/proof/derivation checking.

Non-negotiable proof rules:
- separate facts, assumptions, inferences, and UNKNOWN items;
- build a claim-evidence matrix before accepting a research claim;
- check the first logical failure before improving wording;
- use `S226` for logic consistency, `S227` for method correctness, `S230` for proof-idea checks, and `S237`/`S240`/`S241` when assumptions or derivations matter;
- `writing_engine` may polish only after the logic is stable or the remaining uncertainty is explicitly labeled.

## Writing hard gate

For writing-like tasks, `writing_engine` is mandatory and `S640` must be applied even when another skill is primary. This enforces the user-authored S340 writing requirements, including forbidden phrase removal, evidence-first claim control, and protection against mechanical or promotional prose.

The hard requirement file is:

- `skills/rwf_s340/req_AND_forbid_phr.md`

## Figure hard gate

For figure-like tasks, `figure_engine` is mandatory. The router must inspect `ext/src/figures/` before proposing a new visual implementation.

Non-negotiable figure rules:
- do not start from scratch if a close figures4papers pattern exists;
- keep source-code-first generation;
- do not replace CSV / table / dataframe input logic with hard-coded arrays unless the data source is intentionally changed and documented;
- treat SVG as an export format, not as permission to bypass the source-generating code.

## Router behavior

`router/route.py` discovers S6xx/S640/S650 files by YAML front matter and also treats `proof_engine`, `writing_engine`, `figure_engine`, and `rwf_s340_master` as composite candidates. When a query is idea-like or method-like, it should signal the mandatory `proof_engine` gate. When a query is writing-like, the router should signal the mandatory `writing_engine` + `S640` chain. When a query is figure-like, it should signal the mandatory `figure_engine` + `figures4papers` inspection step.
