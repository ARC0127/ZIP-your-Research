# ZYR v1.6.2 README Usage Extension Audit

## Scope

This update modifies the v1.6.1 repaired package only at the README/usage-guidance layer. It keeps the repaired short-path repository layout and the v1.5/v1.6 execution logic unchanged.

## Changed files

- `README.md`: added the high-efficiency use protocol, bilingual route-bound invocation template, ready-to-use prompt recipes, and low-efficiency prompt warning.
- `CHANGELOG.md`: added the v1.6.2 changelog entry.
- `v`: bumped package version from `1.6.1` to `1.6.2`.
- `skills_manifest.yaml`: bumped manifest version from `1.6.1` to `1.6.2`.
- `manifests/src_manifest.json`: updated package metadata and registered this README usage audit as an added release file.
- `manifests/CHECKSUMS.sha256`: regenerated after the README usage update.

## README additions

The README now explicitly states that efficient ZYR use should specify:

1. task type;
2. engine / skill route;
3. input materials;
4. target deliverable;
5. hard constraints;
6. final validation requirements.

It also includes ready-to-use prompts for:

- paper logic audit;
- Word redline revision;
- research-plan or manuscript restructuring;
- code repair or repository cleanup;
- experiment result analysis;
- README / ZIP release validation;
- migration prompt or append-only project handoff.

## Non-changes

- No source file from `ext/src/` was modified.
- No core boot, router, proof, writing, coding, figure, or validation skill file was modified.
- No algorithmic or execution semantics were changed.

## Acceptance criteria

- README contains the task-to-engine routing table.
- README contains explicit “low-efficiency vs high-efficiency invocation” guidance.
- README contains route-bound templates for the major expected workflows.
- Package validation scripts still pass after the README update.
