# Release Audit — v1.6.4 Proof-Engine Binding Patch

This patch keeps the package version at `1.6.4` and strengthens the mandatory proof-engine route.

## Main changes

- research idea / method / storyline tasks now explicitly require `proof_engine`;
- writing tasks still require `writing_engine`;
- figure tasks still require `figure_engine`;
- `docs/how_to_use/` now contains the current v1.6.4 engine-binding guides;
- stale v1.3.2 how-to PDF and old generator scripts were removed.

## Required routing

```text
idea / method / storyline → proof_engine
writing → writing_engine
figure-making → figure_engine
code repair → coding_engine
release validation → S650
```
