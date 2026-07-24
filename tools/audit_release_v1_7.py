#!/usr/bin/env python3
"""Audit a v1.7 release ZIP without extracting it.

The audit checks ZIP integrity, deterministic metadata, manifest closure,
allowlist/deny rules, third-party license gates, symlinks, and secret patterns.

Usage:
  python3 tools/audit_release_v1_7.py dist/ZIP-your-Research_v1.6.6_release.zip
  python3 tools/audit_release_v1_7.py /tmp/release.zip --root /path/to/repo
"""

from __future__ import annotations

import argparse
import json
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

try:
    from .make_release_v1_7 import (
        DEFAULT_POLICY,
        DEFAULT_THIRD_PARTY,
        ReleaseError,
        _compile_secret_patterns,
        _load_yaml,
        _normalize_prefix,
        _normalize_rel,
        _under_prefix,
        find_secret_pattern,
        path_is_allowed,
        path_is_denied,
        sha256_bytes,
        sha256_file,
        validate_package_closure,
        validate_required_exact,
    )
except ImportError:
    from make_release_v1_7 import (  # type: ignore
        DEFAULT_POLICY,
        DEFAULT_THIRD_PARTY,
        ReleaseError,
        _compile_secret_patterns,
        _load_yaml,
        _normalize_prefix,
        _normalize_rel,
        _under_prefix,
        find_secret_pattern,
        path_is_allowed,
        path_is_denied,
        sha256_bytes,
        sha256_file,
        validate_package_closure,
        validate_required_exact,
    )


def _parse_manifest(data: bytes) -> dict[str, Any]:
    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReleaseError(f"Invalid generated release manifest: {exc}") from exc
    if not isinstance(value, dict) or not isinstance(value.get("files"), list):
        raise ReleaseError("Generated release manifest must contain a files list")
    return value


def _required_positive_int(config: dict[str, Any], key: str) -> int:
    value = config.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ReleaseError(f"zip.{key} must be a positive integer")
    return value


def _required_positive_number(config: dict[str, Any], key: str) -> float:
    value = config.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
        raise ReleaseError(f"zip.{key} must be a positive number")
    return float(value)


def _audit_third_party_archive(
    policy: dict[str, Any], third_party: dict[str, Any], selected: list[str]
) -> None:
    config = policy.get("third_party") or {}
    allowed_ids = {str(value) for value in config.get("allowed_asset_ids") or []}
    required_license = str(config.get("require_license_status") or "")
    required_redistribution = str(config.get("require_redistribution_status") or "")
    assets = third_party.get("assets") or []
    if not isinstance(assets, list):
        raise ReleaseError("Third-party assets must be a list")

    owner_count: dict[str, int] = {rel: 0 for rel in selected if _under_prefix(rel, "ext/src")}
    for raw in assets:
        if not isinstance(raw, dict) or not raw.get("id") or not raw.get("local_path"):
            raise ReleaseError("Malformed third-party asset record")
        asset_id = str(raw["id"])
        local_path = _normalize_prefix(str(raw["local_path"]))
        owned = [rel for rel in selected if _under_prefix(rel, local_path)]
        for rel in owned:
            owner_count[rel] = owner_count.get(rel, 0) + 1
        if not owned:
            continue
        license_data = raw.get("license") or {}
        redistribution = raw.get("redistribution") or {}
        if asset_id not in allowed_ids:
            raise ReleaseError(f"Archive contains unlisted third-party asset: {asset_id}")
        if str(license_data.get("status")) != required_license:
            raise ReleaseError(f"Archive contains UNKNOWN or unverified license asset: {asset_id}")
        if str(redistribution.get("status")) != required_redistribution:
            raise ReleaseError(f"Archive contains redistribution-blocked asset: {asset_id}")
        license_path = license_data.get("license_path")
        if not isinstance(license_path, str) or license_path == "UNKNOWN":
            raise ReleaseError(f"Archive asset lacks a license path: {asset_id}")
        if _normalize_rel(license_path) not in selected:
            raise ReleaseError(f"Archive omits third-party license: {license_path}")

    bad_owners = sorted(rel for rel, count in owner_count.items() if count != 1)
    if bad_owners:
        raise ReleaseError("Vendored archive paths lack a unique owner:\n- " + "\n- ".join(bad_owners))


