#!/usr/bin/env python3
"""Build generated artifacts for v1.3.2.

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
    # v1.3+: writing_engine MASTER
    if (ROOT / "tools" / "build_writing_engine_v1_3.py").exists():
        run("build_writing_engine_v1_3.py")
    run("build_index.py")
    run("build_skill_map.py")
    # v1.3+: coding_engine MASTER
    if (ROOT / "tools" / "build_coding_engine_v1_3.py").exists():
        run("build_coding_engine_v1_3.py")
    print("OK: build_all completed")

if __name__ == "__main__":
    main()
