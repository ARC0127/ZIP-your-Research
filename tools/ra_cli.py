#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, pathlib, sys
try:
    import yaml
except Exception:
    yaml = None

# Local imports
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from interfaces.providers import openalex, crossref, arxiv, semantic_scholar
from interfaces.hooks import deduplicate_by_doi

PROVIDERS = {
    "openalex": openalex.search,
    "crossref": crossref.search,
    "arxiv": arxiv.search,
    "semantic_scholar": semantic_scholar.search,
}

def load_config():
    cfg_path = pathlib.Path("interfaces/config.yaml")
    if cfg_path.exists() and yaml:
        return yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    return {}

def cmd_providers_list(_args):
    cfg = load_config()
    prov_cfg = (cfg.get("providers") or {})
    for name in PROVIDERS:
        enabled = (prov_cfg.get(name) or {}).get("enabled", True)
        print(f"{name}\t{'ENABLED' if enabled else 'DISABLED'}")
    return 0

def cmd_providers_search(args):
    cfg = load_config()
    prov_cfg = (cfg.get("providers") or {}).get(args.provider) or {}
    fn = PROVIDERS.get(args.provider)
    if not fn:
        print("Unknown provider:", args.provider, file=sys.stderr)
        return 2
    res = fn(args.query, limit=args.limit, config=prov_cfg)
    items = res.get("items") or []
    # hooks
    hooks_cfg = (cfg.get("hooks") or {})
    if (hooks_cfg.get("deduplicate_by_doi") or {}).get("enabled", False):
        items, meta = deduplicate_by_doi.deduplicate(items)
        res["items"] = items
        res.setdefault("meta", {}).update(meta)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0

def cmd_repropack_init(args):
    """
    Create a minimal reproducibility skeleton for a research repo.
    This prompt pack is not a code repo, so we generate templates users can adapt.
    """
    out = pathlib.Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out/"README_REPRO.md").write_text(
        "# Replication Package Skeleton\n\n"
        "Fill the sections below and keep this file with your release.\n\n"
        "## 1. Target artifacts\n- Table/Figure/Metric to reproduce:\n\n"
        "## 2. Environment\n- OS:\n- Python:\n- CUDA:\n- Dependencies (pip/conda):\n\n"
        "## 3. Data\n- Required datasets:\n- Download instructions:\n- Checksums:\n\n"
        "## 4. Entrypoints\n```bash\n# e.g.\npython train.py --config configs/...\npython eval.py --checkpoint ...\n```\n\n"
        "## 5. Expected outputs\n- Where artifacts appear:\n- Tolerance:\n\n"
        "## 6. Troubleshooting\n- Common errors and fixes:\n",
        encoding="utf-8"
    )
    (out/"artifact_manifest.json").write_text(
        json.dumps({
            "artifacts": [],
            "entrypoints": [],
            "data": [],
            "environment": {},
            "notes": "Populate this manifest for automated checks."
        }, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print("OK: created repropack skeleton at", str(out))
    return 0

def main():
    ap = argparse.ArgumentParser(prog="ra_cli", description="Research Assistant prompt-pack utilities (1.0.0)")
    sp = ap.add_subparsers(dest="cmd", required=True)

    p1 = sp.add_parser("providers", help="Provider tools")
    sp1 = p1.add_subparsers(dest="subcmd", required=True)
    p1l = sp1.add_parser("list", help="List providers")
    p1l.set_defaults(func=cmd_providers_list)
    p1s = sp1.add_parser("search", help="Search with a provider")
    p1s.add_argument("--provider", required=True, choices=sorted(PROVIDERS.keys()))
    p1s.add_argument("--query", required=True)
    p1s.add_argument("--limit", type=int, default=10)
    p1s.set_defaults(func=cmd_providers_search)

    p2 = sp.add_parser("repropack", help="Replication package utilities")
    sp2 = p2.add_subparsers(dest="subcmd", required=True)
    p2i = sp2.add_parser("init", help="Create a repropack skeleton")
    p2i.add_argument("--out-dir", default="repropack")
    p2i.set_defaults(func=cmd_repropack_init)

    args = ap.parse_args()
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
