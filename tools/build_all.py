#!/usr/bin/env python3
"""Build generated artifacts for v1.0.1.

- writing_engine MASTER prompt
- repository INDEX
- SKILL_MAP (alias)
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def run(script: str):
    p = subprocess.run([sys.executable, str(ROOT / "tools" / script)], cwd=str(ROOT))
    if p.returncode != 0:
        raise SystemExit(p.returncode)

def main():
    run("build.py")
    run("build_index.py")
    run("build_skill_map.py")
    print("OK: build_all completed")

if __name__ == "__main__":
    main()
