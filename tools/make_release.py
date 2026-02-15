#!/usr/bin/env python3
"""Create a clean release zip (exclude .git and build artifacts).

This is for users who want to copy/paste prompts without repo history.

Usage:
  python tools/make_release.py
  python tools/make_release.py --version v1.3.2
"""

import argparse
import zipfile
from pathlib import Path

EXCLUDE_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache"}
EXCLUDE_SUFFIXES = {".zip", ".7z", ".tar", ".gz", ".bz2", ".xz"}


def should_exclude(path: Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDE_DIRS:
        return True
    # prevent nested archives inside release packages
    if path.suffix.lower() in EXCLUDE_SUFFIXES:
        return True
    return False


def read_default_version(root: Path) -> str:
    vfile = root / "VERSION"
    if vfile.exists():
        v = vfile.read_text(encoding="utf-8", errors="replace").strip()
        if v:
            return f"v{v}" if not v.startswith("v") else v
    return "v1.3.2"


def main():
    root = Path(__file__).resolve().parents[1]

    ap = argparse.ArgumentParser()
    ap.add_argument("--version", default=None, help="e.g., v1.3.2 (default: read from VERSION)")
    ap.add_argument("--out", default="", help="output path; default uses ZIP-your-Research_<version>_release.zip")
    args = ap.parse_args()

    version = args.version or read_default_version(root)
    out = Path(args.out) if args.out else root / f"ZIP-your-Research_{version}_release.zip"

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
