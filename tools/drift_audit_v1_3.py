#!/usr/bin/env python3
"""Drift audit (v1.3.2).

Scans markdown files for backtick-referenced local file paths and reports missing targets.

Design note:
- We intentionally exclude historical logs (CHANGELOG / INCREMENTAL_UPDATE*) from strict path checking.
  Those files are allowed to reference removed legacy artifacts.

Usage:
  python tools/drift_audit_v1_3.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKTICK_PATH_RE = re.compile(r"`([^`]+?\.(?:md|py|yaml|yml|json|txt|pdf))`")

IGNORE_SUFFIX = {
    "MODE_LOCK.md", "MODE_LOCK.json", "evidence.json", "repropack/SCAN_REPORT.md",
}
IGNORE_GLOBS = ("*", "?")
IGNORE_MD_FILENAMES = {
    "CHANGELOG.md",
}
IGNORE_SOURCE_PREFIXES = (
    "artifacts/system_audit/",
    "docs/audits/",
    "skills/platform_zyr_skills/rewrites/",
)
EXTERNAL_REF_PREFIXES = (
    "zyr_runtime_skills/",
)


def is_ignored_ref(ref: str) -> bool:
    if " " in ref:
        return True
    if "/" not in ref and not ref.startswith("."):
        return True

    if "://" in ref:
        return True
    if ref.startswith(EXTERNAL_REF_PREFIXES):
        return True
    if any(ch in ref for ch in IGNORE_GLOBS):
        return True
    if any(ref.endswith(s) for s in IGNORE_SUFFIX):
        return True
    return False


def is_ignored_source(md_path: Path) -> bool:
    rel = md_path.relative_to(ROOT).as_posix()
    if any(rel.startswith(prefix) for prefix in IGNORE_SOURCE_PREFIXES):
        return True
    name = md_path.name
    if name in IGNORE_MD_FILENAMES:
        return True
    if name.startswith("INCREMENTAL_UPDATE_"):
        return True
    return False


def resolve_local_ref(md_path: Path, ref: str) -> list[Path]:
    rel = Path(ref)
    candidates = []
    if ref.startswith("/"):
        candidates.append(Path(ref))
    elif ref.startswith("./") or ref.startswith("../"):
        candidates.append((md_path.parent / rel).resolve())
    else:
        candidates.append((ROOT / rel).resolve())
        candidates.append((md_path.parent / rel).resolve())

    dedup = []
    seen = set()
    for candidate in candidates:
        key = str(candidate)
        if key not in seen:
            seen.add(key)
            dedup.append(candidate)
    return dedup


def main():
    missing = []
    for p in sorted(ROOT.rglob("*.md")):
        if is_ignored_source(p):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        for m in BACKTICK_PATH_RE.finditer(text):
            ref = m.group(1).strip()
            if is_ignored_ref(ref):
                continue
            candidates = resolve_local_ref(p, ref)
            if ref.startswith("/") and not any(str(candidate).startswith(str(ROOT)) for candidate in candidates):
                continue
            if not any(candidate.exists() for candidate in candidates):
                missing.append((p.relative_to(ROOT).as_posix(), ref))

    if missing:
        print("DRIFT AUDIT FAILED: missing referenced files")
        for src, ref in missing:
            print(f"- {src}: `{ref}`")
        raise SystemExit(1)

    print("DRIFT AUDIT PASSED: no missing references found")


if __name__ == "__main__":
    main()
