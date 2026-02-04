# Developer API (1.0.x stability)

## Stable contracts
- Skill files use YAML frontmatter; do not remove existing skill IDs.
- Extension providers use `interfaces/provider_contract.md` and schema `interfaces/specs/provider_result.schema.json`.

## Adding a new provider
- Add a python module under `interfaces/providers/`.
- Keep `search(query, *, limit, config) -> dict`.
- Register in config if you want it enabled by default.

## Release checklist
- Update `VERSION` and `CHANGELOG.md`
- Run `tools/verify_v5_archive.py` (should pass)
- Ensure new files are additive
