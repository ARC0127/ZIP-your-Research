# ZYR Version Identity (v1.6.6)

This document is the single source of truth for distinguishing the current
suite release from preserved component lineage.

## Authoritative identities

- `SUITE_RELEASE_VERSION = 1.6.6`
- `ACTIVE_MANIFEST_VERSION = 1.6.6`
- `LEGACY_COMPONENT_LINEAGE = 1.3.2` and other explicitly preserved component
  versions such as `1.3`, `1.5`, and `1.6.5`

## Precedence

1. `VERSION`, `v`, and `skills_manifest.yaml#version` identify the installed
   suite release and must agree.
2. Active entrypoints and user-facing responses must identify the suite as
   `ZIP-your-Research v1.6.6`.
3. A version embedded in a historical filename, module heading, schema,
   regression corpus, or compatibility shim identifies only that component.
4. A component version must never be presented as the current suite release.

## Compatibility policy

Historical v1.3.2 files are retained to preserve references and reproducible
lineage. Active v1.6.6 entrypoints may incorporate those rules or refer to them
as compatibility contracts. Retention does not make v1.3.2 the current suite.

## Active display rule

When version information is visible to a user, use this form:

```text
ZIP-your-Research suite: v1.6.6
Component lineage: v1.3.2-compatible (only when relevant)
```

Do not emit a bare `ZYR v1.3.2` label for the current installation.
