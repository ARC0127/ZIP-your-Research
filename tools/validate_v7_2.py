#!/usr/bin/env python3
"""Validator shim for legacy docs (v7_2).

This repository now uses `tools/validate_v1_3.py` in strict mode.

Usage:
  python tools/validate_v7_2.py
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    p = subprocess.run([sys.executable, str(ROOT / "tools" / "validate_v1_3.py")], cwd=str(ROOT))
    raise SystemExit(p.returncode)

if __name__ == "__main__":
    main()
