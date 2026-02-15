# Contributing (v1.3.2)

Thanks for improving this prompt/skill library.

## What to contribute
- New skills (`skills/**/S*.md`) that are copy/paste-ready
- Examples and rubrics for existing skills
- Validation / build improvements (tools/)
- Documentation improvements (docs/)

## Contribution rules (hard)
- Do not fabricate facts. If a claim needs evidence, label UNKNOWN and add verification steps.
- Do not delete existing skills or writing_engine modules.
- Keep changes additive. If you need to change behavior, add a new file and update CI.

## Adding a new skill
1) Copy `templates/skill_template.md`
2) Choose an ID in the correct segment:
   - S2xx research_core
   - S3xx experiments
   - S4xx reproducibility
   - S5xx paper_ops
3) Fill YAML front matter and the prompt body
4) Add at least one Example
5) Append an entry to `skills_manifest.yaml`
6) Run:
   - `python tools/build_all.py`
   - `python tools/validate_v7_1.py`

## Pull request checklist
- [ ] CI (v1.3.2) passes
- [ ] New skills include Output Contract + Example
- [ ] No deletion of existing content
