#!/usr/bin/env python3
"""Deterministic skill router (v1.3.2, weighted).

Goal: Given a user query, recommend top-K skills (copy/paste ready), with a bias toward:
- 思路/逻辑核查
- 方法正确性核查
- 计算正确性核查
- 论文整体思路核查
- 证明思路核查
- 创新性审查 & 创新点搜索
- 实验完整性检查
- 论文解读
- 句子改写/润色（含检索提示）

Design:
- Read YAML front matter from skills/**/S*.md
- Base score: trigger matches (substring, case-insensitive) + small token overlap bonus
- Apply category weights + task-pattern boosts from router/weights_v1.3.2.yaml
- Treat composite `writing_engine` as a first-class candidate (for rewriting / manuscript-like input)
- Output is stable and audit-friendly.

Usage:
  python router/route.py "我想做方法正确性核查" --topk 5
"""

import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import yaml
except Exception:
    raise SystemExit("PyYAML required. Install: pip install pyyaml")

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
WEIGHTS_FILE = ROOT / "router" / "weights_v1.3.2.yaml"

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)

SECTION_HINTS = [
    "abstract", "introduction", "method", "results", "discussion", "conclusion",
    "related work", "\\section", "appendix", "theorem", "lemma", "proof",
]

# writing intent hints (EN + ZH)
WRITING_HINTS = [
    "rewrite", "revise", "polish", "edit", "review", "camera-ready", "rebuttal",
    "润色", "改写", "重写", "审稿", "降重", "表达", "措辞",
    "icml", "neurips", "iclr", "cvpr", "aaai",
]


# coding/debug intent hints (EN + ZH)
CODING_HINTS = [
    "bug", "fix", "debug", "traceback", "exception", "crash", "regression", "refactor",
    "unit test", "pytest", "mypy", "lint", "ci",
    "报错", "修复", "调试", "回归", "重构", "代码审计", "单测", "编译",
]

def parse_front_matter(text: str) -> Dict:
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return {}
    return yaml.safe_load(m.group(1)) or {}

def iter_skills() -> List[Dict]:
    skills = []
    for p in sorted(SKILLS_DIR.glob("**/S*.md")):
        text = p.read_text(encoding="utf-8")
        fm = parse_front_matter(text)
        if not fm:
            continue
        triggers = fm.get("triggers", []) or []
        if isinstance(triggers, str):
            triggers = [triggers]
        skills.append({
            "id": str(fm.get("id", "")).strip(),
            "name": str(fm.get("name", "")).strip(),
            "category": str(fm.get("category", "")).strip(),
            "triggers": [str(t).strip().lower() for t in triggers if str(t).strip()],
            "path": str(p.relative_to(ROOT).as_posix()),
        })
    return skills

def looks_like_manuscript(q: str) -> bool:
    ql = q.lower()
    if len(q) > 1200:
        return True
    if any(h in ql for h in SECTION_HINTS):
        return True
    if q.count("\n") > 15:
        return True
    return False

def load_weights() -> Dict:
    if WEIGHTS_FILE.exists():
        return yaml.safe_load(WEIGHTS_FILE.read_text(encoding="utf-8")) or {}
    return {}

def tokenize(s: str) -> List[str]:
    # lightweight tokenization: split on non-alphanum, keep chinese as whole chunks
    s = s.lower()
    parts = re.split(r"[^a-z0-9\u4e00-\u9fff]+", s)
    return [p for p in parts if p and len(p) >= 2]

def base_score(query_l: str, triggers: List[str]) -> Tuple[float, List[str]]:
    # stable scoring: trigger substring hits + small token overlap bonus
    score = 0.0
    hits = []
    q_tokens = set(tokenize(query_l))
    for t in triggers:
        if not t:
            continue
        tl = t.lower()
        if tl in query_l:
            score += 1.0 + min(0.6, len(tl) / 60.0)
            hits.append(tl)
        else:
            # token overlap: if all tokens in trigger appear in query, add a small bonus
            t_tokens = [x for x in tokenize(tl) if x not in {"the","and","for","with"}]
            if t_tokens and all(x in q_tokens for x in t_tokens):
                score += 0.25 + min(0.25, len(t_tokens) / 10.0)
    return score, hits

