#!/usr/bin/env python3
"""Strict skill validator (v1.3).

Goals:
- Prevent format drift that causes routing/behavior hallucinations.
- Fail fast on missing or inconsistent schema.

Checks (baseline):
- Every active canonical skill in `skills_manifest.yaml` has valid YAML front matter.
- Historical aliases are non-routable and match `manifests/legacy_nonroutable.yaml`.
- Required fields: id, name, category, triggers, inputs_required, outputs_required, quality_gates.
- Active id/path uniqueness and manifest/front-matter agreement.
- id should match filename prefix when applicable (S###_*.md).
- Backtick-referenced local file paths inside markdown must exist (best-effort; ignores generated artifacts like MODE_LOCK.md).

Usage:
  python tools/validate_v1_3.py
  python tools/validate_v1_3.py --loose   # v7_1 compatible
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Dict, List, Sequence, Tuple

import yaml

sys.dont_write_bytecode = True

from zyr_lib.manifest import (
    RepositoryContractError,
    validate_repository_contract,
)

ROOT = Path(__file__).resolve().parents[1]
RELEASE_CAPABILITIES_PATH = ROOT / "manifests" / "RELEASE_CAPABILITIES.yaml"

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
BACKTICK_PATH_RE = re.compile(r"`([^`]+?\.(?:md|py|yaml|yml|json|txt|pdf))`")
ALLOWED_CATEGORIES = {
    "research_core", "experiments", "reproducibility", "paper_ops", "composite",
    "research_writing_integrated", "figure_design_integrated", "s340_integrated",
    "reproducibility_integrated",
}

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

def load_release_capabilities(
    active_ids: Sequence[str],
) -> Tuple[List[Dict[str, Any]], List[str]]:
    """Load tightly scoped declarations for sources omitted from safe releases."""

    errors: List[str] = []
    try:
        raw = yaml.safe_load(RELEASE_CAPABILITIES_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [], [
            "Missing release capability manifest: "
            f"{RELEASE_CAPABILITIES_PATH.relative_to(ROOT)}"
        ]
    except yaml.YAMLError as exc:
        return [], [f"Invalid release capability manifest YAML: {exc}"]
    if not isinstance(raw, dict) or raw.get("schema_version") != 1:
        return [], ["Release capability manifest requires schema_version: 1"]
    records = raw.get("capabilities")
    if not isinstance(records, list) or not records:
        return [], ["Release capability manifest requires a non-empty capabilities list"]

    allowed_statuses = {"AVAILABLE", "SOURCE_UNAVAILABLE"}
    allowed_missing_behaviors = {
        "FAIL_CLOSED",
        "SOURCE_UNAVAILABLE",
        "DEGRADED_SOURCE_TRACEABILITY",
    }
    active_set = set(active_ids)
    seen_ids = set()
    valid_records: List[Dict[str, Any]] = []
    for index, record in enumerate(records):
        label = f"release capability #{index + 1}"
        if not isinstance(record, dict):
            errors.append(f"{label} must be a mapping")
            continue
        capability_id = str(record.get("id", "")).strip()
        if not capability_id:
            errors.append(f"{label} requires id")
            continue
        if capability_id in seen_ids:
            errors.append(f"Duplicate release capability id: {capability_id}")
            continue
        seen_ids.add(capability_id)

        status = str(record.get("status", "")).strip()
        behavior = str(record.get("missing_behavior", "")).strip()
        if status not in allowed_statuses:
            errors.append(f"{capability_id}: unsupported status {status!r}")
        if behavior not in allowed_missing_behaviors:
            errors.append(f"{capability_id}: unsupported missing_behavior {behavior!r}")

        affected = record.get("affected_skill_ids")
        if not isinstance(affected, list):
            errors.append(f"{capability_id}: affected_skill_ids must be a list")
            affected = []
        normalized_affected = [str(value).strip() for value in affected if str(value).strip()]
        unknown_ids = sorted(set(normalized_affected) - active_set)
        if unknown_ids:
            errors.append(
                f"{capability_id}: affected_skill_ids are not active: {unknown_ids}"
            )

        prefixes = record.get("allowed_missing_ref_prefixes")
        if not isinstance(prefixes, list):
            errors.append(
                f"{capability_id}: allowed_missing_ref_prefixes must be a list"
            )
            prefixes = []
        normalized_prefixes: List[str] = []
        for value in prefixes:
            prefix = str(value).strip().replace("\\", "/")
            posix = PurePosixPath(prefix)
            if (
                not prefix.endswith("/")
                or posix.is_absolute()
                or ".." in posix.parts
                or not prefix.startswith("ext/src/")
            ):
                errors.append(
                    f"{capability_id}: unsafe allowed missing reference prefix {prefix!r}"
                )
                continue
            normalized_prefixes.append(prefix)

        bundled_path = record.get("bundled_path")
        if status == "AVAILABLE":
            if not isinstance(bundled_path, str) or not bundled_path.strip():
                errors.append(f"{capability_id}: AVAILABLE requires bundled_path")
            else:
                candidate = (ROOT / bundled_path).resolve()
                try:
                    candidate.relative_to(ROOT.resolve())
                except ValueError:
                    errors.append(f"{capability_id}: bundled_path escapes repository")
                else:
                    if not candidate.exists():
                        errors.append(
                            f"{capability_id}: declared bundled_path is missing: {bundled_path}"
                        )
            if normalized_prefixes:
                errors.append(
                    f"{capability_id}: AVAILABLE cannot allow missing references"
                )
        else:
            if bundled_path not in (None, ""):
                errors.append(
                    f"{capability_id}: SOURCE_UNAVAILABLE must not declare bundled_path"
                )
            if normalized_prefixes and not normalized_affected:
                # A declaration that cannot name a canonical consumer must not
                # weaken canonical reference validation.
                normalized_prefixes = []

        normalized = dict(record)
        normalized["affected_skill_ids"] = normalized_affected
        normalized["allowed_missing_ref_prefixes"] = normalized_prefixes
        valid_records.append(normalized)
    return valid_records, errors


def _declared_missing_reference(
    ref: str,
    skill_id: str,
    capabilities: Sequence[Dict[str, Any]],
) -> bool:
    """Return true only for an unavailable source declared for this skill."""

    for record in capabilities:
        if record.get("status") != "SOURCE_UNAVAILABLE":
            continue
        if skill_id not in record.get("affected_skill_ids", []):
            continue
        if any(
            ref.startswith(prefix)
            for prefix in record.get("allowed_missing_ref_prefixes", [])
        ):
            return True
    return False


def check_backtick_refs(
    md_path: Path,
    text: str,
    *,
    skill_id: str = "",
    capabilities: Sequence[Dict[str, Any]] = (),
) -> List[str]:
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
            if _declared_missing_reference(ref, skill_id, capabilities):
                continue
            errs.append(f"Missing referenced file `{ref}` in {md_path.relative_to(ROOT)}")
    return errs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--loose", action="store_true", help="compat mode: only require id/name/category + uniqueness")
    args = ap.parse_args()

    try:
        _, active_entries, legacy_count = validate_repository_contract(ROOT)
    except RepositoryContractError as exc:
        print("Validation failed:")
        for line in str(exc).splitlines():
            print(f"- {line}")
        raise SystemExit(1)

    errors: List[str] = []
    ids: Dict[str, Path] = {}
    active_ids = [str(item.get("id", "")).strip() for item in active_entries]
    release_capabilities, capability_errors = load_release_capabilities(active_ids)
    errors.extend(capability_errors)
    canonical_entries = [
        item for item in active_entries if str(item.get("category", "")).strip() != "composite"
    ]

    for item in canonical_entries:
        p = ROOT / str(item["path"])
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
        manifest_id = str(item.get("id", "")).strip()
        if sid and sid != manifest_id:
            errors.append(
                f"Manifest/front-matter id mismatch: {item['path']} has {sid}, expected {manifest_id}"
            )
        for key in ("name", "category"):
            manifest_value = str(item.get(key, "")).strip()
            front_matter_value = str(fm.get(key, "")).strip()
            if front_matter_value and front_matter_value != manifest_value:
                errors.append(
                    f"Manifest/front-matter `{key}` mismatch in {item['path']}: "
                    f"{front_matter_value!r} != {manifest_value!r}"
                )

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
        errors.extend(
            check_backtick_refs(
                p,
                text,
                skill_id=sid,
                capabilities=release_capabilities,
            )
        )

    if errors:
        print("Validation failed:")
        for e in errors:
            print(f"- {e}")
        raise SystemExit(1)

    print(
        "Validation passed: "
        f"active_canonical_skills={len(canonical_entries)} "
        f"legacy_nonroutable={legacy_count} "
        f"physical_skill_files={len(canonical_entries) + legacy_count}"
    )
    unavailable = sorted(
        str(record["id"])
        for record in release_capabilities
        if record.get("status") == "SOURCE_UNAVAILABLE"
    )
    print(
        "Safe-release capability declarations: "
        + (", ".join(f"{value}=SOURCE_UNAVAILABLE" for value in unavailable) or "NONE")
    )

if __name__ == "__main__":
    main()
