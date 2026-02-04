#!/usr/bin/env python3
"""Create a clean release zip (exclude .git and build artifacts).

This is for users who want to copy/paste prompts without repo history.

Usage:
  python tools/make_release.py --version v1.0.1
"""

import argparse
import zipfile
from pathlib import Path

EXCLUDE_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache"}

def should_exclude(path: Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDE_DIRS:
        return True
    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", default="v1.0.1")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[1]
    out = Path(args.out) if args.out else root / f"ZIP-your-Research_{args.version}_release.zip"

    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in root.rglob("*"):
            if p.is_dir():
                continue
            if should_exclude(p):
                continue
            rel = p.relative_to(root)
            z.write(p, arcname=f"ZIP-your-Research/{rel}")

    print(f"OK: wrote {out}")

if __name__ == "__main__":
    main()
