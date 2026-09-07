# Contributing to ZIP-your-Research v1.7.0

Preserve active skill identities, scientific evidence rules, explicit approval
boundaries and third-party attribution. Apply
[the current resource profile](boot/14_RESOURCE_PROPORTIONAL_EXECUTION_v1.md)
when interpreting retained protocols.

## Scope and skill selection

Choose a primary skill for the requested result. Local prose can use S603;
integrated manuscript review retains its applicable global checks. Mathematical
validity uses proof verification; actual figure generation uses its available
backend. Missing sources and unexecuted checks must remain explicit. Do not
turn optional companion lists into a mandatory pipeline for every task.

## Add or change a skill

1. Use [the skill template](templates/skill_template.md) and an unused Sxxx ID.
2. Specify inputs, outputs, quality gates and a concrete example.
3. Register the canonical path in `skills_manifest.yaml` and maintain the short
   discovery description in `manifests/codex_descriptions_v1.yaml`.
4. Update generated files with `python -B tools/zyr.py build` when affected.
5. Validate the changed behavior and retain its source and authority boundaries.

Writing-engine modules remain verbatim source inputs. Do not duplicate a skill
under a second pathname. Active protocols and licensed source material must not
be removed merely to reduce the file count.

## Retire obsolete files

Compare content and references first. Keep a canonical replacement for duplicate
skills, migrate live references, and record the exact old bytes/hash and reason
in `manifests/retired_documents_v1.json`. The cleanup tool refuses active skills,
source modules and changed copies. Update build or compatibility requirements
when the dependency itself is intentionally retired; do not keep dead files just
to satisfy an obsolete file-existence check.

Git retains history. Do not create another archive folder or one report per
maintenance run. Keep the README usage guide complete and replace its single
latest-update section. Cache files and generated operation reports stay untracked.

For an existing installation, follow [update and rollback](docs/RESOURCE_PROFILE_v1.md).

## Validation and delivery

Run from the repository root:

```bash
python -m pip install -r requirements.txt
python -B tools/zyr.py build --check
python -B tools/zyr.py check --ci
python -B tools/zyr.py route-test
python -B tools/prune_retired_docs_v1.py --root . --check
```

CI runs the regression suite and checks the extracted release. Release changes
also follow [the packaging guide](docs/RELEASE.md). Historical source inventories
are provenance snapshots, not the current repository file list; source-specific
integrity checks require the matching source inventory.

Describe the result, relevant checks and remaining limitations. Structural tests
establish package integrity and implemented behavior, not scientific improvement
or measured token savings. Obtain the applicable authorization before commit,
push, publication or other external actions.
