# 00 — Overview

This module exists to bridge two realities:

1) Some useful runtime behaviors live in external or platform-specific skill packs.
2) Your **ZYR repo** must remain portable and reproducible outside those runtimes.

The solution here is *not* to copy runtime internals verbatim, but to store:
- a **verifiable snapshot** (hashes and file metadata),
- **portable templates or interface shapes**,
- **alignment notes** (where source behavior cannot or should not be reproduced verbatim).

Current source families:

- **Platform runtime pack** under `zyr_runtime_skills/**`
- **Claude Code runtime architecture** from `claude-code-sourcemap-main/restored-src/**`

## Scope

- Runtime-facing source packs and architectures that offer reusable operational structure.
- The current module explicitly covers:
  - `zyr_runtime_skills/**`
  - selected Claude Code runtime files relevant to tools, sessions, skills, plugins, and remote execution boundaries
- This module does not attempt to rewrite the entirety of ZYR skills into English; it is intentionally localized.

## Non-goals

- Reproducing platform-private libraries or protobuf APIs.
- Reproducing Anthropic private auth flows, entitlement checks, or backend contracts.
- Guaranteeing bit-identical rendering between Excel/LibreOffice/platform renderers.
- Treating source snapshots as product-clone blueprints.

## Deliverable philosophy

- Prefer *user-visible outcomes* and *QA invariants* over API-level parity.
- Treat rendering as a QA step, not a feature guarantee.
- Treat runtime contracts as portable abstractions, not vendor-specific glue.
- Separate:
  - what ZYR should absorb
  - what ZYR should only reference
  - what ZYR must explicitly reject
