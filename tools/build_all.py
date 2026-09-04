#!/usr/bin/env python3
"""Build authoritative generated artifacts for suite v1.6.6.

- writing_engine MASTER prompt
- coding_engine MASTER prompt
- proof_engine MASTER prompt
- repository INDEX
- SKILL_MAP (alias)
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def run(script: str, *args: str):
    cmd = [sys.executable]
    if getattr(sys.flags, "no_site", 0):
        cmd.append("-S")
    cmd.extend((str(ROOT / "tools" / script), *args))
    p = subprocess.run(cmd, cwd=str(ROOT))
    if p.returncode != 0:
        raise SystemExit(p.returncode)

def main():
    # The stable facade renders every allowlisted output atomically. Historical
    # v1.3/v1.5 builders remain available as compatibility entrypoints only.
    run("zyr.py", "build")
    print("OK: build_all completed")

if __name__ == "__main__":
    main()
