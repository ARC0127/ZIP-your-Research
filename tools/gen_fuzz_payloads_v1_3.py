#!/usr/bin/env python3
"""Generate high-entropy fuzz payloads for prompt regression testing (v1.3)."""
from __future__ import annotations
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tests" / "prompt_regression" / "fuzz_payloads_v1_3.bin"

def main(size_mb: int = 3) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(os.urandom(size_mb * 1024 * 1024))
    print(f"[OK] wrote {OUT} ({size_mb} MiB)")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--size-mb", type=int, default=3)
    args = ap.parse_args()
    main(args.size_mb)
