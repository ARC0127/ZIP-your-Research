#!/usr/bin/env python3
"""Compatibility validator facade for suite v1.7.0.

Runs the structural compatibility core followed by the release-identity gate.

Usage:
  python tools/validate_v7_3.py
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    for script in ("validate_v1_3.py", "validate_release_identity_v1_7_0.py"):
        cmd = [sys.executable]
        if getattr(sys.flags, "no_site", 0):
            cmd.append("-S")
        cmd.append(str(ROOT / "tools" / script))
        p = subprocess.run(cmd, cwd=str(ROOT))
        if p.returncode != 0:
            raise SystemExit(p.returncode)
    print("Validation passed: structural compatibility + v1.7.0 release identity")

if __name__ == "__main__":
    main()
