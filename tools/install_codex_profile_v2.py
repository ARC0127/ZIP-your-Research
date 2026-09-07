#!/usr/bin/env python3
"""Install concise Astra discovery text and optionally the user's instruction profile.

Usage:
  python tools/install_codex_profile_v2.py --codex-home PATH --check
  python tools/install_codex_profile_v2.py --codex-home PATH --apply --backup PATH
  python tools/install_codex_profile_v2.py --codex-home PATH --include-user-instructions --check
  python tools/install_codex_profile_v2.py --codex-home PATH --restore RECEIPT

Requires an existing full ZYR install. --include-user-instructions explicitly
selects the supplied personal AGENTS profile and existing headroom/theory skills.
Backups must be outside CODEX_HOME. Model settings and automatic memories are
never installation targets. v1 remains available for compatibility/rollback.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml

import install_codex_profile_v1 as base

ROOT = Path(__file__).resolve().parents[1]
DESCRIPTIONS = "manifests/codex_descriptions_v1.yaml"
EXTRA_FILES = (
    DESCRIPTIONS, "tools/install_codex_profile_v2.py",
    "tests/integrity/test_astra_instructions_v1.py",
    "docs/ASTRA_INSTRUCTION_AUDIT_v1.md",
)


def descriptions() -> dict[str, str]:
    result = yaml.safe_load((ROOT / DESCRIPTIONS).read_text(encoding="utf-8"))
    manifest = yaml.safe_load((ROOT / "skills_manifest.yaml").read_text(encoding="utf-8"))
    expected = {entry["id"] for entry in manifest["skills"]} | {"platform_zyr_skills"}
    if set(result) != expected:
        raise ValueError("description keys must match the installed manifest identities")
    if any(not isinstance(value, str) or not value.strip() or len(value) > 160 for value in result.values()):
        raise ValueError("each discovery description must be nonempty and at most 160 characters")
    return result


def with_description(data: bytes, description: str) -> bytes:
    text = data.decode("utf-8-sig")
    _, header, body = text.split("---", 2)
    meta = yaml.safe_load(header)
    meta["description"] = description
    return ("---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False).strip() + "\n---" + body).encode("utf-8")


def plan(codex_home: Path, include_user_instructions: bool = False) -> dict[str, bytes]:
    changes = base.plan(codex_home / "skills")
    discovery = descriptions()
    for relative, data in list(changes.items()):
        if relative.count("/") != 1 or not relative.endswith("/SKILL.md"):
            continue
        match = re.search(r"Manifest id: `([^`]+)`", data.decode("utf-8-sig"))
        if match:
            changes[relative] = with_description(data, discovery[match.group(1)])
    archive = "zip-your-research/references/upstream/ZIP-your-Research-main/"
    templates = sorted(p for folder in ("templates/codex-home", "templates/codex-user-skills") for p in (ROOT / folder).rglob("*.md"))
    for relative in (*EXTRA_FILES, *(p.relative_to(ROOT).as_posix() for p in templates)):
        changes[archive + relative] = (ROOT / relative).read_bytes()
    result = {"skills/" + relative: data for relative, data in changes.items()}
    if include_user_instructions:
        if not (codex_home / "AGENTS.md").is_file():
            raise ValueError("personal profile requires an existing AGENTS.md; review templates before adopting")
        for source in (ROOT / "templates/codex-home").rglob("*.md"):
            result[source.relative_to(ROOT / "templates/codex-home").as_posix()] = source.read_bytes()
        for name in ("headroom", "theory-claim-audit"):
            relative = f"skills/{name}/SKILL.md"
            if not (codex_home / relative).is_file():
                raise ValueError(f"personal profile requires existing skill: {name}")
            result[relative] = (ROOT / f"templates/codex-user-skills/{name}.md").read_bytes()
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", type=Path, required=True)
    parser.add_argument("--include-user-instructions", action="store_true")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--restore", type=Path)
    parser.add_argument("--backup", type=Path)
    args = parser.parse_args()
    try:
        if args.restore:
            print(f"RESTORED: {base.restore(args.codex_home, args.restore)} files")
            return 0
        changes = plan(args.codex_home, args.include_user_instructions)
        drift = [p for p, data in changes.items() if not base.within(args.codex_home, p).is_file() or base.within(args.codex_home, p).read_bytes() != data]
        if args.check:
            print(json.dumps({"status": "PASS" if not drift else "DRIFT", "checked": len(changes), "drift": drift}, indent=2))
            return int(bool(drift))
        if not args.backup:
            raise ValueError("--apply requires --backup")
        receipt = base.apply(args.codex_home, changes, args.backup)
        print(json.dumps({"status": "APPLIED", "changed": len(receipt["files"]), "receipt": str(args.backup / "receipt.json")}))
        return 0
    except (ValueError, OSError, KeyError, yaml.YAMLError) as exc:
        parser.exit(1, f"Installation failed: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
