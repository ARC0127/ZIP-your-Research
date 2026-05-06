# Router Addendum: RWF-S340 Integrated Skills v1.6

This addendum binds the v1.6 research-writing, figure, and S340 requirement layer into ZYR routing. The integration is mandatory for matching tasks, not a loose recommendation.

## Mandatory route bindings

| User request | Primary route | Mandatory companion |
|---|---|---|
| paper structure, Introduction, Method, Experiments, research-plan prose | `S601` | `S640` |
| reviewer critique, line-level audit, claim-evidence matrix | `S602` | `S640` |
| polishing, translation, anti-AI-tone rewrite, compression, expansion | `S603` | `S640` |
| result paragraph, table caption, figure caption, ablation narrative | `S604` | `S640`; add `S623` for visual evidence |
| figure design, README architecture diagram, visual explanation | `S621` | `S623`; add `S622` for executable SVG/PNG/PDF output |
| plotting script, Matplotlib figure, SVG/PNG/PDF export | `S622` | `S621` + `S623` |
| integrated package, source preservation, zip repair, path-length issue | `S650` | none unless writing/release notes are also edited |

## S640 hard gate

For writing-like tasks, `S640` must be applied even when another skill is primary. It enforces the user-authored S340 writing requirements, including forbidden phrase removal, evidence-first claim control, and protection against mechanical or promotional prose.

The hard requirement file is:

- `skills/rwf_s340/req_AND_forbid_phr.md`

## Router behavior

`router/route.py` discovers S6xx/S640/S650 files by YAML front matter and also treats `rwf_s340_master` as a composite candidate. When a query is writing-like, the router prints a mandatory global gate notice for `S640`.
