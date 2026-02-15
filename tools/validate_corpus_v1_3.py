#!/usr/bin/env python3
"""Validate prompt regression corpus against the declared schema (v1.3.2).

This is a *deterministic* format check, meant to prevent silent drift.

Usage:
  python tools/validate_corpus_v1_3.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "tests" / "prompt_regression" / "corpus_v1_3.jsonl"
SCHEMA = ROOT / "tests" / "prompt_regression" / "corpus_schema_v1_3.json"


def main() -> None:
    if not CORPUS.exists():
        raise SystemExit(f"Missing corpus: {CORPUS}")
    if not SCHEMA.exists():
        raise SystemExit(f"Missing schema: {SCHEMA}")

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    req = schema.get("entry_required_keys", [])
    allowed = set(schema.get("label_allowed", []))
    max_chars = int(schema.get("text_max_chars", 12000))

    seen_ids: set[str] = set()
    errors: list[str] = []
    n = 0

    for ln, line in enumerate(CORPUS.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if not line.strip():
            continue
        n += 1
        try:
            obj = json.loads(line)
        except Exception as e:
            errors.append(f"L{ln}: invalid json ({e})")
            continue

        for k in req:
            if k not in obj:
                errors.append(f"L{ln}: missing key `{k}`")

        sid = str(obj.get("id", "")).strip()
        if not sid:
            errors.append(f"L{ln}: empty id")
        elif sid in seen_ids:
            errors.append(f"L{ln}: duplicate id `{sid}`")
        else:
            seen_ids.add(sid)

        lab = str(obj.get("label", "")).strip()
        if lab not in allowed:
            errors.append(f"L{ln}: invalid label `{lab}`")

        txt = obj.get("text")
        if not isinstance(txt, str) or not txt.strip():
            errors.append(f"L{ln}: invalid/empty text")
        elif len(txt) > max_chars:
            errors.append(f"L{ln}: text too long ({len(txt)}>{max_chars})")

    if errors:
        print("CORPUS VALIDATION FAILED")
        for e in errors[:200]:
            print(f"- {e}")
        if len(errors) > 200:
            print(f"... and {len(errors)-200} more")
        raise SystemExit(1)

    print(f"CORPUS VALIDATION PASSED: {n} entries")


if __name__ == "__main__":
    main()
