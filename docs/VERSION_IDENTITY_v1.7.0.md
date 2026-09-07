# ZYR Version Identity (v1.7.0)

This document is the single source of truth for distinguishing the current
suite release from preserved component lineage.

## Authoritative identities

- `SUITE_RELEASE_VERSION = 1.7.0`
- `ACTIVE_MANIFEST_VERSION = 1.7.0`
- `LEGACY_COMPONENT_LINEAGE = 1.3.2` and other explicitly preserved component
  versions such as `1.3`, `1.5`, and `1.6.5`

## Precedence

1. `VERSION` and `skills_manifest.yaml#version` identify the installed
   suite release and must agree.
2. Active entrypoints and user-facing responses must identify the suite as
   `ZIP-your-Research v1.7.0`.
3. A version embedded in a historical filename, module heading, schema,
   regression corpus, or compatibility shim identifies only that component.
4. A component version must never be presented as the current suite release.

## Compatibility policy

Historical v1.3.2 files are retained to preserve references and reproducible
lineage. Active v1.7.0 entrypoints may incorporate those rules or refer to them
as compatibility contracts. Retention does not make v1.3.2 the current suite.

## Active display rule

Current Mode Lock Markdown, JSON `version`, migration prompts, installed skill
metadata and user-facing suite labels must all identify v1.7.0. Use
`boot/00_BOOTSTRAP_PROTOCOL_v1.7.0.md`; old format templates are compatibility
assets, not an alternative current startup. Keep original historical records
unchanged when resuming them; normalize the new working session's identity
without changing scope or inventing new consent.

When the user needs version information, use this form:

```text
ZIP-your-Research suite: v1.7.0
```

Do not display multiple versions as the current suite or repeat a version
banner on every reply. Discuss component lineage only when explicitly needed
for maintenance, source attribution or historical reproduction.
