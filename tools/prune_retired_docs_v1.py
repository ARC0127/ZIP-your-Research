#!/usr/bin/env python3
"""Remove exact retired document copies from a checkout or installed suite.

Usage:
  python tools/prune_retired_docs_v1.py --root PATH --check
  python tools/prune_retired_docs_v1.py --root PATH --apply --backup PATH
  python tools/prune_retired_docs_v1.py --root PATH --restore RECEIPT

Only the versioned retirement list is eligible. Changed copies are preserved.
Every deletion is backed up; restore refuses to overwrite subsequent edits.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from install_codex_profile_v1 import restore, sha, within

ROOT = Path(__file__).resolve().parents[1]


def pending(root: Path, records: list[dict]) -> dict[str, bytes]:
    result = {}
    for row in records:
        relative = row["path"]
        path = within(root, relative)
        if relative.startswith(("skills/", "ext/", ".codex/")):
            raise ValueError(f"not a retired documentation path: {relative}")
        if not path.exists():
            continue
        data = path.read_bytes()
        normalized = data if path.suffix == ".pdf" else data.replace(b"\r\n", b"\n")
        if hashlib.sha256(normalized).hexdigest() != row["sha256"]:
            raise ValueError(f"preserving changed document; inspect before removal: {relative}")
        result[relative] = data
    return result


def apply(root: Path, records: list[dict], backup: Path) -> int:
    changes = pending(root, records)
    if backup.resolve().is_relative_to(root.resolve()):
        raise ValueError("backup must be outside the target root")
    backup.mkdir(parents=True, exist_ok=False)
    receipt = {"skills_root": str(root.resolve()), "files": []}
    for relative, data in changes.items():
        saved = within(backup / "files", relative)
        saved.parent.mkdir(parents=True, exist_ok=True)
        saved.write_bytes(data)
        receipt["files"].append({"path": relative, "before": sha(data), "after": None})
    (backup / "receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    # Validate the whole set again before the first deletion.
    for relative, data in changes.items():
        if within(root, relative).read_bytes() != data:
            raise ValueError(f"concurrent edit before cleanup: {relative}")
    for relative in changes:
        within(root, relative).unlink()
    return len(changes)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--restore", type=Path)
    parser.add_argument("--backup", type=Path)
    args = parser.parse_args()
    try:
        if args.restore:
            print(f"RESTORED: {restore(args.root, args.restore)} files")
            return 0
        records = json.loads((ROOT / "manifests/retired_documents_v1.json").read_text(encoding="utf-8"))["files"]
        if args.check:
            remaining = list(pending(args.root, records))
            print(json.dumps({"status": "PASS" if not remaining else "RETIRED_COPIES_PRESENT", "remaining": remaining}, indent=2))
            return int(bool(remaining))
        if not args.backup:
            raise ValueError("--apply requires --backup")
        count = apply(args.root, records, args.backup)
        print(json.dumps({"removed": count, "receipt": str(args.backup / "receipt.json")}))
        return 0
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(1, f"Document cleanup failed: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
