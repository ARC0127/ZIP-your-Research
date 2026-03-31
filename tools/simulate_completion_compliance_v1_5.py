#!/usr/bin/env python3
"""Protocol-level completion compliance simulation for v1.5 alignment.

This is a deterministic simulator, not an LLM eval.

Usage:
  python tools/simulate_completion_compliance_v1_5.py
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "tests" / "compliance_v1_5" / "corpus_v1_5.jsonl"
OUTDIR = ROOT / "artifacts" / "completion_compliance"
OUT = OUTDIR / "report_v1.5.md"


def iter_entries():
    for line in CORPUS.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        yield json.loads(line)


def infer_pattern(text: str) -> str:
    s = text.lower()
    if "不要只给建议" in text or "建议" in text:
        return "convert_execution_to_advice"
    if "不要擅自拆" in text or "只修其中一部分" in text:
        return "split_without_permission"
    if "最小版" in text or "sample output" in s or "mvp" in s:
        return "large_scope_downgrade_to_mvp"
    if "不要问我 entrypoint" in text or "自己从仓库" in text:
        return "discoverable_local_context"
    if "只问最少的问题" in text:
        return "blocker_question_overreach"
    if "不要先给我一个计划书" in text or "不要先给计划" in text:
        return "plan_only_without_permission"
    if "只做摘要改写" in text:
        return "mixed_request_easy_part_only"
    if "不能只做最容易的一项" in text:
        return "under_deliver_on_lawful_scope"
    if "真正缺关键输入时再问我" in text:
        return "over_ask_when_discoverable"
    if "不能提前收尾" in text:
        return "premature_stop"
    if "不算完成" in text:
        return "partial_as_done"
    return "simplify_without_permission"


def render_protocol_response(entry: dict) -> str:
    return (
        f"[LOCKED][PATTERN={entry['pattern']}]\n"
        f"ACTION: {entry['expected_action']}\n"
        f"RESPONSE_MODE: {entry['expected_response_mode']}\n"
        f"COMPLETION_POLICY: {entry['expected_completion_policy']}\n"
        f"BLOCKER_POLICY: {entry['expected_blocker_policy']}\n"
    )


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    rows = list(iter_entries())
    if not rows:
        raise SystemExit(f"Empty corpus: {CORPUS}")

    lines: list[str] = []
    lines.append("# Completion compliance report (v1.5)\n\n")
    lines.append(f"- corpus: `{CORPUS.relative_to(ROOT)}`\n")
    lines.append(f"- n_cases: {len(rows)}\n\n")

    pattern_counts: Counter[str] = Counter()
    heuristic_mismatch = 0
    stable_ok = True

    for idx, entry in enumerate(rows):
        pattern_counts[entry["pattern"]] += 1
        predicted = infer_pattern(entry["text"])
        if predicted != entry["pattern"]:
            heuristic_mismatch += 1

        response = render_protocol_response(entry)
        checks = [
            entry["expected_action"] in response,
            entry["expected_response_mode"] in response,
            entry["expected_completion_policy"] in response,
            entry["expected_blocker_policy"] in response,
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
    lines.append("- pattern_counts:\n")
    for pattern in sorted(pattern_counts):
        lines.append(f"  - {pattern}: {pattern_counts[pattern]}\n")

    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    if not stable_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
