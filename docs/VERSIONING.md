# Versioning

## Current suite identity

The current release is **ZYR v1.7.0**. Component filenames may retain older
suffixes for compatibility and provenance. See `docs/VERSION_IDENTITY_v1.7.0.md`
for the authoritative precedence rules.

## Policy (starting 1.0.0)
We use **Semantic Versioning**: `MAJOR.MINOR.PATCH`.

- MAJOR: breaking changes to file contracts / interface specs.
- MINOR: backward-compatible additions (new skills, workflows, providers).
- PATCH: bugfixes, typos, doc clarifications.

## Legacy tags (pre-1.0)
Earlier internal snapshots existed during development and some are retained as
compatibility assets. The `v1.3.2` label is historical component lineage; it is
not the current suite version.

## Backward compatibility promise (1.0+)
- Preserve active skill identities and distinct protocols. Reviewed identical
  aliases and superseded entrypoints can be retired with references migrated;
  historical files remain recoverable in Git, without another archive directory.
- Interface schemas in `interfaces/specs/` are stable across MINOR releases.