def apply_weights(query_l: str, skill: Dict, sc: float, weights: Dict) -> Tuple[float, List[str]]:
    applied = []
    cat_w = (weights.get("category_weights", {}) or {}).get(skill.get("category",""), 1.0)
    sc *= float(cat_w)
    if cat_w != 1.0:
        applied.append(f"cat*{cat_w:.2f}")

    # task-pattern boosts
    for tp in (weights.get("task_patterns", []) or []):
        patterns = [str(x).lower() for x in (tp.get("patterns", []) or [])]
        if any(p in query_l for p in patterns):
            bskills = tp.get("boost_skills", {}) or {}
            bcat = tp.get("boost_categories", {}) or {}
            if skill["id"] in bskills:
                sc += float(bskills[skill["id"]])
                applied.append(f"{tp.get('name','task')}:skill+{float(bskills[skill['id']]):.1f}")
            if skill.get("category","") in bcat:
                sc *= (1.0 + float(bcat[skill.get('category','')]))
                applied.append(f"{tp.get('name','task')}:cat*{1.0+float(bcat[skill.get('category','')]):.2f}")
    return sc, applied

def secondary_recos(primary_id: str, weights: Dict) -> List[str]:
    out = []
    for rule in (weights.get("secondary_suggestions", []) or []):
        if primary_id in (rule.get("if_primary_in", []) or []):
            out.extend([str(x) for x in (rule.get("suggest", []) or [])])
    # de-dup, stable
    seen = set()
    dedup = []
    for x in out:
        if x not in seen:
            seen.add(x)
            dedup.append(x)
    return dedup

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", help="user query text")
    ap.add_argument("--topk", type=int, default=5)
    args = ap.parse_args()

    q = args.query.strip()
    ql = q.lower()
    weights = load_weights()

    skills = iter_skills()

    # Add composite writing_engine as a candidate for scoring
    skills.append({
        "id": "writing_engine",
        "name": "writing_engine",
        "category": "composite",
        "triggers": [x.lower() for x in WRITING_HINTS],
        "path": "skills/writing_engine/MASTER_v1.3.2.md",
    })

    # v1.2+: Add composite coding_engine as a candidate for scoring
    skills.append({
        "id": "coding_engine",
        "name": "coding_engine",
        "category": "composite",
        "triggers": [x.lower() for x in CODING_HINTS],
        "path": "skills/coding_engine/MASTER_v1.3.2.md",
    })


    # Manuscript heuristic: print a strong hint, but still compute scores
    manuscript_flag = looks_like_manuscript(q)

    scored = []
    for s in skills:
        sc0, hits = base_score(ql, s["triggers"])
        if sc0 <= 0 and not (s["id"] == "writing_engine" and manuscript_flag):
            continue
        sc, applied = apply_weights(ql, s, sc0 if sc0>0 else 0.5, weights)  # give manuscript a seed score
        scored.append((sc, s, hits, applied))

    scored.sort(key=lambda x: (-x[0], x[1]["id"]))

    if manuscript_flag:
        print("Heuristic: manuscript-like input detected → consider PRIMARY writing_engine.")
        print("Next: skills/writing_engine/MASTER_v1.3.2.md")
        print()

    if not scored:
        print("No trigger matches. Suggested starting points:")
        print("- S226 logic_consistency_audit (if you want reasoning/logic checks)")
        print("- S227 method_correctness_audit (if you want method correctness checks)")
        print("- S326 calculation_correctness_check (if you want computation/unit checks)")
        print("- S231 innovation_point_search_plan (if you want novelty search)")
        print("- S232 paper_interpretation_deep_read (if you want paper interpretation)")
        print("- writing_engine (if you want rewriting/polishing)")
        return 0

    topk = min(args.topk, len(scored))
    primary = scored[0][1]["id"]

    print(f"PRIMARY: {primary}")
    sec = secondary_recos(primary, weights)
    if sec:
        print("SECONDARY (verification/companion): " + ", ".join(sec))
    print()

    print(f"Top {topk} matches:")
    for i, (sc, s, hits, applied) in enumerate(scored[:topk], 1):
        print(f"{i}. {s['id']} | {s['name']} | {s['category']} | score={sc:.2f}")
        if hits:
            print(f"   hits: {', '.join(hits[:6])}{'...' if len(hits) > 6 else ''}")
        if applied:
            print(f"   weights: {', '.join(applied[:6])}{'...' if len(applied) > 6 else ''}")
        print(f"   file: {s['path']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
