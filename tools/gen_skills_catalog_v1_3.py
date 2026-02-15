#!/usr/bin/env python3
"""Generate human-friendly skills index docs from skills_manifest.yaml (v1.3.2)."""
from __future__ import annotations

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "skills_manifest.yaml"
OUT = ROOT / "docs" / "SKILLS_INDEX_GENERATED_v1.3.md"

def main() -> None:
    data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    skills = data.get("skills", [])
    by_cat: dict[str, list[dict]] = {}
    for s in skills:
        by_cat.setdefault(s.get("category","misc"), []).append(s)

    lines = []
    lines.append("# Skills Index (generated) — v1.3.2\n")
    lines.append("Generated from `skills_manifest.yaml`.\n")
    for cat in sorted(by_cat.keys()):
        lines.append(f"## {cat}\n")
        for it in sorted(by_cat[cat], key=lambda x: x.get("id","")):
            sid = it.get("id", "")
            name = it.get("name", "")
            path = it.get("path", "")
            lines.append(f"- **{sid}** `{name}` — {path}")
        lines.append("")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] wrote {OUT}")

if __name__ == "__main__":
    main()
