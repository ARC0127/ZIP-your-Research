# 00 — Overview

This module exists to bridge two realities:

1) The **platform runtime** provides convenience tooling and strict QA expectations under `zyr_runtime_skills/**`.
2) Your **ZYR repo** must remain portable and reproducible outside that runtime.

The solution here is *not* to copy platform internals, but to store:
- a **verifiable snapshot** (hashes and file metadata),
- **portable templates** (openpyxl/python-docx/reportlab + CLI verification),
- **alignment notes** (where platform behavior cannot be reproduced verbatim).

## Scope

- Only the platform skill pack under `zyr_runtime_skills/**` is in scope.
- This module does not attempt to rewrite the entirety of ZYR skills into English; it is intentionally localized.

## Non-goals

- Reproducing platform-private libraries or protobuf APIs.
- Guaranteeing bit-identical rendering between Excel/LibreOffice/platform renderers.

## Deliverable philosophy

- Prefer *user-visible outcomes* and *QA invariants* over API-level parity.
- Treat rendering as a QA step, not a feature guarantee.
