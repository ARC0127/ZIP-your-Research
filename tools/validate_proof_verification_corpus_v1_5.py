#!/usr/bin/env python3
"""Validate proof-verification corpus for v1.5.

Usage:
  python tools/validate_proof_verification_corpus_v1_5.py
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "tests" / "proof_verification_v1_5" / "corpus_v1_5.jsonl"
SCHEMA = ROOT / "tests" / "proof_verification_v1_5" / "corpus_schema_v1_5.json"


def main() -> None:
    if not CORPUS.exists():
        raise SystemExit(f"Missing corpus: {CORPUS}")
    if not SCHEMA.exists():
        raise SystemExit(f"Missing schema: {SCHEMA}")

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    req = schema.get("entry_required_keys", [])
    text_max_chars = int(schema.get("text_max_chars", 20000))
    allowed_patterns = set(schema.get("pattern_allowed", []))
    allowed_families = set(schema.get("theorem_family_allowed", []))
    allowed_lengths = set(schema.get("proof_length_bucket_allowed", []))
    allowed_budgets = set(schema.get("review_budget_allowed", []))
    allowed_chunk_policies = set(schema.get("chunk_policy_allowed", []))
    allowed_anchor_kinds = set(schema.get("expected_anchor_kind_allowed", []))
    allowed_primary_artifacts = set(schema.get("expected_primary_artifact_allowed", []))
    allowed_verdicts = set(schema.get("expected_verdict_allowed", []))
    allowed_fatal = set(schema.get("expected_fatal_policy_allowed", []))
    allowed_majority = set(schema.get("expected_majority_policy_allowed", []))
    allowed_refinement = set(schema.get("expected_refinement_policy_allowed", []))
    allowed_formal = set(schema.get("expected_formal_adapter_policy_allowed", []))
    min_counts = schema.get("required_pattern_min_counts", {}) or {}

    errors: list[str] = []
    seen_ids: set[str] = set()
    pattern_counts: Counter[str] = Counter()
    verdict_counts: Counter[str] = Counter()
    family_counts: Counter[str] = Counter()
    length_counts: Counter[str] = Counter()
    budget_counts: Counter[str] = Counter()
    anchor_counts: Counter[str] = Counter()
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

        theorem_family = str(obj.get("theorem_family", "")).strip()
        if theorem_family not in allowed_families:
            errors.append(f"L{ln}: invalid theorem_family `{theorem_family}`")
        else:
            family_counts[theorem_family] += 1

        proof_length_bucket = str(obj.get("proof_length_bucket", "")).strip()
        if proof_length_bucket not in allowed_lengths:
            errors.append(f"L{ln}: invalid proof_length_bucket `{proof_length_bucket}`")
        else:
            length_counts[proof_length_bucket] += 1

        review_budget = str(obj.get("review_budget", "")).strip()
        if review_budget not in allowed_budgets:
            errors.append(f"L{ln}: invalid review_budget `{review_budget}`")
        else:
            budget_counts[review_budget] += 1

        chunk_policy = str(obj.get("chunk_policy", "")).strip()
        if chunk_policy not in allowed_chunk_policies:
            errors.append(f"L{ln}: invalid chunk_policy `{chunk_policy}`")

        expected_anchor_kind = str(obj.get("expected_anchor_kind", "")).strip()
        if expected_anchor_kind not in allowed_anchor_kinds:
            errors.append(f"L{ln}: invalid expected_anchor_kind `{expected_anchor_kind}`")
        else:
            anchor_counts[expected_anchor_kind] += 1

        expected_primary_artifact = str(obj.get("expected_primary_artifact", "")).strip()
        if expected_primary_artifact not in allowed_primary_artifacts:
            errors.append(f"L{ln}: invalid expected_primary_artifact `{expected_primary_artifact}`")

        verdict = str(obj.get("expected_verdict", "")).strip()
        if verdict not in allowed_verdicts:
            errors.append(f"L{ln}: invalid expected_verdict `{verdict}`")
        else:
            verdict_counts[verdict] += 1

        fatal = str(obj.get("expected_fatal_policy", "")).strip()
        if fatal not in allowed_fatal:
            errors.append(f"L{ln}: invalid expected_fatal_policy `{fatal}`")

        majority = str(obj.get("expected_majority_policy", "")).strip()
        if majority not in allowed_majority:
            errors.append(f"L{ln}: invalid expected_majority_policy `{majority}`")

        refinement = str(obj.get("expected_refinement_policy", "")).strip()
        if refinement not in allowed_refinement:
            errors.append(f"L{ln}: invalid expected_refinement_policy `{refinement}`")

        formal = str(obj.get("expected_formal_adapter_policy", "")).strip()
        if formal not in allowed_formal:
            errors.append(f"L{ln}: invalid expected_formal_adapter_policy `{formal}`")

        text = obj.get("text")
        if not isinstance(text, str) or not text.strip():
            errors.append(f"L{ln}: invalid/empty text")
        elif len(text) > text_max_chars:
            errors.append(f"L{ln}: text too long ({len(text)}>{text_max_chars})")

    for pattern, min_count in sorted(min_counts.items()):
        if pattern_counts.get(pattern, 0) < int(min_count):
            errors.append(f"pattern `{pattern}` count too low ({pattern_counts.get(pattern, 0)}<{int(min_count)})")

    for required in ("verified_false", "verified_true", "verification_incomplete"):
        if verdict_counts.get(required, 0) != 8:
            errors.append(f"verdict `{required}` count must be 8 ({verdict_counts.get(required, 0)}!=8)")

    for family in ("analysis", "algebra", "probability", "combinatorics"):
        if family_counts.get(family, 0) < 4:
            errors.append(f"theorem_family `{family}` coverage too low ({family_counts.get(family, 0)}<4)")

    for bucket in ("short", "medium", "long"):
        if length_counts.get(bucket, 0) < 4:
            errors.append(f"proof_length_bucket `{bucket}` coverage too low ({length_counts.get(bucket, 0)}<4)")

    for budget in ("low", "medium", "high"):
        if budget_counts.get(budget, 0) < 4:
            errors.append(f"review_budget `{budget}` coverage too low ({budget_counts.get(budget, 0)}<4)")

    for anchor in ("line_anchor", "lemma_anchor", "assumption_anchor", "multi_anchor"):
        if anchor_counts.get(anchor, 0) < 1:
            errors.append(f"missing expected_anchor_kind coverage `{anchor}`")

    if errors:
        print("PROOF CORPUS VALIDATION FAILED")
        for err in errors[:200]:
            print(f"- {err}")
        if len(errors) > 200:
            print(f"... and {len(errors) - 200} more")
        raise SystemExit(1)

    print(f"PROOF CORPUS VALIDATION PASSED: {n} entries")


if __name__ == "__main__":
    main()
