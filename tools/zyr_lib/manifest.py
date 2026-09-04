"""Load and validate the repository's authoritative metadata.

Usage:
  python tools/zyr.py check
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
SKILL_FILENAME_RE = re.compile(r"^S\d+_.*\.md$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class RepositoryContractError(RuntimeError):
    """Raised when repository metadata is missing or internally inconsistent."""


def resolve_repo_path(root: Path, raw_path: str, label: str) -> Path:
    """Resolve a repository-relative path while rejecting escapes."""
    relative = Path(raw_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise RepositoryContractError(f"{label} must be repository-relative: {raw_path!r}")
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise RepositoryContractError(f"{label} escapes repository root: {raw_path!r}") from exc
    return candidate


def load_yaml_mapping(path: Path) -> dict[str, Any]:
    """Load a YAML document and require a top-level mapping."""
    display_path = _display_path(path)
    if not path.is_file():
        raise RepositoryContractError(f"Required metadata file is missing: {display_path}")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise RepositoryContractError(f"Cannot parse {display_path}: {exc}") from exc
    if not isinstance(data, dict):
        raise RepositoryContractError(f"Expected a YAML mapping in {display_path}")
    return data


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


def parse_front_matter(path: Path) -> dict[str, Any]:
    """Parse YAML front matter from one Markdown file."""
    display_path = _display_path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise RepositoryContractError(f"Cannot read {display_path}: {exc}") from exc
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}
    try:
        data = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        raise RepositoryContractError(
            f"Cannot parse front matter in {display_path}: {exc}"
        ) from exc
    if not isinstance(data, dict):
        raise RepositoryContractError(
            f"Expected front-matter mapping in {display_path}"
        )
    return data


def load_active_manifest(
    root: Path = ROOT,
    allowed_missing_paths: set[str] | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Load the active registry and validate path closure.

    ``allowed_missing_paths`` is reserved for the build bootstrap: an active
    path may be absent only when the generated-files allowlist declares that
    exact path as an output. Normal manifest validation remains fail-closed.
    """
    allowed_missing = allowed_missing_paths or set()
    manifest_path = root / "skills_manifest.yaml"
    data = load_yaml_mapping(manifest_path)
    raw_entries = data.get("skills")
    if not isinstance(raw_entries, list) or not raw_entries:
        raise RepositoryContractError("skills_manifest.yaml must contain a non-empty `skills` list")

    entries: list[dict[str, Any]] = []
    seen_ids: dict[str, str] = {}
    seen_paths: dict[str, str] = {}
    errors: list[str] = []
    for index, raw in enumerate(raw_entries):
        if not isinstance(raw, dict):
            errors.append(f"skills_manifest.yaml entry {index} is not a mapping")
            continue
        entry = dict(raw)
        sid = str(entry.get("id", "")).strip()
        name = str(entry.get("name", "")).strip()
        category = str(entry.get("category", "")).strip()
        relative = str(entry.get("path", "")).strip()
        if not sid or not name or not category or not relative:
            errors.append(
                f"skills_manifest.yaml entry {index} requires id/name/category/path"
            )
            continue
        if sid in seen_ids:
            errors.append(f"Duplicate active skill id `{sid}`: {relative} and {seen_ids[sid]}")
        else:
            seen_ids[sid] = relative
        if relative in seen_paths:
            errors.append(
                f"Duplicate active skill path `{relative}`: {sid} and {seen_paths[relative]}"
            )
        else:
            seen_paths[relative] = sid
        try:
            path = resolve_repo_path(root, relative, f"path for active skill {sid}")
        except RepositoryContractError as exc:
            errors.append(str(exc))
        else:
            if not path.is_file() and relative not in allowed_missing:
                errors.append(f"Missing active skill path for `{sid}`: {relative}")
        entries.append(entry)

    if errors:
        raise RepositoryContractError("\n".join(errors))
    return data, entries


