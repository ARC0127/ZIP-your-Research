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
- Read YAML front matter from real skill files `skills/**/S###_*.md`
- Base score: trigger matches (substring, case-insensitive) + small token overlap bonus
- Apply category weights + task-pattern boosts from router/weights_v1.3.2.yaml
- Treat composite `writing_engine` and `figure_engine` as first-class candidates
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
SKILL_FILENAME_RE = re.compile(r"^S\d+_.*\.md$")

SECTION_HINTS = [
    "abstract", "introduction", "method", "results", "discussion", "conclusion",
    "related work", "\\section", "appendix", "theorem", "lemma", "proof",
]

# writing intent hints (EN + ZH)
WRITING_HINTS = [
    "rewrite", "revise", "polish", "edit", "review", "camera-ready", "rebuttal",
    "write", "writing", "manuscript", "paper section", "readme prose", "abstract", "introduction", "method", "results",
    "润色", "改写", "重写", "审稿", "降重", "表达", "措辞", "写作", "写东西", "摘要", "引言", "方法节", "实验节", "研究计划",
    "icml", "neurips", "iclr", "cvpr", "aaai",
]

FIGURE_HINTS = [
    "figure", "plot", "diagram", "workflow diagram", "architecture diagram",
    "scientific figure", "matplotlib", "chart", "graph", "visualization",
    "画图", "绘图", "图", "流程图", "架构图", "科研绘图", "绘图脚本",
    "svg", "png", "pdf", "figures4papers",
]

RWF_S340_HINTS = [
    "paper writing", "manuscript", "research plan", "readme architecture", "caption",
    "anti ai tone", "forbidden phrase", "mechanical phrasing", "style logic",
    "figure design", "architecture diagram", "workflow diagram", "figures4papers",
    "source-native diagram", "svg", "png", "matplotlib", "writing engine", "figure engine",
    "论文润色", "论文重构", "研究计划", "禁用短语", "禁止词", "机械排比",
    "架构图", "流程图", "科研绘图", "物理边框", "图文一致", "完整性验证", "禁止遗漏",
]


# coding/debug intent hints (EN + ZH)
CODING_HINTS = [
    "bug", "fix", "debug", "traceback", "exception", "crash", "regression", "refactor",
    "unit test", "pytest", "mypy", "lint", "ci",
    "报错", "修复", "调试", "回归", "重构", "代码审计", "单测", "编译",
]

# proof / derivation intent hints (EN + ZH)
PROOF_HINTS = [
    "proof", "theorem", "lemma", "corollary", "derivation", "rigor",
    "pessimistic verification", "progressive verification", "vertical review",
    "first-error-wins", "formal proof", "autoformalization", "lean",
    "证明", "定理", "引理", "推导", "证明验证", "证明审计", "数学证明",
    "理论推导", "形式化证明", "形式化", "proof audit", "derivation audit",
]

def parse_front_matter(text: str) -> Dict:
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return {}
    return yaml.safe_load(m.group(1)) or {}

def is_real_skill_file(path: Path) -> bool:
    rel = path.relative_to(SKILLS_DIR).as_posix()
    if "platform_zyr_skills/rewrites/" in rel:
        return False
    return bool(SKILL_FILENAME_RE.match(path.name))

def iter_skills() -> List[Dict]:
    skills = []
    for p in sorted(path for path in SKILLS_DIR.rglob("*.md") if is_real_skill_file(path)):
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


def looks_like_writing_task(q: str) -> bool:
    ql = q.lower()
    if any(h in ql for h in WRITING_HINTS):
        return True
    if looks_like_manuscript(q):
        return True
    return False

def looks_like_proof_task(q: str) -> bool:
    ql = q.lower()
    if any(h in ql for h in PROOF_HINTS):
        return True
    if any(sym in q for sym in ("∀", "∃", "⇒", "⇔", "∵", "∴")):
        return True
    return False

def looks_like_figure_task(q: str) -> bool:
    ql = q.lower()
    if any(h in ql for h in FIGURE_HINTS):
        return True
    return False

