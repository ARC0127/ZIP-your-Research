#!/usr/bin/env python3
"""Validate ZIP-your-Research v1.6.6 release identity and compatibility.

Usage:
  python tools/validate_release_identity_v1_6_6.py
  python tools/validate_release_identity_v1_6_6.py --root /path/to/repo
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

import yaml

EXPECTED = "1.6.6"


def _read(root: Path, relative: str) -> str:
    path = root / relative
    if not path.is_file():
        raise ValueError(f"missing required file: {relative}")
    return path.read_text(encoding="utf-8")


def _acknowledgments_block(readme: str) -> str:
    match = re.search(
        r"(?ms)^##+\s+Acknowledgments and references\s*$.*?(?=^##+\s+|\Z)",
        readme,
    )
    if not match:
        raise ValueError("README acknowledgments block is missing")
    return match.group(0)


def validate(root: Path) -> list[str]:
    errors: list[str] = []

    for relative in ("VERSION", "v"):
        value = _read(root, relative).strip()
        if value != EXPECTED:
            errors.append(f"{relative}: expected {EXPECTED}, found {value!r}")

    manifest = yaml.safe_load(_read(root, "skills_manifest.yaml")) or {}
    if str(manifest.get("version")) != EXPECTED:
        errors.append("skills_manifest.yaml version does not match 1.6.6")
    entries = {
        str(item.get("id")): str(item.get("path"))
        for item in manifest.get("skills", [])
        if isinstance(item, dict)
    }
    expected_paths = {
        "writing_engine": "skills/writing_engine/MASTER_v1.6.6.md",
        "coding_engine": "skills/coding_engine/MASTER_v1.6.6.md",
    }
    for skill_id, expected_path in expected_paths.items():
        if entries.get(skill_id) != expected_path:
            errors.append(
                f"manifest {skill_id}: expected {expected_path}, found {entries.get(skill_id)!r}"
            )

    required_markers = {
        "README.md": [
            "# ZIP-your-Research (ZYR) v1.6.6",
            "docs/VERSION_IDENTITY_v1.6.6.md",
        ],
        "AGENTS.md": [
            "# AGENTS.md (suite v1.6.6)",
            "boot/00_RESPONSE_STATUS_BANNER_v1.6.6.md",
            "boot/01_GLOBAL_GUARDRAILS_v1.6.6.md",
        ],
        ".claude/skills/zip-your-research/SKILL.md": [
            "suite v1.6.6",
            "docs/VERSION_IDENTITY_v1.6.6.md",
        ],
        ".github/skills/zip-your-research/SKILL.md": [
            "suite v1.6.6",
            "docs/VERSION_IDENTITY_v1.6.6.md",
        ],
        "boot/00_RESPONSE_STATUS_BANNER_v1.6.6.md": ["suite v1.6.6"],
        "boot/01_GLOBAL_GUARDRAILS_v1.6.6.md": ["suite v1.6.6"],
        "skills/writing_engine/MASTER_v1.6.6.md": [
            "# MASTER v1.6.6 (Writing Engine)",
            "Component lineage",
        ],
        "skills/coding_engine/MASTER_v1.6.6.md": [
            "# MASTER v1.6.6 (Coding Engine)",
            "Component lineage",
        ],
        "router/SKILL_MAP_v1.6.6.md": ["# Skill Map (v1.6.6)"],
    }
    for relative, markers in required_markers.items():
        text = _read(root, relative)
        for marker in markers:
            if marker not in text:
                errors.append(f"{relative}: missing marker {marker!r}")

    if "# AGENTS.md (v1.3.2)" in _read(root, "AGENTS.md"):
        errors.append("AGENTS.md still presents v1.3.2 as the active suite")

    for legacy in (
        "boot/00_RESPONSE_STATUS_BANNER_v1.3.2.md",
        "boot/01_GLOBAL_GUARDRAILS_v1.3.2.md",
        "skills/writing_engine/MASTER_v1.3.2.md",
        "skills/coding_engine/MASTER_v1.3.2.md",
        "router/SKILL_MAP_v1.3.2.md",
    ):
        if not (root / legacy).is_file():
            errors.append(f"legacy compatibility asset was removed: {legacy}")

    baseline: dict[str, str] = {}
    for line in _read(root, "manifests/ACKNOWLEDGMENTS_BASELINE_v1.6.6.sha256").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            baseline[key.strip()] = value.strip()
    block = _acknowledgments_block(_read(root, "README.md")).encode("utf-8")
    digest = hashlib.sha256(block).hexdigest()
    if digest != baseline.get("sha256"):
        errors.append("README acknowledgments block changed or was deleted")
    if str(len(block)) != baseline.get("utf8_bytes"):
        errors.append("README acknowledgments byte count changed")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        errors = validate(root)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"RELEASE_IDENTITY_FAIL: {exc}")
        return 1
    if errors:
        print("RELEASE_IDENTITY_FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("RELEASE_IDENTITY_PASS: suite=1.6.6 legacy_lineage_preserved=true acknowledgments_preserved=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
