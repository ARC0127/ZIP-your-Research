#!/usr/bin/env python3
"""Render intake questions from an intake profile YAML (v8.2 shim).

This is a maintainer convenience tool referenced by older docs.

Usage:
  python tools/render_intake_questions_v8_2.py --profile router/intake_profile_v1.3.2.yaml
"""

import argparse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default="router/intake_profile_v1.3.2.yaml")
    args = ap.parse_args()

    prof = (ROOT / args.profile).read_text(encoding="utf-8")
    data = yaml.safe_load(prof) or {}
    blocks = data.get("intake_blocks", []) or []
    print(f"# Intake questions from {args.profile}\n")
    for b in blocks:
        title = b.get("title","(untitled)")
        qs = b.get("questions", []) or []
        print(f"## {title}")
        for q in qs:
            print(f"- {q}")
        print()

if __name__ == "__main__":
    main()
