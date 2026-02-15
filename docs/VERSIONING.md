# Versioning

## Policy (starting 1.0.0)
We use **Semantic Versioning**: `MAJOR.MINOR.PATCH`.

- MAJOR: breaking changes to file contracts / interface specs.
- MINOR: backward-compatible additions (new skills, workflows, providers).
- PATCH: bugfixes, typos, doc clarifications.

## Legacy tags (pre-1.0)
Earlier internal snapshots existed during development, but are not shipped in this release.
For open-source stability, we start semver at **1.0.0** and treat the `v1.3.2` snapshot as the last pre-1.0 milestone.

## Backward compatibility promise (1.0+)
- Existing skill files are never deleted; deprecated items are kept under `archive/` if needed.
- Interface schemas in `interfaces/specs/` are stable across MINOR releases.
