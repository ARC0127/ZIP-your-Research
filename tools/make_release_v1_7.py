#!/usr/bin/env python3
"""Build a fail-closed, reproducible v1.7 release archive.

The legacy ``tools/make_release.py`` is intentionally preserved. This builder
uses only Git-tracked files admitted by ``manifests/release_policy.yaml`` and
refuses dirty trees, symlinks, secrets, and unlicensed third-party assets.

Usage:
  python3 tools/make_release_v1_7.py
  python3 tools/make_release_v1_7.py --out /tmp/ZIP-your-Research.zip
  python3 tools/make_release_v1_7.py --root /path/to/repo --version v1.6.6
"""

from __future__ import annotations

import argparse
import errno
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping

import yaml


DEFAULT_POLICY = "manifests/release_policy.yaml"
DEFAULT_THIRD_PARTY = "manifests/THIRD_PARTY_ASSETS.yaml"


class ReleaseError(RuntimeError):
    """A release safety invariant failed."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ReleaseError(f"Missing policy file: {path}") from exc
    except yaml.YAMLError as exc:
        raise ReleaseError(f"Invalid YAML in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ReleaseError(f"Expected a YAML mapping in {path}")
    return value


def _normalize_rel(raw: str) -> str:
    value = raw.replace("\\", "/").strip("/")
    path = PurePosixPath(value)
    if not value or path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise ReleaseError(f"Unsafe relative path in policy or Git index: {raw!r}")
    return path.as_posix()


def _normalize_prefix(raw: str) -> str:
    return _normalize_rel(raw)


def _under_prefix(rel: str, prefix: str) -> bool:
    normalized = _normalize_prefix(prefix)
    return rel == normalized or rel.startswith(normalized + "/")


def _run_git(root: Path, args: list[str]) -> bytes:
    command = ["git", "-C", str(root), *args]
    completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise ReleaseError(f"Git command failed ({' '.join(args)}): {detail}")
    return completed.stdout


def _git_paths(root: Path, args: list[str]) -> list[str]:
    raw = _run_git(root, [*args, "-z"])
    return [_normalize_rel(item.decode("utf-8", errors="surrogateescape")) for item in raw.split(b"\0") if item]


def _relative_to_root(path: Path, root: Path) -> str | None:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return None


def ensure_clean_tracked_tree(root: Path, *, ignored_untracked: Iterable[str] = ()) -> list[str]:
    """Return tracked paths after rejecting untracked or modified source files."""

    _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    ignored = {_normalize_rel(value) for value in ignored_untracked}
    untracked = set(_git_paths(root, ["ls-files", "--others", "--exclude-standard"]))
    unexpected = sorted(untracked - ignored)
    if unexpected:
        raise ReleaseError("Untracked files refuse release:\n- " + "\n- ".join(unexpected))

    modified = set(_git_paths(root, ["diff", "--name-only"]))
    staged = set(_git_paths(root, ["diff", "--cached", "--name-only"]))
    dirty = sorted(modified | staged)
    if dirty:
        raise ReleaseError("Modified or staged files refuse release:\n- " + "\n- ".join(dirty))

    return sorted(_git_paths(root, ["ls-files", "--cached"]))


def path_is_allowed(rel: str, policy: dict[str, Any]) -> bool:
    allow = policy.get("allow") or {}
    exact = {_normalize_rel(str(value)) for value in allow.get("exact") or []}
    prefixes = [_normalize_prefix(str(value)) for value in allow.get("prefixes") or []]
    return rel in exact or any(_under_prefix(rel, prefix) for prefix in prefixes)


def path_is_denied(rel: str, policy: dict[str, Any]) -> bool:
    deny = policy.get("deny") or {}
    exact = {_normalize_rel(str(value)) for value in deny.get("exact") or []}
    if rel in exact:
        return True
    if any(_under_prefix(rel, str(prefix)) for prefix in deny.get("prefixes") or []):
        return True
    parts = set(PurePosixPath(rel).parts)
    if parts & {str(value) for value in deny.get("path_parts") or []}:
        return True
    name = PurePosixPath(rel).name
    if name in {str(value) for value in deny.get("basenames") or []}:
        return True
    return any(fnmatch.fnmatchcase(name, str(pattern)) for pattern in deny.get("name_globs") or [])


def required_exact_paths(policy: dict[str, Any]) -> set[str]:
    raw = (policy.get("required") or {}).get("exact")
    if not isinstance(raw, list) or not raw:
        raise ReleaseError("release policy requires a non-empty required.exact list")
    normalized = [_normalize_rel(str(value)) for value in raw]
    if len(normalized) != len(set(normalized)):
        raise ReleaseError("release policy required.exact contains duplicate paths")
    required = set(normalized)
    contradictions = sorted(
        rel
        for rel in required
        if not path_is_allowed(rel, policy) or path_is_denied(rel, policy)
    )
    if contradictions:
        raise ReleaseError(
            "Required release paths conflict with allow/deny policy:\n- "
            + "\n- ".join(contradictions)
        )
    return required


def validate_required_exact(policy: dict[str, Any], selected: Iterable[str]) -> set[str]:
    required = required_exact_paths(policy)
    missing = sorted(required - {_normalize_rel(rel) for rel in selected})
    if missing:
        raise ReleaseError("Release omits required exact paths:\n- " + "\n- ".join(missing))
    return required


def _yaml_mapping_from_package(
    package_files: Mapping[str, bytes], rel: str
) -> dict[str, Any]:
    try:
        value = yaml.safe_load(package_files[rel].decode("utf-8"))
    except KeyError as exc:
        raise ReleaseError(f"Release metadata file is missing: {rel}") from exc
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        raise ReleaseError(f"Invalid release metadata YAML in {rel}: {exc}") from exc
    if not isinstance(value, dict):
        raise ReleaseError(f"Expected a YAML mapping in release metadata: {rel}")
    return value


def validate_package_closure(
    policy: dict[str, Any],
    package_files: Mapping[str, bytes],
) -> None:
    """Validate required files plus active, self-check, and capability closure."""

    paths = {_normalize_rel(rel) for rel in package_files}
    validate_required_exact(policy, paths)
    errors: list[str] = []

    skill_manifest = _yaml_mapping_from_package(package_files, "skills_manifest.yaml")
    raw_skills = skill_manifest.get("skills")
    if not isinstance(raw_skills, list) or not raw_skills:
        raise ReleaseError("skills_manifest.yaml must contain a non-empty skills list")
    expected_active_count = (policy.get("required") or {}).get("active_skill_count")
    if (
        isinstance(expected_active_count, bool)
        or not isinstance(expected_active_count, int)
        or expected_active_count <= 0
    ):
        raise ReleaseError("release policy required.active_skill_count must be positive")
    if len(raw_skills) != expected_active_count:
        errors.append(
            "Active skill count does not match release policy: "
            f"{len(raw_skills)} != {expected_active_count}"
        )
    active_ids: set[str] = set()
    active_paths: set[str] = set()
    for index, raw in enumerate(raw_skills):
        if not isinstance(raw, dict):
            errors.append(f"skills_manifest.yaml entry {index} is not a mapping")
            continue
        skill_id = str(raw.get("id") or "").strip()
        raw_path = str(raw.get("path") or "").strip()
        if not skill_id or not raw_path:
            errors.append(f"skills_manifest.yaml entry {index} requires id and path")
            continue
        try:
            skill_path = _normalize_rel(raw_path)
        except ReleaseError as exc:
            errors.append(str(exc))
            continue
        if skill_id in active_ids:
            errors.append(f"Duplicate active skill id in release manifest: {skill_id}")
        if skill_path in active_paths:
            errors.append(f"Duplicate active skill path in release manifest: {skill_path}")
        active_ids.add(skill_id)
        active_paths.add(skill_path)
        if skill_path not in paths:
            errors.append(f"Release omits active skill path for {skill_id}: {skill_path}")

    compatibility = _yaml_mapping_from_package(
        package_files, "manifests/COMPATIBILITY.yaml"
    )
    compatibility_paths: list[str] = []
    public_cli = compatibility.get("public_cli")
    if isinstance(public_cli, dict) and public_cli.get("path"):
        compatibility_paths.append(str(public_cli["path"]))
    else:
        errors.append("COMPATIBILITY.yaml requires public_cli.path")
    raw_entrypoints = compatibility.get("compatibility_entrypoints")
    if not isinstance(raw_entrypoints, list):
        errors.append("COMPATIBILITY.yaml requires compatibility_entrypoints")
    else:
        for index, item in enumerate(raw_entrypoints):
            if not isinstance(item, dict) or not item.get("path"):
                errors.append(f"COMPATIBILITY.yaml entrypoint {index} requires path")
                continue
            compatibility_paths.append(str(item["path"]))
    for raw_path in compatibility_paths:
        try:
            relative = _normalize_rel(raw_path)
        except ReleaseError as exc:
            errors.append(str(exc))
            continue
        if relative not in paths:
            errors.append(f"Release omits compatibility entrypoint: {relative}")

    generated = _yaml_mapping_from_package(
        package_files, "manifests/generated_files.yaml"
    )
    raw_generated = generated.get("generated_files")
    expected_generated_count = (policy.get("required") or {}).get(
        "generated_file_count"
    )
    if (
        isinstance(expected_generated_count, bool)
        or not isinstance(expected_generated_count, int)
        or expected_generated_count <= 0
    ):
        raise ReleaseError("release policy required.generated_file_count must be positive")
    if not isinstance(raw_generated, list) or not raw_generated:
        errors.append("generated_files.yaml requires a non-empty generated_files list")
    else:
        if len(raw_generated) != expected_generated_count:
            errors.append(
                "Generated file count does not match release policy: "
                f"{len(raw_generated)} != {expected_generated_count}"
            )
        for index, item in enumerate(raw_generated):
            if not isinstance(item, dict) or not item.get("path"):
                errors.append(f"generated_files.yaml entry {index} requires path")
                continue
            try:
                output = _normalize_rel(str(item["path"]))
            except ReleaseError as exc:
                errors.append(str(exc))
                continue
            if output not in paths:
                errors.append(f"Release omits generated output: {output}")
            inputs = item.get("inputs")
            if not isinstance(inputs, list) or not inputs:
                errors.append(f"Generated output {output} requires inputs")
                continue
            for raw_input in inputs:
                try:
                    input_path = _normalize_rel(str(raw_input))
                except ReleaseError as exc:
                    errors.append(str(exc))
                    continue
                if input_path not in paths and not any(
                    _under_prefix(rel, input_path) for rel in paths
                ):
                    errors.append(
                        f"Release omits generated input for {output}: {input_path}"
                    )

    legacy = _yaml_mapping_from_package(
        package_files, "manifests/legacy_nonroutable.yaml"
    )
    raw_legacy = legacy.get("entries")
    expected_legacy_count = (policy.get("required") or {}).get("legacy_skill_count")
    if (
        isinstance(expected_legacy_count, bool)
        or not isinstance(expected_legacy_count, int)
        or expected_legacy_count < 0
    ):
        raise ReleaseError("release policy required.legacy_skill_count must be non-negative")
    if not isinstance(raw_legacy, list):
        errors.append("legacy_nonroutable.yaml requires an entries list")
    else:
        if len(raw_legacy) != expected_legacy_count:
            errors.append(
                "Legacy skill count does not match release policy: "
                f"{len(raw_legacy)} != {expected_legacy_count}"
            )
        for index, item in enumerate(raw_legacy):
            if not isinstance(item, dict) or not item.get("path"):
                errors.append(f"legacy_nonroutable.yaml entry {index} requires path")
                continue
            try:
                legacy_path = _normalize_rel(str(item["path"]))
            except ReleaseError as exc:
                errors.append(str(exc))
                continue
            if legacy_path not in paths:
                errors.append(f"Release omits declared legacy skill path: {legacy_path}")

    capability_rel = _normalize_rel(
        str(
            (policy.get("third_party") or {}).get("capabilities_manifest")
            or "manifests/RELEASE_CAPABILITIES.yaml"
        )
    )
    capabilities = _yaml_mapping_from_package(package_files, capability_rel)
    raw_capabilities = capabilities.get("capabilities")
    if not isinstance(raw_capabilities, list) or not raw_capabilities:
        errors.append(f"{capability_rel} requires a non-empty capabilities list")
    else:
        seen_capability_ids: set[str] = set()
        for index, item in enumerate(raw_capabilities):
            if not isinstance(item, dict):
                errors.append(f"{capability_rel} entry {index} is not a mapping")
                continue
            capability_id = str(item.get("id") or "").strip()
            status = str(item.get("status") or "").strip()
            missing_behavior = str(item.get("missing_behavior") or "").strip()
            raw_prefixes = item.get("allowed_missing_ref_prefixes")
            affected = item.get("affected_skill_ids")
            if not capability_id or capability_id in seen_capability_ids:
                errors.append(f"{capability_rel} entry {index} has a missing/duplicate id")
            seen_capability_ids.add(capability_id)
            if not isinstance(raw_prefixes, list) or not isinstance(affected, list):
                errors.append(
                    f"Capability {capability_id or index} requires "
                    "allowed_missing_ref_prefixes and affected_skill_ids lists"
                )
                continue
            try:
                missing_prefixes = [
                    _normalize_prefix(str(prefix)) for prefix in raw_prefixes
                ]
            except ReleaseError as exc:
                errors.append(str(exc))
                continue
            unknown_skills = sorted(
                str(skill_id) for skill_id in affected if str(skill_id) not in active_ids
            )
            if unknown_skills:
                errors.append(
                    f"Capability {capability_id} names inactive skill ids: "
                    + ", ".join(unknown_skills)
                )
            bundled_path = item.get("bundled_path")
            if status == "AVAILABLE":
                if (
                    not isinstance(bundled_path, str)
                    or not bundled_path
                    or missing_prefixes
                    or missing_behavior != "FAIL_CLOSED"
                ):
                    errors.append(
                        f"AVAILABLE capability {capability_id} has inconsistent availability fields"
                    )
                else:
                    try:
                        bundled = _normalize_prefix(bundled_path)
                    except ReleaseError as exc:
                        errors.append(str(exc))
                    else:
                        if not any(_under_prefix(rel, bundled) for rel in paths):
                            errors.append(
                                f"AVAILABLE capability source is absent: {capability_id}: {bundled}"
                            )
            elif status == "SOURCE_UNAVAILABLE":
                if (
                    bundled_path not in (None, "")
                    or not missing_prefixes
                    or missing_behavior != "SOURCE_UNAVAILABLE"
                ):
                    errors.append(
                        f"SOURCE_UNAVAILABLE capability {capability_id} has inconsistent fields"
                    )
                for prefix in missing_prefixes:
                    if any(_under_prefix(rel, prefix) for rel in paths):
                        errors.append(
                            f"Excluded capability prefix is unexpectedly bundled: "
                            f"{capability_id}: {prefix}"
                        )
            else:
                errors.append(f"Capability {capability_id} has unsupported status: {status}")

    if errors:
        raise ReleaseError("Release package closure failed:\n- " + "\n- ".join(errors))


def _has_symlink_component(root: Path, rel: str) -> bool:
    current = root
    for part in PurePosixPath(rel).parts:
        current = current / part
        if current.is_symlink():
            return True
    return False


def _compile_secret_patterns(policy: dict[str, Any]) -> list[tuple[str, re.Pattern[str]]]:
    compiled: list[tuple[str, re.Pattern[str]]] = []
    for item in (policy.get("secrets") or {}).get("patterns") or []:
        if not isinstance(item, dict) or not item.get("id") or not item.get("regex"):
            raise ReleaseError("Each secret pattern requires id and regex")
        try:
            compiled.append((str(item["id"]), re.compile(str(item["regex"]))))
        except re.error as exc:
            raise ReleaseError(f"Invalid secret regex {item.get('id')}: {exc}") from exc
    return compiled


def find_secret_pattern(
    data: bytes, rel: str, patterns: list[tuple[str, re.Pattern[str]]], max_text_bytes: int
) -> str | None:
    """Return the first matching secret pattern id without exposing its value."""

    try:
        text = data.decode("utf-8")
        if len(data) > max_text_bytes:
            raise ReleaseError(f"Text file exceeds configured secret-scan limit: {rel}")
    except UnicodeDecodeError:
        # Latin-1 preserves ASCII byte sequences so embedded credentials in a
        # binary container are still detected without printing their values.
        text = data.decode("latin-1")
    for pattern_id, pattern in patterns:
        if pattern.search(text):
            return pattern_id
    return None


def validate_third_party(
    root: Path,
    policy: dict[str, Any],
    third_party: dict[str, Any],
    selected: list[str],
) -> None:
    config = policy.get("third_party") or {}
    required_license = str(config.get("require_license_status") or "")
    required_redistribution = str(config.get("require_redistribution_status") or "")
    allowed_ids = {str(value) for value in config.get("allowed_asset_ids") or []}
    assets_raw = third_party.get("assets") or []
    if not isinstance(assets_raw, list):
        raise ReleaseError("Third-party manifest field 'assets' must be a list")

    assets: dict[str, dict[str, Any]] = {}
    for raw in assets_raw:
        if not isinstance(raw, dict) or not raw.get("id") or not raw.get("local_path"):
            raise ReleaseError("Every third-party asset requires id and local_path")
        asset_id = str(raw["id"])
        if asset_id in assets:
            raise ReleaseError(f"Duplicate third-party asset id: {asset_id}")
        assets[asset_id] = raw

    missing = sorted(allowed_ids - set(assets))
    if missing:
        raise ReleaseError("Allowed third-party assets are absent from manifest: " + ", ".join(missing))

    for asset_id, asset in assets.items():
        local_path = _normalize_prefix(str(asset["local_path"]))
        included = any(_under_prefix(rel, local_path) for rel in selected)
        if not included:
            continue
        license_data = asset.get("license") or {}
        redistribution = asset.get("redistribution") or {}
        if asset_id not in allowed_ids:
            raise ReleaseError(f"Unlisted third-party asset would be released: {asset_id}")
        if str(license_data.get("status")) != required_license:
            raise ReleaseError(f"Third-party asset has UNKNOWN or unverified license: {asset_id}")
        if str(redistribution.get("status")) != required_redistribution:
            raise ReleaseError(f"Third-party asset is not approved for redistribution: {asset_id}")
        license_path = license_data.get("license_path")
        if not isinstance(license_path, str) or license_path == "UNKNOWN":
            raise ReleaseError(f"Third-party asset lacks a local license path: {asset_id}")
        normalized_license = _normalize_rel(license_path)
        if not (root / normalized_license).is_file():
            raise ReleaseError(f"Third-party license file is missing: {normalized_license}")
        if normalized_license not in selected:
            raise ReleaseError(f"Third-party license file is omitted from release: {normalized_license}")

    if config.get("block_unknown_or_unlisted", True):
        for rel in selected:
            if not _under_prefix(rel, "ext/src"):
                continue
            owners = [
                asset_id
                for asset_id, asset in assets.items()
                if _under_prefix(rel, str(asset["local_path"]))
            ]
            if len(owners) != 1:
                raise ReleaseError(f"Vendored path has no unique third-party owner: {rel}")


def collect_release_files(
    root: Path,
    policy: dict[str, Any],
    third_party: dict[str, Any],
    tracked: list[str],
) -> list[tuple[str, bytes]]:
    selected: list[str] = []
    for rel in tracked:
        if not path_is_allowed(rel, policy) or path_is_denied(rel, policy):
            continue
        path = root / rel
        if _has_symlink_component(root, rel):
            raise ReleaseError(f"Symlink refuses release: {rel}")
        if not path.is_file():
            raise ReleaseError(f"Tracked release path is not a regular file: {rel}")
        selected.append(rel)

    validate_third_party(root, policy, third_party, selected)
    secret_patterns = _compile_secret_patterns(policy)
    max_text_bytes = int((policy.get("secrets") or {}).get("max_text_scan_bytes") or 2_097_152)

    files: list[tuple[str, bytes]] = []
    for rel in sorted(selected):
        data = (root / rel).read_bytes()
        pattern_id = find_secret_pattern(data, rel, secret_patterns, max_text_bytes)
        if pattern_id:
            raise ReleaseError(f"Secret pattern '{pattern_id}' refuses release in: {rel}")
        files.append((rel, data))
    return files


def _zip_info(arcname: str, policy: dict[str, Any]) -> zipfile.ZipInfo:
    values = (policy.get("zip") or {}).get("timestamp_utc") or [1980, 1, 1, 0, 0, 0]
    if not isinstance(values, list) or len(values) != 6:
        raise ReleaseError("zip.timestamp_utc must contain six integers")
    info = zipfile.ZipInfo(arcname, date_time=tuple(int(value) for value in values))
    info.create_system = 3
    mode = int(str((policy.get("zip") or {}).get("file_mode") or "0644"), 8)
    info.external_attr = (0o100000 | mode) << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    return info


def _fsync_file_if_supported(stream: Any) -> None:
    try:
        os.fsync(stream.fileno())
    except OSError as exc:
        unsupported = {
            value
            for value in (
                getattr(errno, "EINVAL", None),
                getattr(errno, "ENOTSUP", None),
                getattr(errno, "EOPNOTSUPP", None),
                getattr(errno, "ENOSYS", None),
            )
            if value is not None
        }
        if exc.errno not in unsupported:
            raise


def _fsync_directory_best_effort(path: Path) -> None:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    try:
        directory_fd = os.open(path, flags)
    except OSError:
        return
    try:
        try:
            os.fsync(directory_fd)
        except OSError:
            # Some platforms/filesystems do not support directory fsync.
            pass
    finally:
        try:
            os.close(directory_fd)
        except OSError:
            pass


def _write_zip_atomically(
    out: Path,
    policy: dict[str, Any],
    entries: list[tuple[str, bytes]],
) -> str:
    """Write a complete ZIP beside ``out`` and atomically replace it."""

    temporary: Path | None = None
    temporary_fd: int | None = None
    try:
        compression_level = (policy.get("zip") or {}).get("compresslevel")
        if (
            isinstance(compression_level, bool)
            or not isinstance(compression_level, int)
            or not 0 <= compression_level <= 9
        ):
            raise ReleaseError("zip.compresslevel must be an integer between 0 and 9")
        out.parent.mkdir(parents=True, exist_ok=True)
        temporary_fd, raw_temporary = tempfile.mkstemp(
            prefix=f".{out.name}.",
            suffix=".tmp",
            dir=out.parent,
        )
        temporary = Path(raw_temporary)
        stream = os.fdopen(temporary_fd, "w+b")
        temporary_fd = None
        with stream:
            with zipfile.ZipFile(
                stream,
                "w",
                compression=zipfile.ZIP_DEFLATED,
                compresslevel=compression_level,
            ) as archive:
                for arcname, data in entries:
                    archive.writestr(_zip_info(arcname, policy), data)
            stream.flush()
            _fsync_file_if_supported(stream)

        archive_sha256 = sha256_file(temporary)
        os.replace(temporary, out)
        temporary = None
        _fsync_directory_best_effort(out.parent)
        return archive_sha256
    except ReleaseError:
        raise
    except Exception as exc:
        raise ReleaseError(f"Atomic ZIP write failed: {type(exc).__name__}: {exc}") from exc
    finally:
        if temporary_fd is not None:
            os.close(temporary_fd)
        if temporary is not None:
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass
            except OSError as exc:
                raise ReleaseError(f"Failed to remove temporary release file: {temporary}") from exc


def _release_manifest(
    policy_path: Path,
    third_party_path: Path,
    policy: dict[str, Any],
    files: list[tuple[str, bytes]],
    release_version: str,
) -> bytes:
    file_data = dict(files)
    capability_rel = _normalize_rel(
        str(
            (policy.get("third_party") or {}).get("capabilities_manifest")
            or "manifests/RELEASE_CAPABILITIES.yaml"
        )
    )
    manifest = {
        "schema_version": 1,
        "policy_version": policy.get("policy_version"),
        "release_version": release_version,
        "archive_root": policy.get("archive_root"),
        "policy_sha256": sha256_bytes(policy_path.read_bytes()),
        "third_party_manifest_sha256": sha256_bytes(third_party_path.read_bytes()),
        "capabilities_manifest_sha256": sha256_bytes(file_data[capability_rel]),
        "files": [
            {"path": rel, "size": len(data), "sha256": sha256_bytes(data)}
            for rel, data in files
        ],
    }
    return (json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode(
        "utf-8"
    )


def build_release(
    *,
    root: Path,
    out: Path,
    policy_path: Path,
    third_party_path: Path,
    release_version: str,
) -> dict[str, Any]:
    root = root.resolve()
    out = out.resolve()
    policy = _load_yaml(policy_path)
    third_party = _load_yaml(third_party_path)
    if int(policy.get("schema_version") or 0) != 1:
        raise ReleaseError("Unsupported release policy schema_version")
    if int(third_party.get("schema_version") or 0) != 1:
        raise ReleaseError("Unsupported third-party manifest schema_version")

    ignored_untracked: list[str] = []
    output_rel = _relative_to_root(out, root)
    if output_rel:
        ignored_untracked.append(output_rel)
    tracked = ensure_clean_tracked_tree(root, ignored_untracked=ignored_untracked)
    files = collect_release_files(root, policy, third_party, tracked)
    if not files:
        raise ReleaseError("Release allowlist selected zero files")

    file_data = dict(files)
    validate_package_closure(policy, file_data)
    version_rel = _normalize_rel(str(policy.get("default_version_file") or "VERSION"))
    if version_rel not in file_data:
        raise ReleaseError(f"Release omits configured version file: {version_rel}")
    try:
        version_from_file = file_data[version_rel].decode("utf-8").strip()
    except UnicodeDecodeError as exc:
        raise ReleaseError(f"Version file is not valid UTF-8: {version_rel}") from exc
    if not version_from_file:
        raise ReleaseError(f"Version file is empty: {version_rel}")
    normalized_file_version = (
        version_from_file if version_from_file.startswith("v") else f"v{version_from_file}"
    )
    normalized_release_version = (
        release_version if release_version.startswith("v") else f"v{release_version}"
    )
    if normalized_release_version != normalized_file_version:
        raise ReleaseError(
            "Requested release version does not match "
            f"{version_rel}: {normalized_release_version!r} != {normalized_file_version!r}"
        )

    archive_root = _normalize_prefix(str(policy.get("archive_root") or "ZIP-your-Research"))
    generated_rel = _normalize_rel(
        str((policy.get("zip") or {}).get("generated_manifest_path") or "RELEASE_MANIFEST_v1_7.json")
    )
    manifest_data = _release_manifest(
        policy_path, third_party_path, policy, files, release_version
    )
    entries = [(f"{archive_root}/{rel}", data) for rel, data in files]
    entries.append((f"{archive_root}/{generated_rel}", manifest_data))
    entries.sort(key=lambda item: item[0])

    archive_sha256 = _write_zip_atomically(out, policy, entries)

    return {
        "archive": str(out),
        "release_version": release_version,
        "file_count": len(files),
        "archive_sha256": archive_sha256,
        "manifest_sha256": sha256_bytes(manifest_data),
    }


def _read_version(root: Path, policy: dict[str, Any]) -> str:
    version_file = root / str(policy.get("default_version_file") or "VERSION")
    try:
        value = version_file.read_text(encoding="utf-8").strip()
    except FileNotFoundError as exc:
        raise ReleaseError(f"Missing version file: {version_file}") from exc
    if not value:
        raise ReleaseError(f"Empty version file: {version_file}")
    return value if value.startswith("v") else f"v{value}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default="", help="repository root (default: parent of tools/)")
    parser.add_argument("--policy", default=DEFAULT_POLICY, help="release policy path, relative to root")
    parser.add_argument(
        "--third-party",
        default=DEFAULT_THIRD_PARTY,
        help="third-party asset manifest path, relative to root",
    )
    parser.add_argument("--version", default="", help="archive version label (default: read policy version file)")
    parser.add_argument("--out", default="", help="output ZIP path")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
    policy_path = Path(args.policy)
    if not policy_path.is_absolute():
        policy_path = root / policy_path
    third_party_path = Path(args.third_party)
    if not third_party_path.is_absolute():
        third_party_path = root / third_party_path

    try:
        policy = _load_yaml(policy_path)
        version = args.version or _read_version(root, policy)
        out = Path(args.out).resolve() if args.out else root / "dist" / f"ZIP-your-Research_{version}_release.zip"
        result = build_release(
            root=root,
            out=out,
            policy_path=policy_path,
            third_party_path=third_party_path,
            release_version=version,
        )
    except ReleaseError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
