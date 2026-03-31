#!/usr/bin/env python3
"""Strict skill validator (v1.3).

Goals:
- Prevent format drift that causes routing/behavior hallucinations.
- Fail fast on missing or inconsistent schema.

Checks (baseline):
- Every real skill file `skills/**/S###_*.md` has YAML front matter parseable by PyYAML.
- Required fields: id, name, category, triggers, inputs_required, outputs_required, quality_gates.
- id uniqueness.
- id should match filename prefix when applicable (S###_*.md).
- Backtick-referenced local file paths inside markdown must exist (best-effort; ignores generated artifacts like MODE_LOCK.md).

Usage:
  python tools/validate_v1_3.py
  python tools/validate_v1_3.py --loose   # v7_1 compatible
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
BACKTICK_PATH_RE = re.compile(r"`([^`]+?\.(?:md|py|yaml|yml|json|txt|pdf))`")
SKILL_FILENAME_RE = re.compile(r"^S\d+_.*\.md$")
ALLOWED_CATEGORIES = {"research_core", "experiments", "reproducibility", "paper_ops", "composite"}

IGNORE_MISSING_REFS = {
    "MODE_LOCK.md", "MODE_LOCK.json", "evidence.json",
}

EXTERNAL_REF_PREFIXES = (
    "zyr_runtime_skills/",
)

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

def iter_skill_files() -> List[Path]:
    return sorted(p for p in SKILLS_DIR.rglob("*.md") if is_real_skill_file(p))

def resolve_local_ref(md_path: Path, ref: str) -> List[Path]:
    raw = ref.strip()
    rel = Path(raw)
    candidates: List[Path] = []

    if raw.startswith("/"):
        candidates.append(Path(raw))
    elif raw.startswith("./") or raw.startswith("../"):
        candidates.append((md_path.parent / rel).resolve())
    else:
        candidates.append((ROOT / rel).resolve())
        candidates.append((md_path.parent / rel).resolve())

    dedup: List[Path] = []
    seen = set()
    for candidate in candidates:
        key = str(candidate)
        if key not in seen:
            seen.add(key)
            dedup.append(candidate)
    return dedup

def check_backtick_refs(md_path: Path, text: str) -> List[str]:
    errs = []
    for m in BACKTICK_PATH_RE.finditer(text):
        ref = m.group(1).strip()
        if " " in ref:
            continue
        if "/" not in ref and not ref.startswith("."):
            continue
        if "://" in ref:
            continue
        # allow glob patterns like skills/**/S*.md
        if "*" in ref or "?" in ref:
            continue
        if ref.startswith(EXTERNAL_REF_PREFIXES):
            continue
        if any(ref.endswith(x) for x in IGNORE_MISSING_REFS):
            continue
        candidates = resolve_local_ref(md_path, ref)
        if ref.startswith("/") and not any(str(p).startswith(str(ROOT)) for p in candidates):
            continue
        if not any(p.exists() for p in candidates):
            errs.append(f"Missing referenced file `{ref}` in {md_path.relative_to(ROOT)}")
    return errs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--loose", action="store_true", help="compat mode: only require id/name/category + uniqueness")
    args = ap.parse_args()

    errors: List[str] = []
    ids: Dict[str, Path] = {}

    for p in iter_skill_files():
        text = p.read_text(encoding="utf-8", errors="replace")
        fm = parse_front_matter(text)
        if not fm:
            errors.append(f"Missing YAML front matter: {p.relative_to(ROOT)}")
            continue

        for k in ("id", "name", "category"):
            if not fm.get(k):
                errors.append(f"Missing `{k}` in front matter: {p.relative_to(ROOT)}")

        sid = str(fm.get("id", "")).strip()
        if sid:
            if sid in ids:
                errors.append(f"Duplicate id `{sid}`: {p.relative_to(ROOT)} and {ids[sid].relative_to(ROOT)}")
            else:
                ids[sid] = p

        cat = str(fm.get("category", "")).strip()
        if cat and cat not in ALLOWED_CATEGORIES:
            errors.append(f"Unknown category `{cat}` in {p.relative_to(ROOT)}")

        if not args.loose:
            for k in ("triggers", "inputs_required", "outputs_required", "quality_gates"):
                v = fm.get(k)
                if v is None or (isinstance(v, list) and len(v) == 0) or (isinstance(v, str) and not v.strip()):
                    errors.append(f"Missing/empty `{k}` in front matter: {p.relative_to(ROOT)}")
            # filename-id consistency check
            # e.g., skills/.../S201_problem_framing.md should have id S201
            stem = p.stem
            m = re.match(r"^(S\d+)_", stem)
            if m and sid and m.group(1) != sid:
                errors.append(f"ID mismatch: filename {stem} vs id {sid} in {p.relative_to(ROOT)}")

        # best-effort reference check
        errors.extend(check_backtick_refs(p, text))

    if errors:
        print("Validation failed:")
        for e in errors:
            print(f"- {e}")
        raise SystemExit(1)

    print("Validation passed.")

if __name__ == "__main__":
    main()
