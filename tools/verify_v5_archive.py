#!/usr/bin/env python3
"""Archive verification shim (v5) for 1.0.x compatibility.

Historically referenced by docs. In v1.2 it runs:
- build_all
- strict validate
- drift audit

Usage:
  python tools/verify_v5_archive.py
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def run(cmd):
    print("+", " ".join(cmd))
    p = subprocess.run(cmd, cwd=str(ROOT))
    if p.returncode != 0:
        raise SystemExit(p.returncode)

def main():
    run([sys.executable, "tools/build_all.py"])
    run([sys.executable, "tools/validate_v7_2.py"])
    run([sys.executable, "tools/drift_audit_v1_3.py"])
    print("OK: verify_v5_archive passed")

if __name__ == "__main__":
    main()