def audit_release(
    *,
    archive_path: Path,
    policy_path: Path,
    third_party_path: Path,
) -> dict[str, Any]:
    policy = _load_yaml(policy_path)
    third_party = _load_yaml(third_party_path)
    archive_root = _normalize_prefix(str(policy.get("archive_root") or "ZIP-your-Research"))
    generated_rel = _normalize_rel(
        str((policy.get("zip") or {}).get("generated_manifest_path") or "RELEASE_MANIFEST_v1_7.json")
    )
    generated_arc = f"{archive_root}/{generated_rel}"
    expected_timestamp = tuple(
        int(value)
        for value in ((policy.get("zip") or {}).get("timestamp_utc") or [1980, 1, 1, 0, 0, 0])
    )
    expected_mode = int(str((policy.get("zip") or {}).get("file_mode") or "0644"), 8)
    zip_policy = policy.get("zip") or {}
    max_entries = _required_positive_int(zip_policy, "max_entries")
    max_archive_bytes = _required_positive_int(zip_policy, "max_archive_bytes")
    max_entry_bytes = _required_positive_int(zip_policy, "max_entry_uncompressed_bytes")
    max_total_bytes = _required_positive_int(zip_policy, "max_total_uncompressed_bytes")
    max_compression_ratio = _required_positive_number(zip_policy, "max_compression_ratio")
    patterns = _compile_secret_patterns(policy)
    max_text_bytes = int((policy.get("secrets") or {}).get("max_text_scan_bytes") or 2_097_152)

    try:
        archive_size = archive_path.stat().st_size
        if archive_size > max_archive_bytes:
            raise ReleaseError(
                f"ZIP archive size exceeds policy limit: {archive_size} > {max_archive_bytes}"
            )
        archive = zipfile.ZipFile(archive_path, "r")
    except ReleaseError:
        raise
    except (OSError, zipfile.BadZipFile) as exc:
        raise ReleaseError(f"Cannot open release archive: {archive_path}: {exc}") from exc

    with archive:
        infos = archive.infolist()
        if len(infos) > max_entries:
            raise ReleaseError(
                f"ZIP entry count exceeds policy limit: {len(infos)} > {max_entries}"
            )
        names = [info.filename for info in infos]
        if names != sorted(names):
            raise ReleaseError("ZIP entries are not in deterministic sorted order")
        if len(names) != len(set(names)):
            raise ReleaseError("ZIP contains duplicate entry names")

        total_uncompressed = 0
        for info in infos:
            if info.file_size < 0 or info.compress_size < 0:
                raise ReleaseError(f"ZIP entry reports an invalid size: {info.filename}")
            if info.file_size > max_entry_bytes:
                raise ReleaseError(
                    "ZIP entry uncompressed size exceeds policy limit: "
                    f"{info.filename}: {info.file_size} > {max_entry_bytes}"
                )
            total_uncompressed += info.file_size
            if total_uncompressed > max_total_bytes:
                raise ReleaseError(
                    "ZIP total uncompressed size exceeds policy limit: "
                    f"{total_uncompressed} > {max_total_bytes}"
                )
            if info.file_size > 0:
                if info.compress_size <= 0:
                    raise ReleaseError(
                        f"ZIP entry has an invalid infinite compression ratio: {info.filename}"
                    )
                ratio = info.file_size / info.compress_size
                if ratio > max_compression_ratio:
                    raise ReleaseError(
                        "ZIP entry compression ratio exceeds policy limit: "
                        f"{info.filename}: {ratio:.2f} > {max_compression_ratio:g}"
                    )
            arc_path = PurePosixPath(info.filename)
            if info.is_dir() or arc_path.is_absolute() or ".." in arc_path.parts:
                raise ReleaseError(f"Unsafe or unexpected ZIP entry: {info.filename}")
            if not info.filename.startswith(archive_root + "/"):
                raise ReleaseError(f"ZIP entry escapes archive root: {info.filename}")
            unix_mode = info.external_attr >> 16
            if stat.S_ISLNK(unix_mode):
                raise ReleaseError(f"ZIP symlink refuses release: {info.filename}")
            if info.flag_bits & 0x1:
                raise ReleaseError(f"Encrypted ZIP entry refuses audit: {info.filename}")
            if info.date_time != expected_timestamp:
                raise ReleaseError(f"Non-deterministic timestamp in ZIP entry: {info.filename}")
            if unix_mode & 0o777 != expected_mode:
                raise ReleaseError(f"Unexpected file mode in ZIP entry: {info.filename}")

        if generated_arc not in names:
            raise ReleaseError(f"ZIP omits generated manifest: {generated_arc}")

        actual_rel = sorted(
            name[len(archive_root) + 1 :]
            for name in names
            if name != generated_arc
        )
        validate_required_exact(policy, actual_rel)

        payloads: dict[str, bytes] = {}
        for info in infos:
            try:
                payloads[info.filename] = archive.read(info)
            except Exception as exc:
                raise ReleaseError(
                    f"ZIP entry failed CRC/decompression validation: {info.filename}: {exc}"
                ) from exc

        manifest = _parse_manifest(payloads[generated_arc])
        release_version = manifest.get("release_version")
        if not isinstance(release_version, str) or not release_version:
            raise ReleaseError("Generated manifest omits release_version")
        if manifest.get("policy_sha256") != sha256_bytes(policy_path.read_bytes()):
            raise ReleaseError("Generated manifest policy hash does not match audit policy")
        if manifest.get("third_party_manifest_sha256") != sha256_bytes(third_party_path.read_bytes()):
            raise ReleaseError("Generated manifest third-party hash does not match audit manifest")
        capability_rel = _normalize_rel(
            str(
                (policy.get("third_party") or {}).get("capabilities_manifest")
                or "manifests/RELEASE_CAPABILITIES.yaml"
            )
        )
        capability_path = policy_path.resolve().parents[1] / capability_rel
        try:
            capability_sha256 = sha256_bytes(capability_path.read_bytes())
        except OSError as exc:
            raise ReleaseError(
                f"Cannot read release capabilities manifest: {capability_path}: {exc}"
            ) from exc
        if manifest.get("capabilities_manifest_sha256") != capability_sha256:
            raise ReleaseError(
                "Generated manifest capabilities hash does not match audit manifest"
            )

        expected_records: dict[str, dict[str, Any]] = {}
        for record in manifest["files"]:
            if not isinstance(record, dict) or not record.get("path"):
                raise ReleaseError("Malformed file record in generated manifest")
            rel = _normalize_rel(str(record["path"]))
            if rel in expected_records:
                raise ReleaseError(f"Duplicate file record in generated manifest: {rel}")
            expected_records[rel] = record

        if actual_rel != sorted(expected_records):
            missing = sorted(set(expected_records) - set(actual_rel))
            extra = sorted(set(actual_rel) - set(expected_records))
            raise ReleaseError(f"Manifest closure mismatch; missing={missing}, extra={extra}")

        package_files = {
            rel: payloads[f"{archive_root}/{rel}"]
            for rel in actual_rel
        }
        validate_package_closure(policy, package_files)

        version_rel = _normalize_rel(str(policy.get("default_version_file") or "VERSION"))
        if version_rel not in actual_rel:
            raise ReleaseError(f"Archive omits configured version file: {version_rel}")
        try:
            version_from_file = payloads[f"{archive_root}/{version_rel}"].decode("utf-8").strip()
        except UnicodeDecodeError as exc:
            raise ReleaseError(f"Archive version file is not valid UTF-8: {version_rel}") from exc
        normalized_file_version = (
            version_from_file if version_from_file.startswith("v") else f"v{version_from_file}"
        )
        normalized_manifest_version = (
            release_version if release_version.startswith("v") else f"v{release_version}"
        )
        if not version_from_file or normalized_file_version != normalized_manifest_version:
            raise ReleaseError(
                "Archive release_version does not match "
                f"{version_rel}: {normalized_manifest_version!r} != {normalized_file_version!r}"
            )

        for rel in actual_rel:
            if not path_is_allowed(rel, policy) or path_is_denied(rel, policy):
                raise ReleaseError(f"Archive path violates release policy: {rel}")
            data = payloads[f"{archive_root}/{rel}"]
            record = expected_records[rel]
            if record.get("size") != len(data) or record.get("sha256") != sha256_bytes(data):
                raise ReleaseError(f"Manifest size/hash mismatch: {rel}")
            pattern_id = find_secret_pattern(data, rel, patterns, max_text_bytes)
            if pattern_id:
                raise ReleaseError(f"Secret pattern '{pattern_id}' found in archive path: {rel}")

        _audit_third_party_archive(policy, third_party, actual_rel)

    try:
        archive_sha256 = sha256_file(archive_path)
    except OSError as exc:
        raise ReleaseError(f"Cannot hash release archive: {archive_path}: {exc}") from exc

    return {
        "archive": str(archive_path.resolve()),
        "archive_sha256": archive_sha256,
        "release_version": release_version,
        "file_count": len(expected_records),
        "status": "PASS",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", help="release ZIP to audit")
    parser.add_argument("--root", default="", help="repository root (default: parent of tools/)")
    parser.add_argument("--policy", default=DEFAULT_POLICY, help="policy path, relative to root")
    parser.add_argument(
        "--third-party",
        default=DEFAULT_THIRD_PARTY,
        help="third-party manifest path, relative to root",
    )
    args = parser.parse_args(argv)

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
    policy_path = Path(args.policy)
    if not policy_path.is_absolute():
        policy_path = root / policy_path
    third_party_path = Path(args.third_party)
    if not third_party_path.is_absolute():
        third_party_path = root / third_party_path

    try:
        result = audit_release(
            archive_path=Path(args.archive),
            policy_path=policy_path,
            third_party_path=third_party_path,
        )
    except ReleaseError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
