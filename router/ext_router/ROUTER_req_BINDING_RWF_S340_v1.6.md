# Router Addendum: RWF-S340 Integrated Skills v1.6

This addendum binds the v1.6 research-writing, figure, and S340 requirement layer into ZYR routing. The integration is mandatory for matching tasks, not a loose recommendation.

## Mandatory engine bindings

| User request | Primary engine | Mandatory companion |
|---|---|---|
| paper structure, Introduction, Method, Experiments, research-plan prose | `writing_engine` | `ext/src/rpws/` + `S601` + `S640` |
| reviewer critique, line-level audit, claim-evidence matrix | `writing_engine` + `proof_engine` | `ext/src/rpws/` + `S602` + `S640` |
| polishing, translation, anti-AI-tone rewrite, compression, expansion | `writing_engine` | `ext/src/rpws/` + `S603` + `S640` |
| result paragraph, table caption, figure caption, ablation narrative | `writing_engine` | `ext/src/rpws/` + `S604` + `S640`; add `S623` for visual evidence |
| figure design, README figure, visual explanation, workflow or architecture diagram | `figure_engine` | inspect `ext/src/figures/` first, then `S621` + `S623`; add `S622` only for executable plotting, file export, or code repair |
| plotting script, Matplotlib figure, SVG/PNG/PDF export | `figure_engine` + `coding_engine` | inspect `ext/src/figures/` first, then `S622` + `S621` + `S623` |
| integrated package, source preservation, zip repair, path-length issue | `S650` | none unless writing/release notes are also edited |

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

`router/route.py` discovers S6xx/S640/S650 files by YAML front matter and also treats `writing_engine`, `figure_engine`, and `rwf_s340_master` as composite candidates. When a query is writing-like, the router should signal the mandatory `writing_engine` + `S640` chain. When a query is figure-like, it should signal the mandatory `figure_engine` + `figures4papers` inspection step.
