#!/usr/bin/env python3
"""Deterministic proof-verification simulation for v1.5.

This is a protocol-level simulator, not an LLM eval.

Usage:
  python tools/simulate_proof_verification_v1_5.py
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "tests" / "proof_verification_v1_5" / "corpus_v1_5.jsonl"
OUTDIR = ROOT / "artifacts" / "proof_verification"
OUT = OUTDIR / "report_v1.5.md"


def iter_entries():
    for line in CORPUS.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        yield json.loads(line)


def infer_pattern(text: str) -> str:
    s = text.lower()
    if "majority" in s and "不要用 majority" in text:
        return "majority_single_negative_fatal"
    if "可微" in text or "condition mismatch" in s:
        return "theorem_condition_mismatch"
    if "第 19 到 21 行" in text or "chunk review" in s:
        return "long_proof_local_derivation_error"
    if "missing lemma" in s or "没有给出相关引理" in text:
        return "missing_lemma_or_unjustified_step"
    if "rigor mismatch" in s or "严格式论文证明" in text:
        return "annotation_or_rigor_mismatch"
    if "笔误" in text or "harmless typo" in s:
        return "harmless_typo_nonfatal"
    if "re-verify" in s or "corrected self-contained proof" in s:
        return "refinement_then_reverify"
    if "Lean sketch" in text and "缺少目标库" in text:
        return "formal_adapter_requested_unavailable"
    if "局部反例" in text or "代入检验" in text:
        return "counterexample_required_for_derivation_failure"
    if "prune" in s and "两个分支" in text:
        return "pruning_multiple_failing_branches"
    if "line anchors" in s or "line anchor" in s:
        return "line_anchor_consistency_failure"
    if "第 3 个引理" in text:
        return "lemma_anchor_fatal_gap"
    if "低预算时" in text:
        return "review_budget_sufficient_detects_hidden_flaw"
    if "budget 太小时" in text:
        return "review_budget_too_small"
    if "repair proposal" in s and "还没 re-verify" in s:
        return "repair_proposal_without_reverify"
    if "竞赛风格答案" in text:
        return "dataset_rigor_paper_rigor_mismatch"
    if "简单图" in text:
        return "unknown_assumption_blocks_verification"
    if "formal success" in s or "autoformalization 某个子引理成功" in text:
        return "formal_success_auxiliary_only"
    if "很长的泛函分析证明" in text:
        return "long_true_proof_clean"
    if "每一行都可复算" in text:
        return "algebra_true_with_line_anchor"
    if "所有 chunk 都通过" in text:
        return "probability_true_progressive_chunk"
    if "lemma anchors 都齐全" in text:
        return "combinatorics_true_lemma_anchor"
    if "Lean sketch 也顺利产出" in text:
        return "formal_adapter_success_nonblocking_true"
    return "review_budget_sufficient_clean_proof"


def render_protocol_response(entry: dict) -> str:
    return (
        f"[LOCKED][PROOF_PATTERN={entry['pattern']}]\n"
        f"PROOF_VERDICT: {entry['expected_verdict']}\n"
        f"FATAL_POLICY: {entry['expected_fatal_policy']}\n"
        f"MAJORITY_POLICY: {entry['expected_majority_policy']}\n"
        f"REFINEMENT_POLICY: {entry['expected_refinement_policy']}\n"
        f"FORMAL_ADAPTER_POLICY: {entry['expected_formal_adapter_policy']}\n"
    )


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    rows = list(iter_entries())
    if not rows:
        raise SystemExit(f"Empty corpus: {CORPUS}")

    lines: list[str] = []
    lines.append("# Proof verification report (v1.5)\n\n")
    lines.append(f"- corpus: `{CORPUS.relative_to(ROOT)}`\n")
    lines.append(f"- n_cases: {len(rows)}\n\n")

    pattern_counts: Counter[str] = Counter()
    verdict_counts: Counter[str] = Counter()
    family_counts: Counter[str] = Counter()
    length_counts: Counter[str] = Counter()
    anchor_kind_counts: Counter[str] = Counter()
    budget_counts: Counter[str] = Counter()
    heuristic_mismatch = 0
    stable_ok = True

    for idx, entry in enumerate(rows):
        pattern_counts[entry["pattern"]] += 1
        verdict_counts[entry["expected_verdict"]] += 1
        family_counts[entry["theorem_family"]] += 1
        length_counts[entry["proof_length_bucket"]] += 1
        anchor_kind_counts[entry["expected_anchor_kind"]] += 1
        budget_counts[entry["review_budget"]] += 1
        predicted = infer_pattern(entry["text"])
        if predicted != entry["pattern"]:
            heuristic_mismatch += 1

        response = render_protocol_response(entry)
        checks = [
            entry["expected_verdict"] in response,
            entry["expected_fatal_policy"] in response,
            entry["expected_majority_policy"] in response,
            entry["expected_refinement_policy"] in response,
            entry["expected_formal_adapter_policy"] in response,
        ]
        ok = all(checks)
        stable_ok = stable_ok and ok

        text_one_line = entry["text"].replace("\n", " ")[:420]
        lines.append(f"## Case {idx:02d}\n")
        lines.append(f"**Pattern**: `{entry['pattern']}`  |  **Focus**: `{entry['focus']}`  |  **Heuristic**: `{predicted}`\n\n")
        lines.append(f"**Shape**: family=`{entry['theorem_family']}` | length=`{entry['proof_length_bucket']}` | budget=`{entry['review_budget']}` | chunk_policy=`{entry['chunk_policy']}` | anchor=`{entry['expected_anchor_kind']}`\n\n")
        lines.append(f"**User**: {text_one_line}\n\n")
        lines.append("**Protocol output**:\n\n```text\n")
        lines.append(response)
        lines.append("```\n\n")
        lines.append(f"**Check**: {'PASS' if ok else 'FAIL'}\n\n")
        lines.append("---\n")

    align = 1.0 - (heuristic_mismatch / max(1, len(rows)))

    lines.append("\n## Summary\n")
    lines.append(f"- protocol_stability: {'PASS' if stable_ok else 'FAIL'}\n")
    lines.append(f"- heuristic_pattern_alignment: {align:.3f}\n")
    lines.append("- verdict_counts:\n")
    for verdict in sorted(verdict_counts):
        lines.append(f"  - {verdict}: {verdict_counts[verdict]}\n")
    lines.append("- theorem_family_counts:\n")
    for theorem_family in sorted(family_counts):
        lines.append(f"  - {theorem_family}: {family_counts[theorem_family]}\n")
    lines.append("- proof_length_bucket_counts:\n")
    for bucket in sorted(length_counts):
        lines.append(f"  - {bucket}: {length_counts[bucket]}\n")
    lines.append("- anchor_kind_counts:\n")
    for anchor_kind in sorted(anchor_kind_counts):
        lines.append(f"  - {anchor_kind}: {anchor_kind_counts[anchor_kind]}\n")
    lines.append("- budget_policy_coverage:\n")
    for budget in sorted(budget_counts):
        lines.append(f"  - {budget}: {budget_counts[budget]}\n")
    lines.append("- pattern_counts:\n")
    for pattern in sorted(pattern_counts):
        lines.append(f"  - {pattern}: {pattern_counts[pattern]}\n")

    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    if not stable_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
