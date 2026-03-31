#!/usr/bin/env python3
"""Generate router/SKILL_MAP_v1.3.2.md from skills front matter.

This avoids manual drift between skills and the skill map.
"""

import re
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
OUT = ROOT / "router" / "SKILL_MAP_v1.3.2.md"

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
SKILL_FILENAME_RE = re.compile(r"^S\d+_.*\.md$")

ORDER = ["research_core", "experiments", "reproducibility", "paper_ops", "composite"]

def parse_front_matter(text: str):
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return None
    return yaml.safe_load(m.group(1)) or {}

def iter_skill_files():
    for p in sorted(SKILLS_DIR.rglob("*.md")):
        rel = p.relative_to(SKILLS_DIR).as_posix()
        if "platform_oai_skills/rewrites/" in rel:
            continue
        if SKILL_FILENAME_RE.match(p.name):
            yield p


def load_manifest_composites():
    manifest = ROOT / "skills_manifest.yaml"
    if not manifest.exists():
        return []
    data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
    composites = []
    for item in data.get("skills", []) or []:
        if str(item.get("category", "")).strip() != "composite":
            continue
        sid = str(item.get("id", "")).strip()
        name = str(item.get("name", sid)).strip()
        path = str(item.get("path", "")).strip()
        outputs = item.get("outputs", []) or []
        trig = "generated composite"
        if outputs:
            trig += f"; outputs: {', '.join(str(x) for x in outputs[:3])}"
        if sid and path:
            composites.append((10**8, sid, name, path, trig))
    return composites

def idnum(sid: str) -> int:
    m = re.match(r"S(\d+)", sid)
    return int(m.group(1)) if m else 10**9

def main():
    buckets = defaultdict(list)
    for p in iter_skill_files():
        fm = parse_front_matter(p.read_text(encoding="utf-8"))
        if not fm:
            continue
        cat = str(fm.get("category", "uncategorized"))
        sid = str(fm.get("id", p.stem))
        name = str(fm.get("name", p.stem))
        triggers = fm.get("triggers", []) or []
        if isinstance(triggers, str):
            triggers = [triggers]
        trig = ", ".join([str(t) for t in triggers[:6]])
        if len(triggers) > 6:
            trig += ", ..."
        buckets[cat].append((idnum(sid), sid, name, p.relative_to(ROOT).as_posix(), trig))

    for item in load_manifest_composites():
        buckets["composite"].append(item)

    for cat in buckets:
        buckets[cat].sort()

    lines = [
        "# Skill Map (v1.3.2)",
        "",
        "This is a human-readable map from intents → primary skills.",
        "",
        "Prefer using **one** primary skill per task.",
        "",
    ]
    for cat in ORDER:
        lines.append(f"## {cat}")
        lines.append("")
        for _, sid, name, rel, trig in buckets.get(cat, []):
            lines.append(f"- **{sid}** `{name}` — {rel}")
            lines.append(f"  - triggers: {trig}")
        lines.append("")

    OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
