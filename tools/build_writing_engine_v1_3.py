#!/usr/bin/env python3
"""Build Writing Engine MASTER (v1.3.2).

Concatenates markdown modules in `skills/writing_engine/modules/` in lexical order
(excluding files starting with '99_').

Usage:
  python tools/build_writing_engine_v1_3.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES_DIR = ROOT / "skills" / "writing_engine" / "modules"
OUT = ROOT / "skills" / "writing_engine" / "MASTER_v1.3.2.md"

def main():
    pattern = re.compile(r"^\d{2}_.+\.md$")
    modules = [p for p in MODULES_DIR.iterdir() if p.is_file() and pattern.match(p.name) and not p.name.startswith("99_")]
    modules = sorted(modules, key=lambda p: p.name)
    if not modules:
        raise SystemExit("No modules found in skills/writing_engine/modules")

    parts = ["# MASTER v1.3.2 (Writing Engine)\n"]
    for p in modules:
        parts.append(p.read_text(encoding="utf-8").rstrip())
        parts.append("\n\n---\n")
    OUT.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
