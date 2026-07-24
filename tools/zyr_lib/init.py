"""Safely initialize a minimal ZYR research workspace.

Usage:
  python tools/zyr.py init /absolute/or/relative/target
  python tools/zyr.py init /absolute/or/relative/target --apply
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml

from .manifest import ROOT, RepositoryContractError, validate_repository_contract

PROJECT_FILE = "ZYR_PROJECT.yaml"
RUN_FILE = "RESEARCH_RUN.md"


class InitError(RuntimeError):
    """Raised when initialization would cross a safety boundary."""


def _resolved_target(raw_target: str, root: Path) -> Path:
    if not raw_target.strip():
        raise InitError("An explicit target directory is required")
    target = Path(raw_target).expanduser().resolve()
    if target == Path(target.anchor) or target == root.resolve():
        raise InitError(f"Refusing unsafe target directory: {target}")
    parent = target.parent
    if not parent.is_dir():
        raise InitError(f"Target parent must already exist: {parent}")
    if target.exists():
        if not target.is_dir():
            raise InitError(f"Target exists and is not a directory: {target}")
        try:
            next(target.iterdir())
        except StopIteration:
            pass
        else:
            raise InitError(f"Target directory must be empty: {target}")
    return target


def _project_bytes(version: str) -> bytes:
    data: dict[str, Any] = {
        "schema_version": 1,
        "zyr_version": version,
        "run_record": RUN_FILE,
        "persistence": {
            "memory": "OFF",
            "source_changes": "APPROVAL_REQUIRED",
        },
    }
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True).encode("utf-8")


def _plan(raw_target: str, root: Path) -> tuple[Path, dict[str, bytes]]:
    target = _resolved_target(raw_target, root)
    try:
        manifest, _, _ = validate_repository_contract(root)
    except RepositoryContractError as exc:
        raise InitError(str(exc)) from exc
    template = root / "templates" / "orchestration" / RUN_FILE
    if not template.is_file():
        raise InitError(f"Required run template is missing: {template}")
    template_bytes = template.read_bytes()
    if not template_bytes:
        raise InitError(f"Required run template is empty: {template}")
    files = {
        PROJECT_FILE: _project_bytes(str(manifest["version"])),
        RUN_FILE: template_bytes,
    }
    return target, files


def _write_file_atomic(path: Path, data: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _apply_plan(target: Path, files: dict[str, bytes]) -> None:
    if target.exists():
        if any(target.iterdir()):
            raise InitError(f"Target became non-empty before write: {target}")
        for relative, data in files.items():
            destination = target / relative
            if destination.exists():
                raise InitError(f"Refusing to overwrite initialization file: {destination}")
            _write_file_atomic(destination, data)
        return

    temporary = Path(tempfile.mkdtemp(prefix=f".{target.name}.", dir=str(target.parent)))
    try:
        for relative, data in files.items():
            destination = temporary / relative
            destination.write_bytes(data)
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)


def run_init(
    raw_target: str,
    apply: bool = False,
    json_output: bool = False,
    root: Path = ROOT,
) -> int:
    """Plan by default; write only after the caller supplies --apply."""
    try:
        target, files = _plan(raw_target, root)
        if apply:
            _apply_plan(target, files)
    except (InitError, OSError, UnicodeError, yaml.YAMLError) as exc:
        print(f"Init failed: {exc}", file=sys.stderr)
        return 1

    payload = {
        "status": "APPLIED" if apply else "DRY_RUN",
        "target": str(target),
        "files": [str(target / relative) for relative in files],
        "memory_persistence": "OFF",
        "source_change_policy": "APPROVAL_REQUIRED",
    }
    if json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"INIT_STATUS: {payload['status']}")
        print(f"TARGET: {payload['target']}")
        for path in payload["files"]:
            print(f"FILE: {path}")
        if not apply:
            print("No files written. Re-run with --apply to create this exact workspace.")
    return 0