def validate_version_contract(
    manifest: dict[str, Any], root: Path = ROOT
) -> str:
    """Require VERSION, v, manifest, and compatibility metadata to agree."""
    values: dict[str, str] = {}
    for relative in ("VERSION", "v"):
        path = root / relative
        if not path.is_file():
            raise RepositoryContractError(f"Required version projection is missing: {relative}")
        value = path.read_text(encoding="utf-8").strip()
        if not value:
            raise RepositoryContractError(f"Required version projection is empty: {relative}")
        values[relative] = value

    values["skills_manifest.yaml#version"] = str(manifest.get("version", "")).strip()
    for label, value in values.items():
        if not SEMVER_RE.fullmatch(value):
            raise RepositoryContractError(f"Invalid semantic version in {label}: {value!r}")
    if len(set(values.values())) != 1:
        rendered = ", ".join(f"{key}={value}" for key, value in values.items())
        raise RepositoryContractError(f"Version contract mismatch: {rendered}")
    return values["VERSION"]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_legacy_overlay(
    active_entries: list[dict[str, Any]], root: Path = ROOT
) -> int:
    """Validate immutable non-routable aliases against active manifest IDs."""
    overlay = load_yaml_mapping(root / "manifests" / "legacy_nonroutable.yaml")
    if overlay.get("schema_version") != 1:
        raise RepositoryContractError("legacy_nonroutable.yaml schema_version must be 1")
    if overlay.get("hash_algorithm") != "sha256":
        raise RepositoryContractError("legacy_nonroutable.yaml hash_algorithm must be sha256")
    raw_entries = overlay.get("entries")
    if not isinstance(raw_entries, list):
        raise RepositoryContractError("legacy_nonroutable.yaml must contain an `entries` list")

    active_by_id = {str(item["id"]): item for item in active_entries}
    declared_paths: set[str] = set()
    errors: list[str] = []
    for index, raw in enumerate(raw_entries):
        if not isinstance(raw, dict):
            errors.append(f"legacy overlay entry {index} is not a mapping")
            continue
        sid = str(raw.get("id", "")).strip()
        relative = str(raw.get("path", "")).strip()
        expected_hash = str(raw.get("sha256", "")).strip()
        if not sid or not relative or not SHA256_RE.fullmatch(expected_hash):
            errors.append(f"legacy overlay entry {index} requires id/path/64-char sha256")
            continue
        if relative in declared_paths:
            errors.append(f"Duplicate legacy overlay path: {relative}")
            continue
        declared_paths.add(relative)
        active = active_by_id.get(sid)
        if active is None:
            errors.append(f"Legacy `{relative}` maps to inactive/unknown id `{sid}`")
            continue
        canonical_relative = str(active["path"])
        if relative == canonical_relative:
            errors.append(f"Legacy path cannot equal canonical path for `{sid}`: {relative}")
            continue
        try:
            legacy_path = resolve_repo_path(root, relative, f"legacy path for {sid}")
            canonical_path = resolve_repo_path(
                root, canonical_relative, f"canonical path for {sid}"
            )
        except RepositoryContractError as exc:
            errors.append(str(exc))
            continue
        if not legacy_path.is_file():
            errors.append(f"Missing declared legacy path for `{sid}`: {relative}")
            continue
        actual_hash = _sha256(legacy_path)
        if actual_hash != expected_hash:
            errors.append(
                f"Legacy hash mismatch for `{sid}` at {relative}: "
                f"expected {expected_hash}, got {actual_hash}"
            )
        try:
            legacy_id = str(parse_front_matter(legacy_path).get("id", "")).strip()
            canonical_id = str(parse_front_matter(canonical_path).get("id", "")).strip()
        except RepositoryContractError as exc:
            errors.append(str(exc))
            continue
        if legacy_id != sid:
            errors.append(f"Legacy front-matter id mismatch at {relative}: {legacy_id!r} != {sid}")
        if canonical_id != sid:
            errors.append(
                f"Canonical front-matter id mismatch at {canonical_relative}: "
                f"{canonical_id!r} != {sid}"
            )

    observed_paths: set[str] = set()
    canonical_paths = {
        str(item["path"])
        for item in active_entries
        if SKILL_FILENAME_RE.fullmatch(Path(str(item["path"])).name)
    }
    skills_root = root / "skills"
    for path in sorted(skills_root.rglob("*.md")):
        relative = path.relative_to(root).as_posix()
        if "platform_zyr_skills/rewrites/" in relative:
            continue
        if not SKILL_FILENAME_RE.fullmatch(path.name):
            continue
        if relative in canonical_paths:
            continue
        observed_paths.add(relative)
        try:
            sid = str(parse_front_matter(path).get("id", "")).strip()
        except RepositoryContractError as exc:
            errors.append(str(exc))
            continue
        if not sid:
            errors.append(f"Non-canonical skill path has no front-matter id: {relative}")
        elif sid not in active_by_id:
            errors.append(
                f"Non-canonical skill path has no active manifest mapping: "
                f"{relative} (id={sid})"
            )

    for relative in sorted(observed_paths - declared_paths):
        errors.append(f"Undeclared non-canonical skill path: {relative}")
    for relative in sorted(declared_paths - observed_paths):
        errors.append(f"Declared legacy path is not a non-canonical active-ID alias: {relative}")
    if errors:
        raise RepositoryContractError("\n".join(errors))
    return len(raw_entries)


