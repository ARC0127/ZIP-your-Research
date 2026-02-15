# Extension Interfaces (1.0.0)

This repository is primarily a **prompt/skill pack**, but it ships a small, open-source-friendly
extension layer so that users can add their own capabilities without modifying core files.

## Two extension types
1) **Providers**: external knowledge/data fetchers (OpenAlex, Crossref, arXiv, Semantic Scholar, custom).
2) **Hooks**: lightweight post-processors (e.g., normalize results, cache, deduplicate).

## Design goals
- Minimal dependencies (stdlib-first).
- File-based plugins (drop-in Python files).
- Stable schemas (JSON schema + example configs).
- Safe defaults (timeouts, rate-limit guidance, never store secrets in repo).

## Quick start
1) Copy `interfaces/config.example.yaml` → `interfaces/config.yaml` (gitignored if you want).
2) Run:
```bash
python3 tools/ra_cli.py providers list
python3 tools/ra_cli.py providers search --provider openalex --query "offline reinforcement learning" --limit 10
```

## Where to add your own provider
- Create `interfaces/providers/my_provider.py` based on `interfaces/providers/_template_provider.py`.
- Register it in `interfaces/config.yaml`.

See: `interfaces/provider_contract.md`.