def looks_like_rwf_s340_task(q: str) -> bool:
    ql = q.lower()
    if any(h in ql for h in RWF_S340_HINTS):
        return True
    if looks_like_manuscript(q):
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

    # v1.6.3+: Add composite figure_engine as a candidate for scoring
    skills.append({
        "id": "figure_engine",
        "name": "figure_engine",
        "category": "composite",
        "triggers": [x.lower() for x in FIGURE_HINTS],
        "path": "skills/figure_engine/MASTER_v1.6.3.md",
    })

    # v1.2+: Add composite coding_engine as a candidate for scoring
    skills.append({
        "id": "coding_engine",
        "name": "coding_engine",
        "category": "composite",
        "triggers": [x.lower() for x in CODING_HINTS],
        "path": "skills/coding_engine/MASTER_v1.3.2.md",
    })

    # v1.5+: Add composite proof_engine as a candidate for scoring
    skills.append({
        "id": "proof_engine",
        "name": "proof_engine",
        "category": "composite",
        "triggers": [x.lower() for x in PROOF_HINTS],
        "path": "skills/proof_engine/MASTER_v1.5.md",
    })

    # v1.6+: Add integrated research-writing/figure/S340 master as a candidate.
    skills.append({
        "id": "rwf_s340_master",
        "name": "research_writing_figure_s340_integrated_master",
        "category": "composite",
        "triggers": [x.lower() for x in RWF_S340_HINTS],
        "path": "skills/rwf_s340/MASTER.md",
    })


    # Manuscript heuristic: print a strong hint, but still compute scores
    manuscript_flag = looks_like_manuscript(q)
    writing_flag = looks_like_writing_task(q)
    proof_flag = looks_like_proof_task(q)
    figure_flag = looks_like_figure_task(q)
    rwf_s340_flag = looks_like_rwf_s340_task(q)

    scored = []
    for s in skills:
        sc0, hits = base_score(ql, s["triggers"])
        if sc0 <= 0 and not (
            (s["id"] == "writing_engine" and writing_flag)
            or (s["id"] == "proof_engine" and proof_flag)
            or (s["id"] in {"rwf_s340_master", "S640"} and rwf_s340_flag)
        ):
            continue
        sc, applied = apply_weights(ql, s, sc0 if sc0 > 0 else 0.5, weights)  # heuristic seed score
        scored.append((sc, s, hits, applied))

    scored.sort(key=lambda x: (-x[0], x[1]["id"]))

    if writing_flag:
        print("Hard requirement: writing task detected → call writing_engine backed by Research-Paper-Writing-Skills.")
        print("Next: skills/writing_engine/MASTER_v1.3.2.md and ext/src/rpws/")
        print()
    if proof_flag:
        print("Heuristic: proof-heavy input detected → consider PRIMARY proof_engine.")
        print("Next: skills/proof_engine/MASTER_v1.5.md")
        print()
    if figure_flag:
        print("Hard requirement: figure task detected → call figure_engine backed by figures4papers.")
        print("Next: inspect ext/src/figures/ first, then use skills/figure_engine/MASTER_v1.6.3.md")
        print()
    if rwf_s340_flag:
        print("Hard requirement: RWF-S340 task detected → apply S640 as global writing/logic gate when prose is involved.")
        print("Next: skills/rwf_s340/MASTER.md and skills/rwf_s340/S640_s340_global_paper_logic_language_audit.md")
        print()

    if not scored:
        print("No trigger matches. Suggested starting points:")
        print("- S226 logic_consistency_audit (if you want reasoning/logic checks)")
        print("- S227 method_correctness_audit (if you want method correctness checks)")
        print("- S326 calculation_correctness_check (if you want computation/unit checks)")
        print("- S231 innovation_point_search_plan (if you want novelty search)")
        print("- S232 paper_interpretation_deep_read (if you want paper interpretation)")
        print("- writing_engine (if you want rewriting/polishing)")
        print("- proof_engine (if you want theorem/proof/derivation verification)")
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
