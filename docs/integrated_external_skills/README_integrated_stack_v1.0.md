# Integrated Research-Writing-Figure Stack

This document describes the v1.6.5 integrated stack.

## Preserved external sources

The external source trees are preserved under `ext/src/`:

- `ext/src/rpws/` — Research-Paper-Writing-Skills;
- `ext/src/awesome/` — awesome-ai-research-writing;
- `ext/src/figures/` — figures4papers.

They are source backends, not duplicated routable skill directories.

## ZYR-native execution layer

The current v1.6.5 execution layer is:

```text
writing tasks
→ writing_engine
→ ext/src/rpws/
→ S601 / S602 / S603 / S604
→ S640

figure tasks
→ figure_engine
→ ext/src/figures/
→ S621 / S622 / S623

package validation
→ S650
```

The integrated wrappers live under `skills/rwf_s340/`. The figure-engine master lives under `skills/figure_engine/MASTER_v1.6.5.md`.

## Non-omission guarantee

The integration keeps the preserved external sources and records them in:

- `manifests/src_manifest.json`
- `manifests/src_FILE_integr_TABLE.md`
- `manifests/SCRIPT_INVENTORY.md`

Use these validators for release checks:

```bash
python tools/validate_no_omission.py
python tools/validate_integrated_sources.py
```

## Routing examples

```bash
python router/route.py "paper writing RPWS S340 logic audit"
python router/route.py "figure engine figures4papers plotting code png pdf"
python router/route.py "ZIP release no omission checksum path length"
```
