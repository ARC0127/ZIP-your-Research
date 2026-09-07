#!/usr/bin/env python3
"""Update an existing ZYR Codex installation with short, reproducible entrypoints.

Usage:
  python tools/install_codex_profile_v1.py --skills-root PATH --check
  python tools/install_codex_profile_v1.py --skills-root PATH --apply --backup PATH
  python tools/install_codex_profile_v1.py --skills-root PATH --restore RECEIPT

Only ZYR files are changed. Every replaced file is backed up before mutation.
No model settings, claim skill, plugin cache, or automatic memory is modified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
POLICY = "boot/14_RESOURCE_PROPORTIONAL_EXECUTION_v1.md"
OVERLAY_FILES = (
    "AGENTS.md", "README.md", "boot/01_GLOBAL_GUARDRAILS_v1.7.0.md", POLICY,
    ".claude/skills/zip-your-research/SKILL.md", ".github/skills/zip-your-research/SKILL.md",
    "tools/zyr.py", "tools/zyr_lib/build.py", "tools/zyr_lib/resource_profile_v1.py",
    "tools/install_codex_profile_v1.py", "router/route_v1_8.py",
    "manifests/generated_files.yaml",
    "skills/writing_engine/MASTER_v1.7.0.md", "skills/coding_engine/MASTER_v1.7.0.md",
    "skills/proof_engine/MASTER_v1.5.md", "docs/RESOURCE_PROFILE_v1.md",
    "tests/integrity/test_resource_profile_v1.py", ".github/workflows/ci.yml",
    "templates/codex/zip-your-research.md", "templates/codex/zyr-research-suite.md",
    "templates/codex/zyr-research-evolution.md",
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def within(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"path escapes root: {relative}")
    return path


def front(text: str) -> dict:
    return yaml.safe_load(text.split("---", 2)[1])


def render_entry(meta: dict, sid: str, source: str, archive: Path) -> str:
    meta = dict(meta)
    title = sid if sid.startswith("S") else sid.replace("_", " ")
    original = front((ROOT / source).read_text(encoding="utf-8-sig")) if sid.startswith("S") else {}
    triggers = original.get("triggers", [])
    purpose = str(original.get("name", sid)).replace("_", " ")
    meta["description"] = f"ZYR {title}: {purpose}. Use for {', '.join(str(x) for x in triggers[:2]) or purpose}, or an explicit {sid} request."
    if sid == "S660":
        meta["description"] = "ZYR S660: explicitly requested multi-agent research, independent cross-examination, and candidate adjudication. Ordinary authoritative search uses a single-agent research skill."
    if sid == "writing_engine":
        meta["description"] = "ZYR writing workflow: select a local prose skill or integrated manuscript checks to match the requested edit."
    action = "Read `references/source.md` once and apply its output contract to the requested task."
    if sid in {"writing_engine", "coding_engine", "proof_engine", "rwf_s340_master", "figure_engine", "platform_zyr_skills"}:
        action = (
            "Use the module headings in `references/source.md` to select the applicable protocol; "
            "read those sections and their required references. Do not preload the entire master "
            "or all companion skills. A full workflow request retains the full applicable contract."
        )
    if sid == "writing_engine":
        action += " Local prose: S603; structure: S601; claim/evidence review: S602; result narrative: S604. Integrated manuscript review adds S640."
    if sid == "proof_engine":
        action += " Normalize only the needed assumptions and verify the relevant proof obligations. Local wording alone does not activate proof review."
    if sid == "S660":
        action += " Enter this workflow only when multi-agent research or independent cross-examination is explicitly selected; retain its real-worker gate."
    return (
        "---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False).strip() + "\n---\n\n"
        f"# ZYR {title}\n\nSuite v1.6.6; resource profile v1.\n\n"
        f"- Manifest id: `{sid}`\n- Upstream path: `{source}`\n\n"
        "Read `references/resource_policy.md` unless resource profile v1 is already "
        "loaded through another ZYR entry; all entries share this policy. It scopes retained blanket "
        "loading, companion, and repetition defaults; explicit approvals and scientific "
        "evidence requirements remain intact. Start with the current agent and one primary "
        "skill. Add work only for an unresolved obligation.\n\n"
        f"{action}\n\n"
        f"Paths inside the source protocol resolve against `{archive.as_posix()}`. "
        "Do not read the whole archive. Preserve user-frozen claims and mark missing evidence "
        "UNKNOWN. Do not claim a check ran unless it did.\n"
    )


def plan(skills: Path) -> dict[str, bytes]:
    archive = skills / "zip-your-research/references/upstream/ZIP-your-Research-main"
    if not (archive / "skills_manifest.yaml").is_file():
        raise ValueError("requires an existing full ZYR installation")
    manifest = yaml.safe_load((ROOT / "skills_manifest.yaml").read_text(encoding="utf-8"))
    canonical = {x["id"]: x["path"] for x in manifest["skills"]}
    canonical["platform_zyr_skills"] = "skills/platform_zyr_skills/README.md"
    changes: dict[str, bytes] = {}
    seen = set()
    policy = (ROOT / POLICY).read_bytes()
    for file in sorted(skills.glob("*/SKILL.md")):
        name = file.parent.name
        if name != "zip-your-research" and not name.startswith("zyr-"):
            continue
        text = file.read_text(encoding="utf-8-sig")
        meta = front(text)
        match = re.search(r"Manifest id: `([^`]+)`", text)
        if match:
            sid = match.group(1)
            if sid not in canonical or sid in seen:
                raise ValueError(f"unknown or duplicate installed manifest id: {sid}")
            seen.add(sid)
            source = canonical[sid]
            source_copy = file.parent / "references/source.md"
            if not source_copy.is_file():
                raise ValueError(f"missing preserved protocol: {source_copy}")
            changes[f"{name}/SKILL.md"] = render_entry(meta, sid, source, archive).encode("utf-8")
            changes[f"{name}/references/source.md"] = (ROOT / source).read_bytes()
        else:
            template = ROOT / "templates/codex" / f"{name}.md"
            if not template.is_file():
                raise ValueError(f"unrecognized ZYR entry: {name}")
            changes[f"{name}/SKILL.md"] = template.read_bytes()
            if name == "zyr-research-evolution":
                historical = file.parent / "references/full_evolution_protocol.md"
                changes[f"{name}/references/full_evolution_protocol.md"] = historical.read_bytes() if historical.exists() else file.read_bytes()
        changes[f"{name}/references/resource_policy.md"] = policy
    if seen != set(canonical):
        raise ValueError(f"installed manifest closure mismatch: missing={sorted(set(canonical)-seen)}")
    for relative in OVERLAY_FILES:
        changes[f"zip-your-research/references/upstream/ZIP-your-Research-main/{relative}"] = (ROOT / relative).read_bytes()
    router = skills / "zyr-research-evolution/scripts/route_manifest.py"
    text = router.read_text(encoding="utf-8")
    if '"route_v1_7.py"' not in text and '"route_v1_8.py"' not in text:
        raise ValueError("installed route_manifest.py has an unrecognized router binding")
    changes[router.relative_to(skills).as_posix()] = text.replace('"route_v1_7.py"', '"route_v1_8.py"').encode("utf-8")
    return changes


def apply(skills: Path, changes: dict[str, bytes], backup: Path) -> dict:
    backup = backup.resolve()
    if backup.is_relative_to(skills.resolve()):
        raise ValueError("backup must be outside the skills root")
    backup.mkdir(parents=True, exist_ok=False)
    records = []
    for relative, data in changes.items():
        dest = within(skills, relative)
        before = dest.read_bytes() if dest.exists() else None
        if before == data:
            continue
        if before is not None:
            saved = within(backup / "files", relative)
            saved.parent.mkdir(parents=True, exist_ok=True)
            saved.write_bytes(before)
        records.append({"path": relative, "before": sha(before) if before is not None else None, "after": sha(data)})
    receipt = {"skills_root": str(skills.resolve()), "files": records}
    (backup / "receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    # Preflight every target before the first write; avoid overwriting concurrent edits.
    for row in records:
        dest = within(skills, row["path"])
        current = sha(dest.read_bytes()) if dest.exists() else None
        if current != row["before"]:
            raise ValueError(f"concurrent edit before install: {row['path']}")
    for row in records:
        dest = within(skills, row["path"])
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(changes[row["path"]])
    for row in records:
        if sha(within(skills, row["path"]).read_bytes()) != row["after"]:
            raise ValueError(f"installed hash mismatch: {row['path']}")
    return receipt


def restore(skills: Path, receipt_path: Path) -> int:
    record = json.loads(receipt_path.read_text(encoding="utf-8"))
    if Path(record["skills_root"]).resolve() != skills.resolve():
        raise ValueError("receipt belongs to a different skills root")
    pending = []
    for row in record["files"]:
        dest = within(skills, row["path"])
        current = sha(dest.read_bytes()) if dest.exists() else None
        if current == row["before"]:
            continue  # also permits recovery after an interrupted apply/restore
        if current != row["after"]:
            raise ValueError(f"refusing to overwrite a later edit: {row['path']}")
        data = None
        if row["before"] is not None:
            data = within(receipt_path.parent / "files", row["path"]).read_bytes()
            if sha(data) != row["before"]:
                raise ValueError(f"backup hash mismatch: {row['path']}")
        pending.append((dest, data))
    for dest, data in pending:
        if data is None:
            dest.unlink()
        else:
            dest.write_bytes(data)
    return len(pending)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-root", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--restore", type=Path)
    parser.add_argument("--backup", type=Path)
    args = parser.parse_args()
    try:
        if args.restore:
            print(f"RESTORED: {restore(args.skills_root, args.restore)} files")
            return 0
        changes = plan(args.skills_root)
        drift = [p for p, data in changes.items() if not within(args.skills_root, p).is_file() or within(args.skills_root, p).read_bytes() != data]
        if args.check:
            print(json.dumps({"status": "PASS" if not drift else "DRIFT", "checked": len(changes), "drift": drift}, indent=2))
            return bool(drift)
        if not args.backup:
            raise ValueError("--apply requires --backup")
        receipt = apply(args.skills_root, changes, args.backup)
        print(json.dumps({"status": "APPLIED", "changed": len(receipt["files"]), "receipt": str(args.backup / "receipt.json")}))
        return 0
    except (ValueError, OSError, KeyError, yaml.YAMLError) as exc:
        parser.exit(1, f"Installation failed: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
