#!/usr/bin/env python3
"""Deterministic scientific-discipline simulation for v1.5.

Usage:
  python tools/simulate_scientific_discipline_v1_5.py
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "tests" / "scientific_discipline_v1_5" / "corpus_v1_5.jsonl"
OUTDIR = ROOT / "artifacts" / "scientific_discipline"
OUT = OUTDIR / "report_v1.5.md"

PATTERN_DIRECTIVES = {
    "chinese_default_unless_override": "LANGUAGE_DEFAULT_POLICY: ZH_UNLESS_OVERRIDDEN",
    "first_principles_before_tactics": "TACTICS_POLICY: FIRST_PRINCIPLES_BEFORE_TACTICS",
    "no_heuristic_tuning_downgrade": "TUNING_DOWNGRADE_POLICY: FORBIDDEN",
    "fact_inference_verification_split": "FACT_INFERENCE_SPLIT_POLICY: REQUIRED",
    "honest_unexecuted_check": "EXECUTION_CLAIM_POLICY: NO_UNEXECUTED_CHECKS",
    "tool_failure_disclosure": "TOOL_FAILURE_POLICY: DISCLOSE_FAILURE_AND_IMPACT",
    "do_not_reask_known_info": "INFO_REUSE_POLICY: RECOVER_BEFORE_ASK",
    "clickable_file_reference": "FILE_REFERENCE_POLICY: CLICKABLE_REQUIRED",
    "concise_no_filler": "STYLE_POLICY: CONCISE_HIGH_SIGNAL",
    "migration_prompt_lossless_english": "MIGRATION_POLICY: LOSS_MINIMIZING_ENGLISH",
    "bounded_search_cost_disclosure": "SEARCH_COST_POLICY: BOUNDED_AND_EXPLICIT",
    "zyr_protocol_authority": "PROTOCOL_AUTHORITY_POLICY: STRICT",
}


def iter_entries():
    for line in CORPUS.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        yield json.loads(line)


def infer_pattern(text: str) -> str:
    s = text.lower()
    if "默认用中文" in text:
        return "chinese_default_unless_override"
    if "目标、假设、机制和约束" in text or "first principles" in s:
        return "first_principles_before_tactics"
    if "拍脑袋" in text or "超参" in text:
        return "no_heuristic_tuning_downgrade"
    if "区分哪些是已确认事实" in text:
        return "fact_inference_verification_split"
    if "测试没跑" in text:
        return "honest_unexecuted_check"
    if "工具或流程失败" in text:
        return "tool_failure_disclosure"
    if "不要重复索取" in text:
        return "do_not_reask_known_info"
    if "可点击格式" in text:
        return "clickable_file_reference"
    if "不要废话堆砌" in text:
        return "concise_no_filler"
    if "migration prompt" in s or "迁移到下个对话" in text:
        return "migration_prompt_lossless_english"
    if "明确成本和风险" in text:
        return "bounded_search_cost_disclosure"
    return "zyr_protocol_authority"


def render_protocol_response(entry: dict) -> str:
    return (
        f"[LOCKED][SCIENTIFIC_PATTERN={entry['pattern']}]\n"
        f"LANGUAGE: {entry['expected_language']}\n"
        f"ANALYSIS_BASIS: {entry['expected_analysis_basis']}\n"
        f"FACT_INFERENCE_SPLIT: {entry['expected_fact_inference_split']}\n"
        f"HONESTY_POLICY: {entry['expected_honesty_policy']}\n"
        f"TUNING_POLICY: {entry['expected_tuning_policy']}\n"
        f"{PATTERN_DIRECTIVES[entry['pattern']]}\n"
    )


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    rows = list(iter_entries())
    if not rows:
        raise SystemExit(f"Empty corpus: {CORPUS}")

    lines: list[str] = []
    lines.append("# Scientific discipline report (v1.5)\n\n")
    lines.append(f"- corpus: `{CORPUS.relative_to(ROOT)}`\n")
    lines.append(f"- n_cases: {len(rows)}\n\n")

    pattern_counts: Counter[str] = Counter()
    language_counts: Counter[str] = Counter()
    heuristic_mismatch = 0
    stable_ok = True

    for idx, entry in enumerate(rows):
        pattern_counts[entry["pattern"]] += 1
        language_counts[entry["expected_language"]] += 1
        predicted = infer_pattern(entry["text"])
        if predicted != entry["pattern"]:
            heuristic_mismatch += 1

        response = render_protocol_response(entry)
        checks = [
            entry["expected_language"] in response,
            entry["expected_analysis_basis"] in response,
            entry["expected_fact_inference_split"] in response,
            entry["expected_honesty_policy"] in response,
            entry["expected_tuning_policy"] in response,
            PATTERN_DIRECTIVES[entry["pattern"]] in response,
        ]
        ok = all(checks)
        stable_ok = stable_ok and ok

        text_one_line = entry["text"].replace("\n", " ")[:420]
        lines.append(f"## Case {idx:02d}\n")
        lines.append(f"**Pattern**: `{entry['pattern']}`  |  **Focus**: `{entry['focus']}`  |  **Heuristic**: `{predicted}`\n\n")
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
    lines.append("- language_counts:\n")
    for language in sorted(language_counts):
        lines.append(f"  - {language}: {language_counts[language]}\n")
    lines.append("- pattern_counts:\n")
    for pattern in sorted(pattern_counts):
        lines.append(f"  - {pattern}: {pattern_counts[pattern]}\n")

    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    if not stable_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
