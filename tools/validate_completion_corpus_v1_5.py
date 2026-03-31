#!/usr/bin/env python3
"""Validate completion-compliance corpus for v1.5 alignment.

Usage:
  python tools/validate_completion_corpus_v1_5.py
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "tests" / "compliance_v1_5" / "corpus_v1_5.jsonl"
SCHEMA = ROOT / "tests" / "compliance_v1_5" / "corpus_schema_v1_5.json"


def main() -> None:
    if not CORPUS.exists():
        raise SystemExit(f"Missing corpus: {CORPUS}")
    if not SCHEMA.exists():
        raise SystemExit(f"Missing schema: {SCHEMA}")

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    req = schema.get("entry_required_keys", [])
    text_max_chars = int(schema.get("text_max_chars", 20000))
    allowed_patterns = set(schema.get("pattern_allowed", []))
    allowed_actions = set(schema.get("expected_action_allowed", []))
    allowed_modes = set(schema.get("expected_response_mode_allowed", []))
    allowed_completion = set(schema.get("expected_completion_policy_allowed", []))
    allowed_blocker = set(schema.get("expected_blocker_policy_allowed", []))
    min_counts = schema.get("required_pattern_min_counts", {}) or {}

    errors: list[str] = []
    seen_ids: set[str] = set()
    pattern_counts: Counter[str] = Counter()
    n = 0

    for ln, line in enumerate(CORPUS.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if not line.strip():
            continue
        n += 1
        try:
            obj = json.loads(line)
        except Exception as exc:
            errors.append(f"L{ln}: invalid json ({exc})")
            continue

        for key in req:
            if key not in obj:
                errors.append(f"L{ln}: missing key `{key}`")

        sid = str(obj.get("id", "")).strip()
        if not sid:
            errors.append(f"L{ln}: empty id")
        elif sid in seen_ids:
            errors.append(f"L{ln}: duplicate id `{sid}`")
        else:
            seen_ids.add(sid)

        pattern = str(obj.get("pattern", "")).strip()
        if pattern not in allowed_patterns:
            errors.append(f"L{ln}: invalid pattern `{pattern}`")
        else:
            pattern_counts[pattern] += 1

        action = str(obj.get("expected_action", "")).strip()
        if action not in allowed_actions:
            errors.append(f"L{ln}: invalid expected_action `{action}`")

        mode = str(obj.get("expected_response_mode", "")).strip()
        if mode not in allowed_modes:
            errors.append(f"L{ln}: invalid expected_response_mode `{mode}`")

        completion = str(obj.get("expected_completion_policy", "")).strip()
        if completion not in allowed_completion:
            errors.append(f"L{ln}: invalid expected_completion_policy `{completion}`")

        blocker = str(obj.get("expected_blocker_policy", "")).strip()
        if blocker not in allowed_blocker:
            errors.append(f"L{ln}: invalid expected_blocker_policy `{blocker}`")

        text = obj.get("text")
        if not isinstance(text, str) or not text.strip():
            errors.append(f"L{ln}: invalid/empty text")
        elif len(text) > text_max_chars:
            errors.append(f"L{ln}: text too long ({len(text)}>{text_max_chars})")

    for pattern, min_count in sorted(min_counts.items()):
        if pattern_counts.get(pattern, 0) < int(min_count):
            errors.append(
                f"pattern `{pattern}` count too low ({pattern_counts.get(pattern, 0)}<{int(min_count)})"
            )

    if errors:
        print("COMPLIANCE CORPUS VALIDATION FAILED")
        for err in errors[:200]:
            print(f"- {err}")
        if len(errors) > 200:
            print(f"... and {len(errors) - 200} more")
        raise SystemExit(1)

    print(f"COMPLIANCE CORPUS VALIDATION PASSED: {n} entries")


if __name__ == "__main__":
    main()
