#!/usr/bin/env python3
"""Validate scientific-discipline corpus for v1.5.

Usage:
  python tools/validate_scientific_discipline_corpus_v1_5.py
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "tests" / "scientific_discipline_v1_5" / "corpus_v1_5.jsonl"
SCHEMA = ROOT / "tests" / "scientific_discipline_v1_5" / "corpus_schema_v1_5.json"


def main() -> None:
    if not CORPUS.exists():
        raise SystemExit(f"Missing corpus: {CORPUS}")
    if not SCHEMA.exists():
        raise SystemExit(f"Missing schema: {SCHEMA}")

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    req = schema.get("entry_required_keys", [])
    text_max_chars = int(schema.get("text_max_chars", 20000))
    allowed_patterns = set(schema.get("pattern_allowed", []))
    allowed_lang = set(schema.get("expected_language_allowed", []))
    allowed_basis = set(schema.get("expected_analysis_basis_allowed", []))
    allowed_split = set(schema.get("expected_fact_inference_split_allowed", []))
    allowed_honesty = set(schema.get("expected_honesty_policy_allowed", []))
    allowed_tuning = set(schema.get("expected_tuning_policy_allowed", []))
    min_counts = schema.get("required_pattern_min_counts", {}) or {}

    errors: list[str] = []
    seen_ids: set[str] = set()
    pattern_counts: Counter[str] = Counter()
    lang_counts: Counter[str] = Counter()
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

        language = str(obj.get("expected_language", "")).strip()
        if language not in allowed_lang:
            errors.append(f"L{ln}: invalid expected_language `{language}`")
        else:
            lang_counts[language] += 1

        basis = str(obj.get("expected_analysis_basis", "")).strip()
        if basis not in allowed_basis:
            errors.append(f"L{ln}: invalid expected_analysis_basis `{basis}`")

        split = str(obj.get("expected_fact_inference_split", "")).strip()
        if split not in allowed_split:
            errors.append(f"L{ln}: invalid expected_fact_inference_split `{split}`")

        honesty = str(obj.get("expected_honesty_policy", "")).strip()
        if honesty not in allowed_honesty:
            errors.append(f"L{ln}: invalid expected_honesty_policy `{honesty}`")

        tuning = str(obj.get("expected_tuning_policy", "")).strip()
        if tuning not in allowed_tuning:
            errors.append(f"L{ln}: invalid expected_tuning_policy `{tuning}`")

        text = obj.get("text")
        if not isinstance(text, str) or not text.strip():
            errors.append(f"L{ln}: invalid/empty text")
        elif len(text) > text_max_chars:
            errors.append(f"L{ln}: text too long ({len(text)}>{text_max_chars})")

    for pattern, min_count in sorted(min_counts.items()):
        if pattern_counts.get(pattern, 0) < int(min_count):
            errors.append(f"pattern `{pattern}` count too low ({pattern_counts.get(pattern, 0)}<{int(min_count)})")

    if lang_counts.get("zh", 0) < 1 or lang_counts.get("en", 0) < 1:
        errors.append("language coverage insufficient (need at least one zh and one en case)")

    if errors:
        print("SCIENTIFIC DISCIPLINE CORPUS VALIDATION FAILED")
        for err in errors[:200]:
            print(f"- {err}")
        if len(errors) > 200:
            print(f"... and {len(errors) - 200} more")
        raise SystemExit(1)

    print(f"SCIENTIFIC DISCIPLINE CORPUS VALIDATION PASSED: {n} entries")


if __name__ == "__main__":
    main()