def validate_compatibility_contract(root: Path = ROOT) -> None:
    """Validate the single public CLI and the explicitly retained legacy entrypoints."""
    data = load_yaml_mapping(root / "manifests" / "COMPATIBILITY.yaml")
    if data.get("schema_version") != 1:
        raise RepositoryContractError("COMPATIBILITY.yaml schema_version must be 1")
    version_contract = data.get("version_contract")
    if not isinstance(version_contract, dict):
        raise RepositoryContractError(
            "COMPATIBILITY.yaml requires a `version_contract` mapping"
        )
    if version_contract.get("authoritative") != "VERSION":
        raise RepositoryContractError(
            "COMPATIBILITY.yaml must declare VERSION as the authoritative version source"
        )
    public_cli = data.get("public_cli")
    if not isinstance(public_cli, dict):
        raise RepositoryContractError("COMPATIBILITY.yaml requires a `public_cli` mapping")
    public_path = str(public_cli.get("path", "")).strip()
    if public_cli.get("status") != "stable" or public_path != "tools/zyr.py":
        raise RepositoryContractError(
            "COMPATIBILITY.yaml must declare tools/zyr.py as the sole stable public CLI"
        )
    if not resolve_repo_path(root, public_path, "public CLI").is_file():
        raise RepositoryContractError(f"Public CLI is missing: {public_path}")

    legacy = data.get("compatibility_entrypoints")
    if not isinstance(legacy, list):
        raise RepositoryContractError(
            "COMPATIBILITY.yaml requires a `compatibility_entrypoints` list"
        )
    seen: set[str] = set()
    for index, item in enumerate(legacy):
        if not isinstance(item, dict):
            raise RepositoryContractError(f"compatibility entrypoint {index} is not a mapping")
        relative = str(item.get("path", "")).strip()
        if not relative or item.get("status") != "compatibility_only":
            raise RepositoryContractError(
                f"compatibility entrypoint {index} requires path/status=compatibility_only"
            )
        if relative == public_path or relative in seen:
            raise RepositoryContractError(f"Duplicate/conflicting compatibility path: {relative}")
        seen.add(relative)
        if not resolve_repo_path(root, relative, "compatibility entrypoint").is_file():
            raise RepositoryContractError(f"Compatibility entrypoint is missing: {relative}")


def validate_repository_contract(
    root: Path = ROOT,
    allowed_missing_active_paths: set[str] | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]], int]:
    """Validate version, active registry, legacy aliases, and CLI compatibility."""
    manifest, active_entries = load_active_manifest(root, allowed_missing_active_paths)
    validate_version_contract(manifest, root)
    legacy_count = validate_legacy_overlay(active_entries, root)
    validate_compatibility_contract(root)
    return manifest, active_entries, legacy_count


def run_manifest(
    root: Path = ROOT, skill_id: str = "", json_output: bool = False
) -> int:
    """Print a read-only view of active canonical manifest state."""
    try:
        manifest, entries, legacy_count = validate_repository_contract(root)
    except RepositoryContractError as exc:
        print(f"Manifest check failed: {exc}", file=sys.stderr)
        return 1

    selected: dict[str, Any] | None = None
    if skill_id:
        selected = next(
            (entry for entry in entries if str(entry.get("id", "")) == skill_id),
            None,
        )
        if selected is None:
            print(f"Unknown active skill id: {skill_id}", file=sys.stderr)
            return 1

    categories = Counter(str(entry["category"]) for entry in entries)
    payload: dict[str, Any] = {
        "version": str(manifest["version"]),
        "authority": "skills_manifest.yaml",
        "active_skill_count": len(entries),
        "legacy_nonroutable_count": legacy_count,
        "category_counts": dict(sorted(categories.items())),
    }
    if selected is not None:
        payload["skill"] = selected
    elif json_output:
        payload["skills"] = entries

    if json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    print(f"VERSION: {payload['version']}")
    print(f"AUTHORITY: {payload['authority']}")
    print(f"ACTIVE_SKILLS: {payload['active_skill_count']}")
    print(f"LEGACY_NONROUTABLE: {payload['legacy_nonroutable_count']}")
    print(
        "CATEGORIES: "
        + ", ".join(f"{name}={count}" for name, count in payload["category_counts"].items())
    )
    if selected is not None:
        print(f"SKILL_ID: {selected['id']}")
        print(f"SKILL_PATH: {selected['path']}")
        print(f"SKILL_CATEGORY: {selected['category']}")
    return 0
