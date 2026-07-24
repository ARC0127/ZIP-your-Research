"""Governed dynamic Skill memory for ZYR.

Usage:
  python tools/zyr.py skill-memory draft TRACE.yaml
  python tools/zyr.py skill-memory plan create --root ROOT --proposal PROPOSAL.yaml --trusted-consent-public-key HOST.pem
  python tools/zyr.py skill-memory apply create --root ROOT --proposal PROPOSAL.yaml --trusted-consent-public-key HOST.pem --consent-id ID --consent-attestation ATTESTATION.json
  python tools/zyr.py skill-memory list --root ROOT
  python tools/zyr.py skill-memory search --root ROOT --query "literature review"
  python tools/zyr.py skill-memory verify --root ROOT

The source repository is never a valid dynamic-memory root. Draft and plan are
read-only. Every mutation is a second phase bound to an exact consent ID.
"""

from __future__ import annotations

import copy
import base64
import hashlib
import json
import os
import re
import secrets
import shutil
import sys
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator, Mapping, Sequence

import yaml
from yaml.constructor import ConstructorError
from yaml.resolver import BaseResolver
from yaml.tokens import AliasToken, AnchorToken, TagToken

from .manifest import ROOT


SCHEMA_VERSION = 1
STORE_TYPE = "ZYR_DYNAMIC_SKILL_MEMORY"
REGISTRY_FILE = "registry.yaml"
AUDIT_FILE = "audit/events.jsonl"
INDEX_FILE = "index/skill_catalog.json"
LOCK_FILE = ".skill-memory.lock"
PREPARED_FILE = "journal/PREPARED.json"
QUARANTINE_DIR = "journal/quarantine"
TRUSTED_CONSENT_PUBLIC_KEY_FILE = "trust/consent_public_key.pem"
AUTHORIZATION_RECEIPT_DIR = "audit/authorizations"
MAX_YAML_BYTES = 8 * 1024 * 1024
MAX_ATTESTATION_BYTES = 64 * 1024
MAX_AUTHORIZATION_RECEIPT_BYTES = 1024 * 1024
MAX_EVALUATION_ARTIFACT_BYTES = 32 * 1024 * 1024
CONSENT_KIND = "ZYR_SKILL_MEMORY_USER_CONSENT"
AUTHORIZATION_RECEIPT_KIND = "ZYR_SKILL_MEMORY_AUTHORIZATION_RECEIPT"
CONSENT_MAX_LIFETIME = timedelta(minutes=15)

# RFC 8032 Ed25519 verification constants. ZYR only verifies host-produced
# signatures; private-key generation and signing remain outside the agent.
_ED25519_P = 2**255 - 19
_ED25519_L = 2**252 + 27742317777372353535851937790883648493
_ED25519_D = (
    -121665 * pow(121666, _ED25519_P - 2, _ED25519_P)
) % _ED25519_P
_ED25519_I = pow(2, (_ED25519_P - 1) // 4, _ED25519_P)
_ED25519_BASE_Y = (4 * pow(5, _ED25519_P - 2, _ED25519_P)) % _ED25519_P
_ED25519_SPKI_PREFIX = bytes.fromhex("302a300506032b6570032100")

DYNAMIC_SKILL_ID_RE = re.compile(r"^dyn-[a-z0-9][a-z0-9-]{2,59}$")
TRACE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$")
ACTOR_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@/-]{1,127}$")
PROPOSAL_ID_RE = re.compile(r"^smp-[0-9a-f]{16}$")
EVALUATION_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$")
ATTESTATION_ID_RE = re.compile(r"^att-[A-Za-z0-9][A-Za-z0-9._:-]{7,127}$")
NONCE_RE = re.compile(r"^[A-Za-z0-9_-]{16,128}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("openai_key", re.compile(r"(?<![A-Za-z0-9])sk-(?:proj-)?[A-Za-z0-9_-]{20,}")),
    ("github_pat", re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}")),
    ("aws_access_key", re.compile(r"AKIA[0-9A-Z]{16}")),
    (
        "private_key",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ),
    (
        "assigned_secret",
        re.compile(
            r"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)"
            r"\s*[:=]\s*[\"']?[A-Za-z0-9_./+=-]{16,}"
        ),
    ),
)

INJECTION_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "instruction_override",
        re.compile(
            r"(?i)(?:ignore|disregard|override).{0,40}(?:instruction|prompt|rule)"
            r"|(?:忽略|覆盖|绕过).{0,30}(?:指令|提示|规则)"
        ),
    ),
    (
        "authority_escalation",
        re.compile(
            r"(?i)(?:system\s+prompt|developer\s+message|reveal.{0,20}secret)"
            r"|(?:系统提示|开发者消息|泄露.{0,20}(?:密钥|秘密))"
        ),
    ),
)

DESTRUCTIVE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("recursive_root_delete", re.compile(r"(?i)\brm\s+-rf\s+(?:/|~|\$HOME)\b")),
    (
        "powershell_recursive_force_delete",
        re.compile(r"(?i)\bRemove-Item\b.{0,100}\b-Recurse\b.{0,100}\b-Force\b"),
    ),
    (
        "download_pipe_shell",
        re.compile(r"(?i)\b(?:curl|wget)\b.{0,200}\|\s*(?:sh|bash|zsh|powershell)\b"),
    ),
    (
        "executable_code_fence",
        re.compile(r"(?i)```(?:bash|sh|zsh|powershell|cmd|batch|python|javascript|typescript)"),
    ),
    (
        "runtime_install",
        re.compile(r"(?i)\b(?:pip|uv\s+pip|npm|pnpm|yarn|conda)\s+install\b"),
    ),
    (
        "preauthorized_tools",
        re.compile(r"(?im)^\s*allowed-tools\s*:"),
    ),
    (
        "approval_ui_spoof",
        re.compile(r"(?i)<\s*(?:button|form)\b|approve\s+(?:delete|update|create)"),
    ),
)

REQUIRED_BODY_HEADINGS = (
    "## When to use",
    "## Procedure",
    "## Evidence and limits",
    "## Failure boundaries",
)


class SkillMemoryError(RuntimeError):
    """Raised when a dynamic Skill memory operation fails closed."""


@dataclass
class _StoreLockLease:
    path: Path
    descriptor: int
    token: str
    device: int
    inode: int


class _UniqueKeySafeLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects ambiguous duplicate mapping keys."""


class _NoAliasSafeDumper(yaml.SafeDumper):
    """Emit canonical self-contained YAML without anchors or aliases."""

    def ignore_aliases(self, data: Any) -> bool:
        return True


def _construct_unique_mapping(
    loader: _UniqueKeySafeLoader,
    node: yaml.nodes.MappingNode,
    deep: bool = False,
) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable mapping key",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found a duplicate key",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeySafeLoader.add_constructor(
    BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _read_stable_bytes(path: Path, label: str, maximum: int) -> bytes:
    if not path.is_file():
        raise SkillMemoryError(f"{label} is missing: {path}")
    _reject_link_or_hardlink(path, label)
    before = path.stat()
    if before.st_size > maximum:
        raise SkillMemoryError(f"{label} exceeds the {maximum}-byte limit")
    raw = path.read_bytes()
    after = path.stat()
    before_identity = (
        before.st_dev,
        before.st_ino,
        before.st_size,
        before.st_mtime_ns,
    )
    after_identity = (
        after.st_dev,
        after.st_ino,
        after.st_size,
        after.st_mtime_ns,
    )
    if before_identity != after_identity:
        raise SkillMemoryError(f"{label} changed while it was being read")
    if len(raw) > maximum:
        raise SkillMemoryError(f"{label} exceeds the {maximum}-byte limit")
    return raw


def _read_yaml_mapping(path: Path, label: str) -> dict[str, Any]:
    try:
        raw = _read_stable_bytes(path, label, MAX_YAML_BYTES)
        text = raw.decode("utf-8")
        if "\x00" in text:
            raise SkillMemoryError(f"{label} contains a NUL byte")
        for token in yaml.scan(text):
            if isinstance(token, (AliasToken, AnchorToken, TagToken)):
                raise SkillMemoryError(
                    f"{label} contains forbidden YAML aliases, anchors, or tags"
                )
        value = yaml.load(text, Loader=_UniqueKeySafeLoader)
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise SkillMemoryError(f"Cannot parse {label} {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SkillMemoryError(f"{label} must be a YAML mapping: {path}")
    return value


def _unique_json_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise SkillMemoryError("JSON record contains a duplicate key")
        result[key] = value
    return result


def _read_json_mapping(
    path: Path,
    label: str,
    maximum: int = MAX_ATTESTATION_BYTES,
) -> dict[str, Any]:
    try:
        raw = _read_stable_bytes(path, label, maximum)
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_unique_json_pairs,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SkillMemoryError(f"Cannot parse {label} {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SkillMemoryError(f"{label} must be a JSON object: {path}")
    return value


def _path_is_within(candidate: Path, parent: Path) -> bool:
    try:
        candidate.relative_to(parent)
    except ValueError:
        return False
    return True


def _is_link_like(path: Path) -> bool:
    if path.is_symlink():
        return True
    is_junction = getattr(path, "is_junction", None)
    return bool(is_junction and is_junction())


def _has_symlink_component(path: Path) -> bool:
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current = current / part
        if not current.exists():
            break
        if _is_link_like(current):
            return True
    return False


def _resolve_root(raw_root: str, *, source_root: Path = ROOT) -> Path:
    if not str(raw_root).strip():
        raise SkillMemoryError("An explicit dynamic Skill memory root is required")
    expanded = Path(raw_root).expanduser()
    absolute = Path(os.path.abspath(str(expanded)))
    if _has_symlink_component(absolute):
        raise SkillMemoryError(
            f"Dynamic Skill memory root crosses a symlink: {absolute}"
        )
    candidate = absolute.resolve(strict=False)
    source = source_root.resolve()
    home = Path.home().resolve()
    if candidate == Path(candidate.anchor) or candidate == home:
        raise SkillMemoryError(f"Refusing unsafe dynamic Skill memory root: {candidate}")
    if candidate == source or _path_is_within(candidate, source):
        raise SkillMemoryError(
            "Dynamic Skill memory must be outside the ZYR source repository: "
            f"{candidate}"
        )
    if _has_symlink_component(candidate):
        raise SkillMemoryError(f"Dynamic Skill memory root crosses a symlink: {candidate}")
    parent = candidate.parent
    if not parent.is_dir():
        raise SkillMemoryError(f"Dynamic Skill memory root parent must exist: {parent}")
    if candidate.exists() and not candidate.is_dir():
        raise SkillMemoryError(f"Dynamic Skill memory root is not a directory: {candidate}")
    return candidate


def _safe_child(root: Path, relative: str) -> Path:
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        raise SkillMemoryError(f"Unsafe dynamic Skill memory path: {relative!r}")
    unresolved = root / rel
    if _has_symlink_component(unresolved):
        raise SkillMemoryError(
            f"Dynamic Skill memory path crosses a symlink or junction: {unresolved}"
        )
    candidate = unresolved.resolve(strict=False)
    if candidate == root or not _path_is_within(candidate, root):
        raise SkillMemoryError(f"Dynamic Skill memory path escapes root: {relative!r}")
    if _has_symlink_component(candidate):
        raise SkillMemoryError(f"Dynamic Skill memory path crosses a symlink: {candidate}")
    return candidate


def _validate_dynamic_id(skill_id: str) -> str:
    normalized = str(skill_id).strip()
    if not DYNAMIC_SKILL_ID_RE.fullmatch(normalized):
        raise SkillMemoryError(
            "Dynamic Skill id must match dyn-[a-z0-9][a-z0-9-]{2,59}: "
            f"{normalized!r}"
        )
    return normalized


def _nonempty_string(value: Any, field: str, *, maximum: int = 4096) -> str:
    text = str(value or "").strip()
    if not text:
        raise SkillMemoryError(f"{field} must be a non-empty string")
    if len(text) > maximum:
        raise SkillMemoryError(f"{field} exceeds {maximum} characters")
    if "\x00" in text:
        raise SkillMemoryError(f"{field} contains a NUL byte")
    return text


def _string_list(
    value: Any,
    field: str,
    *,
    minimum: int = 0,
    maximum: int = 128,
    item_maximum: int = 4096,
) -> list[str]:
    if not isinstance(value, list):
        raise SkillMemoryError(f"{field} must be a list")
    items = [
        _nonempty_string(item, f"{field}[]", maximum=item_maximum) for item in value
    ]
    if len(items) < minimum:
        raise SkillMemoryError(f"{field} requires at least {minimum} item(s)")
    if len(items) > maximum:
        raise SkillMemoryError(f"{field} exceeds {maximum} item(s)")
    if len(set(items)) != len(items):
        raise SkillMemoryError(f"{field} contains duplicate items")
    return items


def _scan_untrusted_text(text: str, field: str) -> None:
    for family, patterns in (
        ("secret", SECRET_PATTERNS),
        ("prompt-injection", INJECTION_PATTERNS),
        ("destructive instruction", DESTRUCTIVE_PATTERNS),
    ):
        for pattern_id, pattern in patterns:
            if pattern.search(text):
                raise SkillMemoryError(
                    f"{field} failed {family} scan: {pattern_id}"
                )


def _reject_link_or_hardlink(path: Path, label: str) -> None:
    if _is_link_like(path):
        raise SkillMemoryError(f"{label} is a symlink or junction: {path}")
    if path.is_file() and path.stat().st_nlink > 1:
        raise SkillMemoryError(f"{label} is a hardlink: {path}")


def _root_identity(root: Path) -> dict[str, Any]:
    if root.exists():
        stat = root.stat()
        return {
            "kind": "existing_root",
            "device": int(stat.st_dev),
            "inode": int(stat.st_ino),
        }
    stat = root.parent.stat()
    return {
        "kind": "absent_root",
        "parent_device": int(stat.st_dev),
        "parent_inode": int(stat.st_ino),
        "new_name": root.name,
    }


def _lock_path(root: Path) -> Path:
    return (
        root / LOCK_FILE
        if root.exists()
        else root.parent / f".{root.name}.skill-memory.lock"
    )


def _resolve_source_file(raw_path: str, label: str, root: Path) -> Path:
    if not str(raw_path).strip():
        raise SkillMemoryError(f"{label} path is required")
    absolute = Path(os.path.abspath(str(Path(raw_path).expanduser())))
    if _has_symlink_component(absolute):
        raise SkillMemoryError(f"{label} path crosses a symlink or junction: {absolute}")
    resolved = absolute.resolve(strict=False)
    if not resolved.is_file():
        raise SkillMemoryError(f"{label} is missing: {resolved}")
    _reject_link_or_hardlink(resolved, label)
    if _path_is_within(resolved, root):
        raise SkillMemoryError(f"{label} must be outside the managed dynamic store")
    return resolved


Ed25519Point = tuple[int, int, int, int]


def _ed25519_recover_x(y: int, sign: int) -> int | None:
    if y >= _ED25519_P:
        return None
    y_squared = y * y % _ED25519_P
    denominator = (_ED25519_D * y_squared + 1) % _ED25519_P
    if denominator == 0:
        return None
    x_squared = (
        (y_squared - 1)
        * pow(denominator, _ED25519_P - 2, _ED25519_P)
    ) % _ED25519_P
    x = pow(x_squared, (_ED25519_P + 3) // 8, _ED25519_P)
    if (x * x - x_squared) % _ED25519_P:
        x = x * _ED25519_I % _ED25519_P
    if (x * x - x_squared) % _ED25519_P:
        return None
    if x == 0 and sign:
        return None
    if (x & 1) != sign:
        x = _ED25519_P - x
    return x


def _ed25519_point_from_xy(x: int, y: int) -> Ed25519Point:
    return x, y, 1, x * y % _ED25519_P


_ED25519_IDENTITY = _ed25519_point_from_xy(0, 1)
_ED25519_BASE_X = _ed25519_recover_x(_ED25519_BASE_Y, 0)
if _ED25519_BASE_X is None:  # pragma: no cover - constant integrity guard
    raise RuntimeError("Invalid Ed25519 base point constants")
_ED25519_BASE = _ed25519_point_from_xy(
    _ED25519_BASE_X,
    _ED25519_BASE_Y,
)


def _ed25519_add(left: Ed25519Point, right: Ed25519Point) -> Ed25519Point:
    x1, y1, z1, t1 = left
    x2, y2, z2, t2 = right
    a = (y1 - x1) * (y2 - x2) % _ED25519_P
    b = (y1 + x1) * (y2 + x2) % _ED25519_P
    c = 2 * _ED25519_D * t1 * t2 % _ED25519_P
    d = 2 * z1 * z2 % _ED25519_P
    e = (b - a) % _ED25519_P
    f = (d - c) % _ED25519_P
    g = (d + c) % _ED25519_P
    h = (b + a) % _ED25519_P
    return (
        e * f % _ED25519_P,
        g * h % _ED25519_P,
        f * g % _ED25519_P,
        e * h % _ED25519_P,
    )


def _ed25519_scalar_mult(point: Ed25519Point, scalar: int) -> Ed25519Point:
    result = _ED25519_IDENTITY
    addend = point
    while scalar:
        if scalar & 1:
            result = _ed25519_add(result, addend)
        addend = _ed25519_add(addend, addend)
        scalar >>= 1
    return result


def _ed25519_points_equal(left: Ed25519Point, right: Ed25519Point) -> bool:
    x1, y1, z1, _ = left
    x2, y2, z2, _ = right
    return (
        (x1 * z2 - x2 * z1) % _ED25519_P == 0
        and (y1 * z2 - y2 * z1) % _ED25519_P == 0
    )


def _ed25519_decode_point(encoded: bytes) -> Ed25519Point | None:
    if len(encoded) != 32:
        return None
    value = int.from_bytes(encoded, "little")
    sign = value >> 255
    y = value & ((1 << 255) - 1)
    x = _ed25519_recover_x(y, sign)
    if x is None:
        return None
    return _ed25519_point_from_xy(x, y)


@dataclass(frozen=True)
class _Ed25519PublicKey:
    raw: bytes
    point: Ed25519Point

    @classmethod
    def from_raw(cls, raw: bytes) -> "_Ed25519PublicKey":
        point = _ed25519_decode_point(raw)
        if point is None:
            raise ValueError("Invalid Ed25519 public key encoding")
        if _ed25519_points_equal(point, _ED25519_IDENTITY):
            raise ValueError("Ed25519 public key cannot be the identity")
        if not _ed25519_points_equal(
            _ed25519_scalar_mult(point, _ED25519_L),
            _ED25519_IDENTITY,
        ):
            raise ValueError("Ed25519 public key is not in the prime subgroup")
        return cls(raw=bytes(raw), point=point)

    def verify(self, signature: bytes, message: bytes) -> bool:
        if len(signature) != 64:
            return False
        encoded_r = signature[:32]
        scalar_s = int.from_bytes(signature[32:], "little")
        if scalar_s >= _ED25519_L:
            return False
        point_r = _ed25519_decode_point(encoded_r)
        if point_r is None:
            return False
        challenge = int.from_bytes(
            hashlib.sha512(encoded_r + self.raw + message).digest(),
            "little",
        ) % _ED25519_L
        left = _ed25519_scalar_mult(_ED25519_BASE, scalar_s)
        right = _ed25519_add(
            point_r,
            _ed25519_scalar_mult(self.point, challenge),
        )
        return _ed25519_points_equal(left, right)

    def subject_public_key_info(self) -> bytes:
        return _ED25519_SPKI_PREFIX + self.raw

    def public_pem(self) -> bytes:
        encoded = base64.b64encode(self.subject_public_key_info()).decode("ascii")
        body = "\n".join(
            encoded[index : index + 64]
            for index in range(0, len(encoded), 64)
        )
        return (
            "-----BEGIN PUBLIC KEY-----\n"
            f"{body}\n"
            "-----END PUBLIC KEY-----\n"
        ).encode("ascii")


def _load_ed25519_public_key_pem(raw: bytes) -> tuple[_Ed25519PublicKey, bytes]:
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise ValueError("PEM must be ASCII") from exc
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if (
        len(lines) < 3
        or lines[0] != "-----BEGIN PUBLIC KEY-----"
        or lines[-1] != "-----END PUBLIC KEY-----"
    ):
        raise ValueError("Expected a PUBLIC KEY PEM block")
    try:
        der = base64.b64decode("".join(lines[1:-1]), validate=True)
    except (ValueError, base64.binascii.Error) as exc:
        raise ValueError("PEM body is not valid base64") from exc
    if (
        len(der) != len(_ED25519_SPKI_PREFIX) + 32
        or not der.startswith(_ED25519_SPKI_PREFIX)
    ):
        raise ValueError("PEM does not contain an Ed25519 SubjectPublicKeyInfo")
    return (
        _Ed25519PublicKey.from_raw(der[len(_ED25519_SPKI_PREFIX) :]),
        der,
    )


def _load_consent_public_key(
    raw_path: str,
    root: Path,
) -> tuple[Path, _Ed25519PublicKey, str]:
    path = _resolve_source_file(raw_path, "trusted consent public key", root)
    raw = _read_stable_bytes(path, "trusted consent public key", 16 * 1024)
    try:
        key, der = _load_ed25519_public_key_pem(raw)
    except ValueError as exc:
        raise SkillMemoryError(
            "Trusted consent public key must be valid Ed25519 PUBLIC KEY PEM"
        ) from exc
    return path, key, _sha256_bytes(der)


def _load_store_consent_public_key(
    root: Path,
    expected_sha256: str,
) -> _Ed25519PublicKey:
    path = _safe_child(root, TRUSTED_CONSENT_PUBLIC_KEY_FILE)
    raw = _read_stable_bytes(
        path,
        "stored trusted consent public key",
        16 * 1024,
    )
    try:
        key, der = _load_ed25519_public_key_pem(raw)
    except ValueError as exc:
        raise SkillMemoryError(
            "Stored trusted consent public key is not valid Ed25519 PEM"
        ) from exc
    if _sha256_bytes(der) != expected_sha256:
        raise SkillMemoryError(
            "Stored trusted consent public key fingerprint does not match registry"
        )
    return key


def _parse_utc_timestamp(raw: Any, field: str) -> datetime:
    text = _nonempty_string(raw, field, maximum=64)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise SkillMemoryError(f"{field} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise SkillMemoryError(f"{field} must include a timezone")
    return parsed.astimezone(timezone.utc)


def _verify_host_attestation(
    *,
    plan: Mapping[str, Any],
    root: Path,
    raw_attestation: str,
    public_key: _Ed25519PublicKey,
    public_key_sha256: str,
    now: datetime | None = None,
) -> dict[str, Any]:
    path = _resolve_source_file(
        raw_attestation,
        "host consent attestation",
        root,
    )
    value = _read_json_mapping(path, "host consent attestation")
    expected_keys = {
        "schema_version",
        "kind",
        "attestation_id",
        "actor_id",
        "decision",
        "plan_consent_id",
        "public_key_sha256",
        "issued_at",
        "expires_at",
        "nonce",
        "signature",
    }
    if set(value) != expected_keys:
        raise SkillMemoryError(
            "Host consent attestation has missing or unexpected fields"
        )
    if value.get("schema_version") != SCHEMA_VERSION:
        raise SkillMemoryError("Host consent attestation schema_version must be 1")
    if value.get("kind") != CONSENT_KIND or value.get("decision") != "APPROVE":
        raise SkillMemoryError("Host consent attestation does not approve this operation")
    attestation_id = _nonempty_string(
        value.get("attestation_id"),
        "attestation.attestation_id",
        maximum=128,
    )
    if not ATTESTATION_ID_RE.fullmatch(attestation_id):
        raise SkillMemoryError("attestation.attestation_id has an invalid format")
    actor_id = _nonempty_string(
        value.get("actor_id"),
        "attestation.actor_id",
        maximum=128,
    )
    if not ACTOR_ID_RE.fullmatch(actor_id):
        raise SkillMemoryError("attestation.actor_id has an invalid format")
    if value.get("plan_consent_id") != plan.get("consent_id"):
        raise SkillMemoryError("Host attestation is bound to a different plan")
    if value.get("public_key_sha256") != public_key_sha256:
        raise SkillMemoryError("Host attestation key fingerprint does not match the plan")
    nonce = _nonempty_string(value.get("nonce"), "attestation.nonce", maximum=128)
    if not NONCE_RE.fullmatch(nonce):
        raise SkillMemoryError("attestation.nonce has an invalid format")
    issued_at = _parse_utc_timestamp(value.get("issued_at"), "attestation.issued_at")
    expires_at = _parse_utc_timestamp(value.get("expires_at"), "attestation.expires_at")
    current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    if expires_at <= issued_at or expires_at - issued_at > CONSENT_MAX_LIFETIME:
        raise SkillMemoryError("Host attestation lifetime exceeds the 15-minute limit")
    if current < issued_at - timedelta(seconds=30) or current > expires_at:
        raise SkillMemoryError("Host consent attestation is not currently valid")
    signature_text = _nonempty_string(
        value.get("signature"),
        "attestation.signature",
        maximum=256,
    )
    try:
        signature = base64.b64decode(signature_text, validate=True)
    except (ValueError, base64.binascii.Error) as exc:
        raise SkillMemoryError("Host attestation signature is not valid base64") from exc
    signed = dict(value)
    signed.pop("signature")
    if not public_key.verify(signature, _canonical_json(signed)):
        raise SkillMemoryError("Host consent attestation signature is invalid")
    return {
        "attestation_id": attestation_id,
        "actor_id": actor_id,
        "issued_at": issued_at.isoformat().replace("+00:00", "Z"),
        "expires_at": expires_at.isoformat().replace("+00:00", "Z"),
        "sha256": _sha256_file(path),
        "public_key_sha256": public_key_sha256,
        "signed_record": value,
    }


def _slug(raw: str, *, maximum: int = 54) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", raw.lower()).strip("-")
    value = value[:maximum].rstrip("-")
    return value or "learned-workflow"


def _proposal_core(proposal: Mapping[str, Any]) -> dict[str, Any]:
    skill = proposal.get("skill")
    if not isinstance(skill, dict):
        raise SkillMemoryError("proposal.skill must be a mapping")
    return {
        "schema_version": proposal.get("schema_version"),
        "proposer_id": proposal.get("proposer_id"),
        "source_trace_ids": proposal.get("source_trace_ids"),
        "skill": skill,
    }


def _expected_proposal_id(proposal: Mapping[str, Any]) -> str:
    return "smp-" + _sha256_bytes(_canonical_json(_proposal_core(proposal)))[:16]


def _render_skill_markdown(skill: Mapping[str, Any]) -> bytes:
    skill_id = _validate_dynamic_id(str(skill.get("id", "")))
    description = _nonempty_string(
        skill.get("description"), "proposal.skill.description", maximum=1024
    )
    if "\n" in description or "\r" in description:
        raise SkillMemoryError("proposal.skill.description must be one line")
    body = _nonempty_string(skill.get("body"), "proposal.skill.body", maximum=65536)
    if body.lstrip().startswith("---"):
        raise SkillMemoryError("proposal.skill.body must not contain YAML front matter")
    for heading in REQUIRED_BODY_HEADINGS:
        if heading not in body:
            raise SkillMemoryError(f"proposal.skill.body is missing heading: {heading}")
    _scan_untrusted_text(description, "proposal.skill.description")
    _scan_untrusted_text(body, "proposal.skill.body")
    front_matter = yaml.safe_dump(
        {"name": skill_id, "description": description},
        sort_keys=False,
        allow_unicode=True,
    ).strip()
    normalized_body = body.replace("\r\n", "\n").replace("\r", "\n").strip()
    return f"---\n{front_matter}\n---\n\n{normalized_body}\n".encode("utf-8")


def _validate_proposal(value: Mapping[str, Any]) -> dict[str, Any]:
    proposal = copy.deepcopy(dict(value))
    if proposal.get("schema_version") != SCHEMA_VERSION:
        raise SkillMemoryError("proposal.schema_version must be 1")
    proposer_id = _nonempty_string(
        proposal.get("proposer_id"), "proposal.proposer_id", maximum=128
    )
    if not ACTOR_ID_RE.fullmatch(proposer_id):
        raise SkillMemoryError("proposal.proposer_id has an invalid format")
    trace_ids = _string_list(
        proposal.get("source_trace_ids"),
        "proposal.source_trace_ids",
        minimum=1,
        maximum=64,
        item_maximum=128,
    )
    if any(not TRACE_ID_RE.fullmatch(item) for item in trace_ids):
        raise SkillMemoryError("proposal.source_trace_ids contains an invalid id")
    skill = proposal.get("skill")
    if not isinstance(skill, dict):
        raise SkillMemoryError("proposal.skill must be a mapping")
    skill_id = _validate_dynamic_id(str(skill.get("id", "")))
    if str(skill.get("name", skill_id)).strip() != skill_id:
        raise SkillMemoryError("proposal.skill.name must equal proposal.skill.id")
    description = _nonempty_string(
        skill.get("description"), "proposal.skill.description", maximum=1024
    )
    retrieval_terms = _string_list(
        skill.get("retrieval_terms", []),
        "proposal.skill.retrieval_terms",
        minimum=1,
        maximum=32,
        item_maximum=128,
    )
    scope = _nonempty_string(skill.get("scope"), "proposal.skill.scope", maximum=4096)
    _scan_untrusted_text(scope, "proposal.skill.scope")
    skill_markdown = _render_skill_markdown(skill)
    expected_id = _expected_proposal_id(proposal)
    proposal_id = _nonempty_string(
        proposal.get("proposal_id"), "proposal.proposal_id", maximum=20
    )
    if not PROPOSAL_ID_RE.fullmatch(proposal_id) or proposal_id != expected_id:
        raise SkillMemoryError(
            f"proposal.proposal_id must equal the content-bound id {expected_id}"
        )
    proposal["proposer_id"] = proposer_id
    proposal["source_trace_ids"] = trace_ids
    proposal["skill"] = {
        "id": skill_id,
        "name": skill_id,
        "description": description,
        "retrieval_terms": retrieval_terms,
        "scope": scope,
        "body": str(skill.get("body", "")).strip(),
    }
    proposal["_skill_markdown"] = skill_markdown
    return proposal


def _draft_from_trace(trace: Mapping[str, Any], requested_skill_id: str = "") -> dict[str, Any]:
    if trace.get("schema_version") != SCHEMA_VERSION:
        raise SkillMemoryError("trace.schema_version must be 1")
    trace_id = _nonempty_string(trace.get("trace_id"), "trace.trace_id", maximum=128)
    if not TRACE_ID_RE.fullmatch(trace_id):
        raise SkillMemoryError("trace.trace_id has an invalid format")
    proposer_id = _nonempty_string(
        trace.get("proposer_id"), "trace.proposer_id", maximum=128
    )
    if not ACTOR_ID_RE.fullmatch(proposer_id):
        raise SkillMemoryError("trace.proposer_id has an invalid format")
    task_family = _nonempty_string(
        trace.get("task_family"), "trace.task_family", maximum=256
    )
    title = _nonempty_string(trace.get("title"), "trace.title", maximum=256)
    scope = _nonempty_string(trace.get("scope"), "trace.scope", maximum=4096)
    steps = _string_list(
        trace.get("steps"),
        "trace.steps",
        minimum=2,
        maximum=32,
        item_maximum=2048,
    )
    failure_boundaries = _string_list(
        trace.get("failure_boundaries"),
        "trace.failure_boundaries",
        minimum=1,
        maximum=32,
        item_maximum=2048,
    )
    outcome = trace.get("outcome")
    if not isinstance(outcome, dict):
        raise SkillMemoryError("trace.outcome must be a mapping")
    if outcome.get("status") != "VERIFIED_SUCCESS":
        raise SkillMemoryError(
            "Only VERIFIED_SUCCESS traces can produce a Skill candidate"
        )
    evidence_ids = _string_list(
        outcome.get("evidence_ids"),
        "trace.outcome.evidence_ids",
        minimum=1,
        maximum=64,
        item_maximum=128,
    )
    verification = _nonempty_string(
        outcome.get("verification"),
        "trace.outcome.verification",
        maximum=4096,
    )
    for field, text in (
        ("trace.task_family", task_family),
        ("trace.title", title),
        ("trace.scope", scope),
        ("trace.outcome.verification", verification),
    ):
        _scan_untrusted_text(text, field)
    for index, item in enumerate([*steps, *failure_boundaries]):
        _scan_untrusted_text(item, f"trace.workflow_item[{index}]")

    skill_id = (
        _validate_dynamic_id(requested_skill_id)
        if requested_skill_id
        else _validate_dynamic_id(f"dyn-{_slug(task_family)}")
    )
    terms = []
    for raw in (task_family, title):
        for term in re.findall(r"[A-Za-z0-9][A-Za-z0-9._-]{1,63}|[\u4e00-\u9fff]{2,16}", raw):
            normalized = term.lower()
            if normalized not in terms:
                terms.append(normalized)
    if not terms:
        terms = [skill_id.removeprefix("dyn-")]

    numbered_steps = "\n".join(
        f"{index}. {step}" for index, step in enumerate(steps, start=1)
    )
    rendered_failures = "\n".join(f"- {item}" for item in failure_boundaries)
    rendered_evidence = ", ".join(f"`{item}`" for item in evidence_ids)
    body = (
        f"# {title}\n\n"
        "## When to use\n\n"
        f"Use this candidate for `{task_family}` within this reviewed scope: {scope}\n\n"
        "## Procedure\n\n"
        f"{numbered_steps}\n\n"
        "## Evidence and limits\n\n"
        f"- Source trace: `{trace_id}`.\n"
        f"- Verification evidence: {rendered_evidence}.\n"
        f"- Observed verification: {verification}\n"
        "- This is a procedural candidate, not proof of scientific improvement or "
        "generalization.\n"
        "- Keep it in PILOT until a fixed-denominator baseline/challenger evaluation "
        "passes.\n\n"
        "## Failure boundaries\n\n"
        f"{rendered_failures}\n"
    )
    proposal: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "proposal_id": "",
        "proposer_id": proposer_id,
        "source_trace_ids": [trace_id],
        "skill": {
            "id": skill_id,
            "name": skill_id,
            "description": (
                f"Procedural memory candidate for {task_family}; "
                "requires evaluated promotion before active use."
            ),
            "retrieval_terms": terms[:32],
            "scope": scope,
            "body": body.strip(),
        },
    }
    proposal["proposal_id"] = _expected_proposal_id(proposal)
    return _validate_proposal(proposal)


def _empty_registry() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "store_type": STORE_TYPE,
        "consent_public_key_sha256": None,
        "next_event_sequence": 1,
        "skills": {},
        "events": [],
    }


def _version_path(skill_id: str, version: int) -> str:
    return f"skills/{skill_id}/versions/v{version:04d}/SKILL.md"


def _active_path(skill_id: str) -> str:
    return f"active/{skill_id}/SKILL.md"


def _authorization_receipt_path(sequence: int) -> str:
    return f"{AUTHORIZATION_RECEIPT_DIR}/{sequence:08d}.json"


def _plan_consent_core(plan: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: copy.deepcopy(value)
        for key, value in plan.items()
        if key not in {"consent_id", "required_confirmation", "preview"}
    }


def _authorization_receipt_bytes(
    plan: Mapping[str, Any],
    signed_attestation: Mapping[str, Any],
) -> bytes:
    payload = {
        "schema_version": SCHEMA_VERSION,
        "kind": AUTHORIZATION_RECEIPT_KIND,
        "event_sequence": plan["event_sequence"],
        "consent_id": plan["consent_id"],
        "plan_core": _plan_consent_core(plan),
        "signed_attestation": copy.deepcopy(dict(signed_attestation)),
    }
    return (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def _registry_bytes(registry: Mapping[str, Any]) -> bytes:
    return yaml.dump(
        dict(registry),
        Dumper=_NoAliasSafeDumper,
        sort_keys=False,
        allow_unicode=True,
    ).encode("utf-8")


def _audit_bytes(registry: Mapping[str, Any]) -> bytes:
    events = registry.get("events", [])
    return b"".join(_canonical_json(event) + b"\n" for event in events)


def _index_payload(registry: Mapping[str, Any]) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    skills = registry.get("skills", {})
    if isinstance(skills, dict):
        for skill_id in sorted(skills):
            record = skills[skill_id]
            if not isinstance(record, dict) or record.get("state") != "ACTIVE":
                continue
            active_version = record.get("active_version")
            version_record = (record.get("versions") or {}).get(str(active_version), {})
            entries.append(
                {
                    "id": skill_id,
                    "description": record.get("description", ""),
                    "retrieval_terms": record.get("retrieval_terms", []),
                    "version": active_version,
                    "sha256": version_record.get("sha256", ""),
                    "path": _active_path(skill_id),
                }
            )
    return {
        "schema_version": SCHEMA_VERSION,
        "authority": REGISTRY_FILE,
        "derived": True,
        "retrieval_mode": "progressive-disclosure-lexical",
        "skills": entries,
    }


def _index_bytes(registry: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(
            _index_payload(registry),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def _load_registry(root: Path) -> dict[str, Any]:
    registry_path = root / REGISTRY_FILE
    if not root.exists():
        return _empty_registry()
    if _is_link_like(root):
        raise SkillMemoryError(f"Dynamic Skill memory root is a symlink or junction: {root}")
    if not registry_path.is_file():
        non_lock_entries = [
            item for item in root.iterdir() if item.name != LOCK_FILE
        ]
        if non_lock_entries:
            raise SkillMemoryError(
                "Existing dynamic Skill memory root is not an initialized store: "
                f"{root}"
            )
        return _empty_registry()
    _reject_link_or_hardlink(registry_path, "dynamic Skill registry")
    registry = _read_yaml_mapping(registry_path, "dynamic Skill registry")
    _validate_registry_structure(registry)
    return registry


def _validate_registry_structure(registry: Mapping[str, Any]) -> None:
    if set(registry) != {
        "schema_version",
        "store_type",
        "consent_public_key_sha256",
        "next_event_sequence",
        "skills",
        "events",
    }:
        raise SkillMemoryError("registry has missing or unexpected top-level fields")
    if registry.get("schema_version") != SCHEMA_VERSION:
        raise SkillMemoryError("registry.schema_version must be 1")
    if registry.get("store_type") != STORE_TYPE:
        raise SkillMemoryError(f"registry.store_type must be {STORE_TYPE}")
    next_sequence = registry.get("next_event_sequence")
    if not isinstance(next_sequence, int) or next_sequence < 1:
        raise SkillMemoryError("registry.next_event_sequence must be a positive integer")
    skills = registry.get("skills")
    events = registry.get("events")
    if not isinstance(skills, dict) or not isinstance(events, list):
        raise SkillMemoryError("registry.skills must be a mapping and events a list")
    consent_key_sha256 = registry.get("consent_public_key_sha256")
    if consent_key_sha256 is not None and not SHA256_RE.fullmatch(
        str(consent_key_sha256)
    ):
        raise SkillMemoryError("registry consent public-key fingerprint is invalid")
    if (skills or events) and consent_key_sha256 is None:
        raise SkillMemoryError("initialized registry has no trusted consent key")
    expected_sequence = 1
    for event in events:
        if not isinstance(event, dict) or event.get("sequence") != expected_sequence:
            raise SkillMemoryError("registry.events must have contiguous sequence numbers")
        if not {
            "sequence",
            "operation",
            "skill_id",
            "authorization",
        }.issubset(event) or not set(event).issubset(
            {
                "sequence",
                "operation",
                "skill_id",
                "version",
                "proposal_id",
                "evaluation_id",
                "authorization",
            }
        ):
            raise SkillMemoryError("registry event has missing or unexpected fields")
        if event.get("operation") not in {
            "create",
            "update",
            "promote",
            "rollback",
            "deprecate",
            "delete",
        }:
            raise SkillMemoryError("registry event operation is invalid")
        _validate_dynamic_id(str(event.get("skill_id", "")))
        authorization = event.get("authorization")
        if (
            not isinstance(authorization, dict)
            or set(authorization)
            != {
                "mode",
                "public_key_sha256",
                "operation_binding_sha256",
                "receipt_path",
            }
            or authorization.get("mode") != "HOST_ED25519_ATTESTED"
            or authorization.get("public_key_sha256") != consent_key_sha256
            or not SHA256_RE.fullmatch(
                str(authorization.get("operation_binding_sha256", ""))
            )
            or authorization.get("receipt_path")
            != _authorization_receipt_path(expected_sequence)
        ):
            raise SkillMemoryError("registry event authorization binding is invalid")
        expected_sequence += 1
    if next_sequence != expected_sequence:
        raise SkillMemoryError("registry.next_event_sequence does not follow events")

    allowed_skill_states = {"PILOT", "ACTIVE", "DEPRECATED", "DELETED"}
    allowed_version_states = {"PILOT", "ACTIVE", "SUPERSEDED", "DEPRECATED"}
    for raw_id, raw_record in skills.items():
        skill_id = _validate_dynamic_id(str(raw_id))
        if not isinstance(raw_record, dict):
            raise SkillMemoryError(f"registry skill record is not a mapping: {skill_id}")
        state = raw_record.get("state")
        if state not in allowed_skill_states:
            raise SkillMemoryError(f"Invalid state for {skill_id}: {state!r}")
        if state == "DELETED":
            if set(raw_record) != {"state", "deleted_event_sequence"}:
                raise SkillMemoryError(
                    f"Deleted tombstone for {skill_id} must be content-free"
                )
            continue
        if set(raw_record) != {
            "description",
            "retrieval_terms",
            "scope",
            "state",
            "active_version",
            "versions",
        }:
            raise SkillMemoryError(
                f"registry record has missing or unexpected fields: {skill_id}"
            )
        description = _nonempty_string(
            raw_record.get("description"),
            f"registry.skills.{skill_id}.description",
            maximum=1024,
        )
        scope = _nonempty_string(
            raw_record.get("scope"),
            f"registry.skills.{skill_id}.scope",
            maximum=4096,
        )
        retrieval_terms = _string_list(
            raw_record.get("retrieval_terms"),
            f"registry.skills.{skill_id}.retrieval_terms",
            minimum=1,
            maximum=32,
            item_maximum=128,
        )
        _scan_untrusted_text(description, f"registry.skills.{skill_id}.description")
        _scan_untrusted_text(scope, f"registry.skills.{skill_id}.scope")
        for term in retrieval_terms:
            _scan_untrusted_text(term, f"registry.skills.{skill_id}.retrieval_terms")
        versions = raw_record.get("versions")
        if not isinstance(versions, dict) or not versions:
            raise SkillMemoryError(f"registry skill has no versions: {skill_id}")
        active_version = raw_record.get("active_version")
        active_count = 0
        for raw_version, version_record in versions.items():
            try:
                version = int(raw_version)
            except (TypeError, ValueError) as exc:
                raise SkillMemoryError(
                    f"Invalid version key for {skill_id}: {raw_version!r}"
                ) from exc
            if version < 1 or not isinstance(version_record, dict):
                raise SkillMemoryError(f"Invalid version record for {skill_id} v{version}")
            base_version_fields = {
                "state",
                "path",
                "sha256",
                "proposal_id",
                "proposer_id",
                "source_trace_ids",
                "description",
                "retrieval_terms",
                "scope",
            }
            evaluated_fields = {
                "evaluation_id",
                "evaluation_summary",
            }
            if not set(version_record) in (
                base_version_fields,
                base_version_fields | evaluated_fields,
            ):
                raise SkillMemoryError(
                    f"Version record has missing or unexpected fields: "
                    f"{skill_id} v{version}"
                )
            if version_record.get("state") not in allowed_version_states:
                raise SkillMemoryError(
                    f"Invalid version state for {skill_id} v{version}"
                )
            if version_record.get("state") == "ACTIVE":
                active_count += 1
            if version_record.get("path") != _version_path(skill_id, version):
                raise SkillMemoryError(f"Invalid version path for {skill_id} v{version}")
            if not SHA256_RE.fullmatch(str(version_record.get("sha256", ""))):
                raise SkillMemoryError(f"Invalid version hash for {skill_id} v{version}")
            if not PROPOSAL_ID_RE.fullmatch(
                str(version_record.get("proposal_id", ""))
            ):
                raise SkillMemoryError(
                    f"Invalid proposal id for {skill_id} v{version}"
                )
            proposer_id = str(version_record.get("proposer_id", ""))
            if not ACTOR_ID_RE.fullmatch(proposer_id):
                raise SkillMemoryError(
                    f"Invalid proposer id for {skill_id} v{version}"
                )
            source_trace_ids = _string_list(
                version_record.get("source_trace_ids"),
                f"registry.skills.{skill_id}.versions.{version}.source_trace_ids",
                minimum=1,
                maximum=64,
                item_maximum=128,
            )
            if any(not TRACE_ID_RE.fullmatch(item) for item in source_trace_ids):
                raise SkillMemoryError(
                    f"Invalid source trace id for {skill_id} v{version}"
                )
            if (
                version_record.get("description") != description
                and version_record.get("state") == "ACTIVE"
            ):
                raise SkillMemoryError(
                    f"ACTIVE version description drift: {skill_id} v{version}"
                )
            if version_record.get("state") in {"ACTIVE", "SUPERSEDED"} and not set(
                version_record
            ).issuperset(evaluated_fields):
                raise SkillMemoryError(
                    f"Evaluated version lacks evaluation summary: {skill_id} v{version}"
                )
        if state == "ACTIVE":
            if active_count != 1 or str(active_version) not in versions:
                raise SkillMemoryError(f"ACTIVE skill has invalid pointer: {skill_id}")
            if versions[str(active_version)].get("state") != "ACTIVE":
                raise SkillMemoryError(f"ACTIVE pointer is inconsistent: {skill_id}")
        elif active_version is not None or active_count:
            raise SkillMemoryError(f"Non-active skill has an active pointer: {skill_id}")


def _append_event(
    registry: dict[str, Any],
    *,
    operation: str,
    skill_id: str,
    version: int | None = None,
    proposal_id: str = "",
    evaluation_id: str = "",
) -> int:
    sequence = int(registry["next_event_sequence"])
    event: dict[str, Any] = {
        "sequence": sequence,
        "operation": operation,
        "skill_id": skill_id,
    }
    if version is not None:
        event["version"] = version
    if proposal_id:
        event["proposal_id"] = proposal_id
    if evaluation_id:
        event["evaluation_id"] = evaluation_id
    registry["events"].append(event)
    registry["next_event_sequence"] = sequence + 1
    return sequence


def _load_evaluation_artifact(
    value: Any,
    *,
    field: str,
    root: Path,
) -> tuple[dict[str, str], dict[str, str]]:
    if not isinstance(value, dict) or set(value) != {"path", "sha256"}:
        raise SkillMemoryError(f"{field} must contain only path and sha256")
    expected_hash = str(value.get("sha256", ""))
    if not SHA256_RE.fullmatch(expected_hash):
        raise SkillMemoryError(f"{field}.sha256 must be SHA-256")
    path = _resolve_source_file(str(value.get("path", "")), field, root)
    raw = _read_stable_bytes(path, field, MAX_EVALUATION_ARTIFACT_BYTES)
    actual_hash = _sha256_bytes(raw)
    if actual_hash != expected_hash:
        raise SkillMemoryError(f"{field} does not match its declared SHA-256")
    normalized = {"path": str(path), "sha256": actual_hash}
    return normalized, {str(path): actual_hash}


def _load_evaluation(
    path: Path,
    *,
    skill_id: str,
    version: int,
    proposer_id: str,
    current_active_version: int | None,
    root: Path,
    consent_public_key: _Ed25519PublicKey,
    consent_public_key_sha256: str,
) -> dict[str, Any]:
    value = _read_yaml_mapping(path, "Skill evaluation")
    expected_top_level = {
        "schema_version",
        "evaluation_id",
        "skill_id",
        "candidate_version",
        "grader_id",
        "grader_public_key_sha256",
        "grader_signature",
        "champion_version",
        "protocol",
        "case_results",
        "negative_mutations",
        "artifact_manifest_sha256",
        "fatal_vetoes",
        "verdict",
        "claim_level",
    }
    if set(value) != expected_top_level:
        raise SkillMemoryError("Skill evaluation has missing or unexpected fields")
    if value.get("schema_version") != SCHEMA_VERSION:
        raise SkillMemoryError("evaluation.schema_version must be 1")
    signature_text = _nonempty_string(
        value.get("grader_signature"),
        "evaluation.grader_signature",
        maximum=256,
    )
    try:
        signature = base64.b64decode(signature_text, validate=True)
    except (ValueError, base64.binascii.Error) as exc:
        raise SkillMemoryError(
            "evaluation.grader_signature is not valid base64"
        ) from exc
    signed_evaluation = dict(value)
    signed_evaluation.pop("grader_signature")
    try:
        signed_bytes = _canonical_json(signed_evaluation)
    except (TypeError, ValueError) as exc:
        raise SkillMemoryError(
            "Skill evaluation contains non-canonical value types"
        ) from exc
    if not consent_public_key.verify(signature, signed_bytes):
        raise SkillMemoryError("Skill evaluation grader signature is invalid")
    evaluation_id = _nonempty_string(
        value.get("evaluation_id"), "evaluation.evaluation_id", maximum=128
    )
    if not EVALUATION_ID_RE.fullmatch(evaluation_id):
        raise SkillMemoryError("evaluation.evaluation_id has an invalid format")
    if value.get("skill_id") != skill_id or value.get("candidate_version") != version:
        raise SkillMemoryError("evaluation target does not match the requested candidate")
    grader_id = _nonempty_string(
        value.get("grader_id"), "evaluation.grader_id", maximum=128
    )
    if not ACTOR_ID_RE.fullmatch(grader_id) or grader_id == proposer_id:
        raise SkillMemoryError(
            "evaluation.grader_id must be valid and independent from proposer_id"
        )
    if value.get("grader_public_key_sha256") != consent_public_key_sha256:
        raise SkillMemoryError(
            "Evaluation grader key must match the store's trusted host key"
        )
    protocol = value.get("protocol")
    required_protocol_fields = {
        "model_id",
        "runtime_artifact",
        "toolset_artifact",
        "source_snapshot_artifact",
        "scoring_policy_artifact",
        "budget_id",
    }
    if not isinstance(protocol, dict) or set(protocol) != required_protocol_fields:
        raise SkillMemoryError("evaluation.protocol has missing or unexpected fields")
    model_id = _nonempty_string(
        protocol.get("model_id"),
        "evaluation.protocol.model_id",
        maximum=256,
    )
    budget_id = _nonempty_string(
        protocol.get("budget_id"),
        "evaluation.protocol.budget_id",
        maximum=256,
    )
    artifact_sources: dict[str, str] = {}
    normalized_protocol: dict[str, Any] = {
        "model_id": model_id,
        "budget_id": budget_id,
    }
    for field in (
        "runtime_artifact",
        "toolset_artifact",
        "source_snapshot_artifact",
        "scoring_policy_artifact",
    ):
        artifact, sources = _load_evaluation_artifact(
            protocol.get(field),
            field=f"evaluation.protocol.{field}",
            root=root,
        )
        normalized_protocol[field] = artifact
        artifact_sources.update(sources)

    raw_cases = value.get("case_results")
    if not isinstance(raw_cases, list) or not 2 <= len(raw_cases) <= 512:
        raise SkillMemoryError("evaluation.case_results requires 2 to 512 cases")
    case_results: list[dict[str, Any]] = []
    case_ids: list[str] = []
    expected_case_fields = {
        "case_id",
        "no_skill_result",
        "champion_result",
        "candidate_result",
        "no_skill_artifact",
        "champion_artifact",
        "candidate_artifact",
    }
    for index, raw_case in enumerate(raw_cases):
        if not isinstance(raw_case, dict) or set(raw_case) != expected_case_fields:
            raise SkillMemoryError(
                f"evaluation.case_results[{index}] has missing or unexpected fields"
            )
        case_id = _nonempty_string(
            raw_case.get("case_id"),
            f"evaluation.case_results[{index}].case_id",
            maximum=128,
        )
        if not TRACE_ID_RE.fullmatch(case_id) or case_id in case_ids:
            raise SkillMemoryError("evaluation case IDs must be valid and unique")
        case_ids.append(case_id)
        normalized_case = {"case_id": case_id}
        for arm in ("no_skill", "champion", "candidate"):
            result = raw_case.get(f"{arm}_result")
            if result not in {"PASS", "FAIL"}:
                raise SkillMemoryError(
                    f"evaluation.case_results[{index}].{arm}_result "
                    "must be PASS or FAIL"
                )
            artifact, sources = _load_evaluation_artifact(
                raw_case.get(f"{arm}_artifact"),
                field=f"evaluation.case_results[{index}].{arm}_artifact",
                root=root,
            )
            normalized_case[f"{arm}_result"] = result
            normalized_case[f"{arm}_artifact"] = artifact
            artifact_sources.update(sources)
        case_results.append(normalized_case)

    champion_version = value.get("champion_version")
    if current_active_version is None:
        if champion_version is not None or any(
            case["champion_result"] != case["no_skill_result"]
            or case["champion_artifact"] != case["no_skill_artifact"]
            for case in case_results
        ):
            raise SkillMemoryError(
                "First promotion requires champion_version=null and a byte-bound "
                "CHAMPION arm identical to NO_SKILL"
            )
    elif champion_version != current_active_version:
        raise SkillMemoryError(
            "evaluation.champion_version must match the current ACTIVE version"
        )
    no_skill_passes = sum(
        case["no_skill_result"] == "PASS" for case in case_results
    )
    champion_passes = sum(
        case["champion_result"] == "PASS" for case in case_results
    )
    candidate_passes = sum(
        case["candidate_result"] == "PASS" for case in case_results
    )
    if candidate_passes <= max(no_skill_passes, champion_passes):
        raise SkillMemoryError(
            "candidate_passes must exceed both NO_SKILL and CHAMPION "
            "on the same holdout"
        )
    regressions = sum(
        case["champion_result"] == "PASS"
        and case["candidate_result"] == "FAIL"
        for case in case_results
    )
    if regressions:
        raise SkillMemoryError("Candidate has a regression against CHAMPION")

    raw_mutations = value.get("negative_mutations")
    if not isinstance(raw_mutations, list) or not raw_mutations:
        raise SkillMemoryError("evaluation.negative_mutations must not be empty")
    mutation_ids: set[str] = set()
    negative_mutations: list[dict[str, Any]] = []
    for index, raw_mutation in enumerate(raw_mutations):
        if not isinstance(raw_mutation, dict) or set(raw_mutation) != {
            "mutation_id",
            "detected",
            "artifact",
        }:
            raise SkillMemoryError(
                f"evaluation.negative_mutations[{index}] has invalid fields"
            )
        mutation_id = _nonempty_string(
            raw_mutation.get("mutation_id"),
            f"evaluation.negative_mutations[{index}].mutation_id",
            maximum=128,
        )
        artifact, sources = _load_evaluation_artifact(
            raw_mutation.get("artifact"),
            field=f"evaluation.negative_mutations[{index}].artifact",
            root=root,
        )
        if (
            not TRACE_ID_RE.fullmatch(mutation_id)
            or mutation_id in mutation_ids
            or raw_mutation.get("detected") is not True
        ):
            raise SkillMemoryError(
                "All negative mutations require unique IDs and detection=true"
            )
        mutation_ids.add(mutation_id)
        artifact_sources.update(sources)
        negative_mutations.append(
            {
                "mutation_id": mutation_id,
                "detected": True,
                "artifact": artifact,
            }
        )
    fatal_vetoes = value.get("fatal_vetoes")
    if fatal_vetoes != []:
        raise SkillMemoryError("evaluation.fatal_vetoes must be an empty list")
    artifact_core = {
        "protocol": normalized_protocol,
        "case_results": case_results,
        "negative_mutations": negative_mutations,
    }
    expected_manifest_hash = _sha256_bytes(_canonical_json(artifact_core))
    if value.get("artifact_manifest_sha256") != expected_manifest_hash:
        raise SkillMemoryError(
            "evaluation.artifact_manifest_sha256 is not content-bound to artifacts"
        )
    if value.get("verdict") != "PROMOTE":
        raise SkillMemoryError("evaluation.verdict must be PROMOTE")
    if value.get("claim_level") != "BEHAVIORAL":
        raise SkillMemoryError(
            "evaluation.claim_level must be BEHAVIORAL; scientific improvement is separate"
        )
    return {
        "schema_version": SCHEMA_VERSION,
        "evaluation_id": evaluation_id,
        "skill_id": skill_id,
        "candidate_version": version,
        "grader_id": grader_id,
        "grader_public_key_sha256": consent_public_key_sha256,
        "protocol": normalized_protocol,
        "holdout_case_ids": case_ids,
        "no_skill_passes": no_skill_passes,
        "champion_version": champion_version,
        "champion_passes": champion_passes,
        "candidate_passes": candidate_passes,
        "negative_mutation_total": len(negative_mutations),
        "negative_mutation_detected": len(negative_mutations),
        "regressions": 0,
        "artifact_manifest_sha256": expected_manifest_hash,
        "artifact_sources": artifact_sources,
        "verdict": "PROMOTE",
        "claim_level": "BEHAVIORAL",
    }


def _existing_file_bytes(
    root: Path, relative: str, extra_writes: Mapping[str, bytes]
) -> bytes:
    if relative in extra_writes:
        return extra_writes[relative]
    path = _safe_child(root, relative)
    if not path.is_file():
        raise SkillMemoryError(f"Required immutable Skill version is missing: {path}")
    _reject_link_or_hardlink(path, "immutable Skill version")
    return path.read_bytes()


def _directory_identity(root: Path, relative: str) -> dict[str, Any]:
    target = _validate_tree_for_delete(root, relative)
    if not target.exists():
        raise SkillMemoryError(f"Planned delete target disappeared: {target}")
    target_stat = target.stat()
    parent_stat = target.parent.stat()
    entries: list[dict[str, Any]] = []
    for path in sorted(target.rglob("*"), key=lambda item: item.as_posix()):
        relative_entry = path.relative_to(target).as_posix()
        if path.is_dir():
            entries.append({"path": relative_entry, "type": "directory"})
        elif path.is_file():
            entries.append(
                {
                    "path": relative_entry,
                    "type": "file",
                    "bytes": path.stat().st_size,
                    "sha256": _sha256_file(path),
                }
            )
        else:
            raise SkillMemoryError(f"Unsupported delete-tree entry: {path}")
    return {
        "target_device": int(target_stat.st_dev),
        "target_inode": int(target_stat.st_ino),
        "parent_device": int(parent_stat.st_dev),
        "parent_inode": int(parent_stat.st_ino),
        "tree_sha256": _sha256_bytes(_canonical_json(entries)),
    }


def _simulate_operation(
    *,
    operation: str,
    root: Path,
    proposal_path: Path | None = None,
    skill_id: str = "",
    version: int | None = None,
    evaluation_path: Path | None = None,
    consent_public_key: _Ed25519PublicKey,
    consent_public_key_sha256: str,
    allow_lock: bool = False,
) -> dict[str, Any]:
    if not SHA256_RE.fullmatch(consent_public_key_sha256):
        raise SkillMemoryError("Trusted consent public-key fingerprint is invalid")
    if _lock_path(root).exists() and not allow_lock:
        raise SkillMemoryError(
            f"Dynamic Skill memory store is locked: {_lock_path(root)}"
        )
    prepared_path = root / PREPARED_FILE
    if prepared_path.exists():
        raise SkillMemoryError(
            f"PREPARED journal requires recovery before a new plan: {prepared_path}"
        )
    registry = _load_registry(root)
    before_registry = copy.deepcopy(registry)
    before_hash = (
        _sha256_file(root / REGISTRY_FILE)
        if (root / REGISTRY_FILE).is_file()
        else "ABSENT"
    )
    skills: dict[str, Any] = registry["skills"]
    extra_writes: dict[str, bytes] = {}
    delete_paths: list[str] = []
    source_hashes: dict[str, str] = {}
    preview = ""
    target_version: int | None = version
    configured_consent_key = registry.get("consent_public_key_sha256")
    if (
        configured_consent_key is not None
        and configured_consent_key != consent_public_key_sha256
    ):
        raise SkillMemoryError(
            "Trusted consent key does not match the key pinned by this store"
        )
    if configured_consent_key is not None:
        stored_key = _load_store_consent_public_key(
            root,
            str(configured_consent_key),
        )
        if stored_key.raw != consent_public_key.raw:
            raise SkillMemoryError(
                "Provided consent key does not match the stored trusted key"
            )

    proposal: dict[str, Any] | None = None
    if operation in {"create", "update"}:
        if proposal_path is None:
            raise SkillMemoryError(f"{operation} requires --proposal")
        proposal = _validate_proposal(
            _read_yaml_mapping(proposal_path, "Skill proposal")
        )
        source_hashes[str(proposal_path)] = _sha256_file(proposal_path)
        proposal_skill_id = str(proposal["skill"]["id"])
        if skill_id and _validate_dynamic_id(skill_id) != proposal_skill_id:
            raise SkillMemoryError(
                "--skill-id does not match proposal.skill.id"
            )
        skill_id = proposal_skill_id
        preview = proposal["_skill_markdown"].decode("utf-8")
    else:
        skill_id = _validate_dynamic_id(skill_id)

    record = skills.get(skill_id)

    if operation == "create":
        if record is not None:
            raise SkillMemoryError(
                f"Dynamic Skill id already exists or is tombstoned: {skill_id}"
            )
        assert proposal is not None
        registry["consent_public_key_sha256"] = consent_public_key_sha256
        target_version = 1
        version_relative = _version_path(skill_id, target_version)
        skill_markdown = proposal["_skill_markdown"]
        version_record = {
            "state": "PILOT",
            "path": version_relative,
            "sha256": _sha256_bytes(skill_markdown),
            "proposal_id": proposal["proposal_id"],
            "proposer_id": proposal["proposer_id"],
            "source_trace_ids": proposal["source_trace_ids"],
            "description": proposal["skill"]["description"],
            "retrieval_terms": proposal["skill"]["retrieval_terms"],
            "scope": proposal["skill"]["scope"],
        }
        skills[skill_id] = {
            "description": proposal["skill"]["description"],
            "retrieval_terms": proposal["skill"]["retrieval_terms"],
            "scope": proposal["skill"]["scope"],
            "state": "PILOT",
            "active_version": None,
            "versions": {"1": version_record},
        }
        extra_writes[version_relative] = skill_markdown
        extra_writes[
            TRUSTED_CONSENT_PUBLIC_KEY_FILE
        ] = consent_public_key.public_pem()
        _append_event(
            registry,
            operation="create",
            skill_id=skill_id,
            version=target_version,
            proposal_id=proposal["proposal_id"],
        )

    elif operation == "update":
        if not isinstance(record, dict) or record.get("state") == "DELETED":
            raise SkillMemoryError(
                f"Cannot update missing/deleted dynamic Skill: {skill_id}"
            )
        assert proposal is not None
        existing_versions = [int(item) for item in record["versions"]]
        target_version = max(existing_versions) + 1
        version_relative = _version_path(skill_id, target_version)
        skill_markdown = proposal["_skill_markdown"]
        record["versions"][str(target_version)] = {
            "state": "PILOT",
            "path": version_relative,
            "sha256": _sha256_bytes(skill_markdown),
            "proposal_id": proposal["proposal_id"],
            "proposer_id": proposal["proposer_id"],
            "source_trace_ids": proposal["source_trace_ids"],
            "description": proposal["skill"]["description"],
            "retrieval_terms": proposal["skill"]["retrieval_terms"],
            "scope": proposal["skill"]["scope"],
        }
        if record.get("active_version") is None:
            record["description"] = proposal["skill"]["description"]
            record["retrieval_terms"] = proposal["skill"]["retrieval_terms"]
            record["scope"] = proposal["skill"]["scope"]
            record["state"] = "PILOT"
        extra_writes[version_relative] = skill_markdown
        _append_event(
            registry,
            operation="update",
            skill_id=skill_id,
            version=target_version,
            proposal_id=proposal["proposal_id"],
        )

    elif operation == "promote":
        if not isinstance(record, dict) or record.get("state") == "DELETED":
            raise SkillMemoryError(
                f"Cannot promote missing/deleted dynamic Skill: {skill_id}"
            )
        if not isinstance(target_version, int) or target_version < 1:
            raise SkillMemoryError("promote requires a positive --version")
        version_record = (record.get("versions") or {}).get(str(target_version))
        if not isinstance(version_record, dict) or version_record.get("state") != "PILOT":
            raise SkillMemoryError(
                "promote target must be an existing PILOT version"
            )
        if evaluation_path is None:
            raise SkillMemoryError("promote requires --evaluation")
        evaluation = _load_evaluation(
            evaluation_path,
            skill_id=skill_id,
            version=target_version,
            proposer_id=str(version_record.get("proposer_id", "")),
            current_active_version=record.get("active_version"),
            root=root,
            consent_public_key=consent_public_key,
            consent_public_key_sha256=consent_public_key_sha256,
        )
        source_hashes[str(evaluation_path)] = _sha256_file(evaluation_path)
        source_hashes.update(evaluation["artifact_sources"])
        active_version = record.get("active_version")
        if active_version is not None:
            record["versions"][str(active_version)]["state"] = "SUPERSEDED"
        version_record["state"] = "ACTIVE"
        version_record["evaluation_id"] = evaluation["evaluation_id"]
        version_record["evaluation_summary"] = {
            "grader_id": evaluation["grader_id"],
            "grader_public_key_sha256": evaluation[
                "grader_public_key_sha256"
            ],
            "protocol": evaluation["protocol"],
            "holdout_case_ids": evaluation["holdout_case_ids"],
            "no_skill_passes": evaluation["no_skill_passes"],
            "champion_version": evaluation["champion_version"],
            "champion_passes": evaluation["champion_passes"],
            "candidate_passes": evaluation["candidate_passes"],
            "negative_mutation_total": evaluation[
                "negative_mutation_total"
            ],
            "regressions": 0,
            "artifact_manifest_sha256": evaluation[
                "artifact_manifest_sha256"
            ],
            "artifact_sources": evaluation["artifact_sources"],
            "claim_level": "BEHAVIORAL",
        }
        record["state"] = "ACTIVE"
        record["active_version"] = target_version
        record["description"] = version_record["description"]
        record["retrieval_terms"] = version_record["retrieval_terms"]
        record["scope"] = version_record["scope"]
        version_bytes = _existing_file_bytes(root, version_record["path"], extra_writes)
        if _sha256_bytes(version_bytes) != version_record["sha256"]:
            raise SkillMemoryError("Candidate version hash does not match registry")
        extra_writes[_active_path(skill_id)] = version_bytes
        preview = version_bytes.decode("utf-8")
        _append_event(
            registry,
            operation="promote",
            skill_id=skill_id,
            version=target_version,
            evaluation_id=evaluation["evaluation_id"],
        )

    elif operation == "rollback":
        if not isinstance(record, dict) or record.get("state") != "ACTIVE":
            raise SkillMemoryError("rollback requires an ACTIVE dynamic Skill")
        if not isinstance(target_version, int) or target_version < 1:
            raise SkillMemoryError("rollback requires a positive --version")
        current_version = int(record["active_version"])
        if target_version == current_version:
            raise SkillMemoryError("rollback target is already active")
        version_record = (record.get("versions") or {}).get(str(target_version))
        if not isinstance(version_record, dict) or version_record.get("state") not in {
            "SUPERSEDED",
            "DEPRECATED",
        }:
            raise SkillMemoryError(
                "rollback target must be an existing SUPERSEDED or DEPRECATED version"
            )
        record["versions"][str(current_version)]["state"] = "SUPERSEDED"
        version_record["state"] = "ACTIVE"
        record["active_version"] = target_version
        record["state"] = "ACTIVE"
        record["description"] = version_record["description"]
        record["retrieval_terms"] = version_record["retrieval_terms"]
        record["scope"] = version_record["scope"]
        version_bytes = _existing_file_bytes(root, version_record["path"], extra_writes)
        if _sha256_bytes(version_bytes) != version_record["sha256"]:
            raise SkillMemoryError("Rollback version hash does not match registry")
        extra_writes[_active_path(skill_id)] = version_bytes
        preview = version_bytes.decode("utf-8")
        _append_event(
            registry,
            operation="rollback",
            skill_id=skill_id,
            version=target_version,
        )

    elif operation == "deprecate":
        if not isinstance(record, dict) or record.get("state") == "DELETED":
            raise SkillMemoryError(f"Cannot deprecate missing/deleted Skill: {skill_id}")
        for version_record in record["versions"].values():
            if version_record.get("state") in {"ACTIVE", "PILOT"}:
                version_record["state"] = "DEPRECATED"
        record["state"] = "DEPRECATED"
        record["active_version"] = None
        active_directory = f"active/{skill_id}"
        active_target = _safe_child(root, active_directory)
        if active_target.exists():
            _validate_tree_for_delete(root, active_directory)
            delete_paths.append(active_directory)
        _append_event(registry, operation="deprecate", skill_id=skill_id)

    elif operation == "delete":
        if not isinstance(record, dict) or record.get("state") == "DELETED":
            raise SkillMemoryError(f"Cannot delete missing/already-deleted Skill: {skill_id}")
        payload_directory = f"skills/{skill_id}"
        active_directory = f"active/{skill_id}"
        for relative in (payload_directory, active_directory):
            target = _safe_child(root, relative)
            if target.exists():
                _validate_tree_for_delete(root, relative)
                delete_paths.append(relative)
        sequence = _append_event(registry, operation="delete", skill_id=skill_id)
        skills[skill_id] = {
            "state": "DELETED",
            "deleted_event_sequence": sequence,
        }

    else:
        raise SkillMemoryError(f"Unsupported dynamic Skill memory operation: {operation}")

    if registry.get("consent_public_key_sha256") is None:
        raise SkillMemoryError("Dynamic Skill memory store has no pinned consent key")
    operation_binding = {
        "schema_version": SCHEMA_VERSION,
        "operation": operation,
        "root": str(root),
        "root_identity": _root_identity(root),
        "skill_id": skill_id,
        "version": target_version,
        "before_registry_sha256": before_hash,
        "source_sha256": source_hashes,
        "public_key_sha256": consent_public_key_sha256,
    }
    event = registry["events"][-1]
    event_sequence = int(event["sequence"])
    authorization_receipt_relative = _authorization_receipt_path(event_sequence)
    registry["events"][-1]["authorization"] = {
        "mode": "HOST_ED25519_ATTESTED",
        "public_key_sha256": consent_public_key_sha256,
        "operation_binding_sha256": _sha256_bytes(
            _canonical_json(operation_binding)
        ),
        "receipt_path": authorization_receipt_relative,
    }
    event_sha256 = _sha256_bytes(_canonical_json(registry["events"][-1]))
    _validate_registry_structure(registry)
    extra_writes[AUDIT_FILE] = _audit_bytes(registry)
    extra_writes[INDEX_FILE] = _index_bytes(registry)
    extra_writes[REGISTRY_FILE] = _registry_bytes(registry)
    after_hash = _sha256_bytes(extra_writes[REGISTRY_FILE])

    write_records = [
        {
            "relative_path": relative,
            "absolute_path": str(_safe_child(root, relative)),
            "sha256": _sha256_bytes(data),
            "bytes": len(data),
        }
        for relative, data in sorted(extra_writes.items())
    ]
    delete_records = [
        {
            "relative_path": relative,
            "absolute_path": str(_safe_child(root, relative)),
            "quarantine_relative_path": (
                f"{QUARANTINE_DIR}/"
                f"{index:04d}-{_sha256_bytes(relative.encode('utf-8'))[:16]}"
            ),
            "identity": _directory_identity(root, relative),
        }
        for index, relative in enumerate(sorted(set(delete_paths)), start=1)
    ]
    plan_core: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "operation": operation,
        "root": str(root),
        "root_identity": _root_identity(root),
        "skill_id": skill_id,
        "version": target_version,
        "before_registry_sha256": before_hash,
        "after_registry_sha256": after_hash,
        "source_sha256": source_hashes,
        "consent_public_key_sha256": consent_public_key_sha256,
        "writes": write_records,
        "deletes": delete_records,
        "prepared_journal": str(_safe_child(root, PREPARED_FILE)),
        "event_sequence": event_sequence,
        "event_sha256": event_sha256,
        "authorization_receipt": {
            "relative_path": authorization_receipt_relative,
            "absolute_path": str(
                _safe_child(root, authorization_receipt_relative)
            ),
        },
    }
    consent_id = "zyr-smc-" + _sha256_bytes(_canonical_json(plan_core))[:24]
    plan = dict(plan_core)
    plan["consent_id"] = consent_id
    plan["required_confirmation"] = f"APPROVE {consent_id}"
    plan["preview"] = preview
    return {
        "plan": plan,
        "before_registry": before_registry,
        "after_registry": registry,
        "writes": extra_writes,
        "deletes": sorted(set(delete_paths)),
    }


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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


def _validate_tree_for_delete(root: Path, relative: str) -> Path:
    target = _safe_child(root, relative)
    if not target.exists():
        return target
    if target == root or not _path_is_within(target, root):
        raise SkillMemoryError(f"Refusing unsafe recursive delete target: {target}")
    if _is_link_like(target) or _has_symlink_component(target):
        raise SkillMemoryError(
            f"Refusing recursive delete through symlink or junction: {target}"
        )
    if not target.is_dir():
        raise SkillMemoryError(f"Recursive delete target is not a directory: {target}")
    for child in target.rglob("*"):
        if _is_link_like(child):
            raise SkillMemoryError(
                f"Refusing recursive delete containing symlink or junction: {child}"
            )
        if child.is_file() and child.stat().st_nlink > 1:
            raise SkillMemoryError(
                f"Refusing recursive delete containing hardlink: {child}"
            )
    return target


def _remove_tree(root: Path, relative: str) -> None:
    target = _validate_tree_for_delete(root, relative)
    if not target.exists():
        return
    shutil.rmtree(target)


def _stage_deletes(
    root: Path,
    delete_records: Sequence[Mapping[str, Any]],
    lock_lease: _StoreLockLease,
) -> None:
    for record in delete_records:
        relative = str(record["relative_path"])
        quarantine_relative = str(record["quarantine_relative_path"])
        expected_identity = record["identity"]
        _assert_lock_owner(lock_lease)
        actual_identity = _directory_identity(root, relative)
        if actual_identity != expected_identity:
            raise SkillMemoryError(
                f"Delete target identity changed before quarantine: {relative}"
            )
        target = _safe_child(root, relative)
        quarantine = _safe_child(root, quarantine_relative)
        if quarantine.exists():
            raise SkillMemoryError(
                f"Delete quarantine target already exists: {quarantine}"
            )
        quarantine.parent.mkdir(parents=True, exist_ok=True)
        _assert_lock_owner(lock_lease)
        os.replace(target, quarantine)
        moved_identity = _directory_identity(root, quarantine_relative)
        current_parent = target.parent.stat()
        if (
            moved_identity["target_device"] != expected_identity["target_device"]
            or moved_identity["target_inode"] != expected_identity["target_inode"]
            or moved_identity["tree_sha256"] != expected_identity["tree_sha256"]
            or current_parent.st_dev != expected_identity["parent_device"]
            or current_parent.st_ino != expected_identity["parent_inode"]
        ):
            raise SkillMemoryError(
                f"Delete target or parent changed during quarantine move: {relative}"
            )
        _assert_lock_owner(lock_lease)


def _clear_quarantine(
    root: Path,
    delete_records: Sequence[Mapping[str, Any]],
    lock_lease: _StoreLockLease,
) -> None:
    for record in delete_records:
        _assert_lock_owner(lock_lease)
        quarantine_relative = str(record["quarantine_relative_path"])
        quarantine = _safe_child(root, quarantine_relative)
        if not quarantine.exists():
            continue
        expected_identity = record["identity"]
        actual_identity = _directory_identity(root, quarantine_relative)
        if (
            actual_identity["target_device"] != expected_identity["target_device"]
            or actual_identity["target_inode"] != expected_identity["target_inode"]
            or actual_identity["tree_sha256"] != expected_identity["tree_sha256"]
        ):
            raise SkillMemoryError(
                f"Quarantined delete content changed: {quarantine_relative}"
            )
        _remove_tree(root, quarantine_relative)
    quarantine_root = _safe_child(root, QUARANTINE_DIR)
    try:
        quarantine_root.rmdir()
    except OSError:
        pass


def _assert_lock_owner(lease: _StoreLockLease) -> None:
    descriptor_stat = os.fstat(lease.descriptor)
    if (
        descriptor_stat.st_dev != lease.device
        or descriptor_stat.st_ino != lease.inode
    ):
        raise SkillMemoryError("Dynamic Skill memory lock descriptor identity changed")
    try:
        path_stat = lease.path.stat(follow_symlinks=False)
        raw = lease.path.read_text(encoding="ascii")
    except (OSError, UnicodeError) as exc:
        raise SkillMemoryError(
            "Dynamic Skill memory lock was removed or replaced during apply"
        ) from exc
    if (
        path_stat.st_dev != lease.device
        or path_stat.st_ino != lease.inode
        or raw != lease.token
    ):
        raise SkillMemoryError(
            "Dynamic Skill memory lock ownership changed during apply"
        )


@contextmanager
def _exclusive_store_lock(root: Path) -> Iterator[_StoreLockLease]:
    lock_path = _lock_path(root)
    descriptor: int | None = None
    lease: _StoreLockLease | None = None
    try:
        descriptor = os.open(
            str(lock_path),
            os.O_CREAT | os.O_EXCL | os.O_WRONLY,
            0o600,
        )
        token = f"{os.getpid()}:{secrets.token_urlsafe(32)}"
        os.write(descriptor, token.encode("ascii"))
        os.fsync(descriptor)
        stat = os.fstat(descriptor)
        lease = _StoreLockLease(
            path=lock_path,
            descriptor=descriptor,
            token=token,
            device=int(stat.st_dev),
            inode=int(stat.st_ino),
        )
        _assert_lock_owner(lease)
        yield lease
        _assert_lock_owner(lease)
    except FileExistsError as exc:
        raise SkillMemoryError(
            f"Dynamic Skill memory store is locked; inspect before retrying: {lock_path}"
        ) from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if lease is not None:
            try:
                path_stat = lock_path.stat(follow_symlinks=False)
                raw = lock_path.read_text(encoding="ascii")
            except (OSError, UnicodeError):
                pass
            else:
                if (
                    path_stat.st_dev == lease.device
                    and path_stat.st_ino == lease.inode
                    and raw == lease.token
                ):
                    lock_path.unlink(missing_ok=True)


def _prepared_bytes(
    plan: Mapping[str, Any],
    transaction_root_identity: Mapping[str, Any],
    writes: Mapping[str, bytes],
) -> bytes:
    payload = {
        "schema_version": SCHEMA_VERSION,
        "status": "PREPARED",
        "consent_id": plan["consent_id"],
        "operation": plan["operation"],
        "skill_id": plan["skill_id"],
        "version": plan.get("version"),
        "root": plan["root"],
        "transaction_root_identity": dict(transaction_root_identity),
        "before_registry_sha256": plan["before_registry_sha256"],
        "after_registry_sha256": plan["after_registry_sha256"],
        "consent_public_key_sha256": plan["consent_public_key_sha256"],
        "writes": [
            {
                "relative_path": relative,
                "sha256": _sha256_bytes(data),
            }
            for relative, data in sorted(writes.items())
        ],
        "deletes": plan["deletes"],
    }
    return (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def _load_prepared_journal(root: Path) -> dict[str, Any]:
    path = _safe_child(root, PREPARED_FILE)
    value = _read_json_mapping(
        path,
        "Skill-memory PREPARED journal",
        MAX_YAML_BYTES,
    )
    expected_keys = {
        "schema_version",
        "status",
        "consent_id",
        "operation",
        "skill_id",
        "version",
        "root",
        "transaction_root_identity",
        "before_registry_sha256",
        "after_registry_sha256",
        "consent_public_key_sha256",
        "writes",
        "deletes",
    }
    if set(value) != expected_keys:
        raise SkillMemoryError("PREPARED journal has missing or unexpected fields")
    if value.get("schema_version") != SCHEMA_VERSION or value.get("status") != "PREPARED":
        raise SkillMemoryError("PREPARED journal schema or status is invalid")
    if value.get("root") != str(root) or value.get(
        "transaction_root_identity"
    ) != _root_identity(root):
        raise SkillMemoryError("PREPARED journal root identity does not match")
    for field in ("before_registry_sha256", "after_registry_sha256"):
        raw_hash = value.get(field)
        if raw_hash != "ABSENT" and not SHA256_RE.fullmatch(str(raw_hash)):
            raise SkillMemoryError(f"PREPARED journal {field} is invalid")
    if not SHA256_RE.fullmatch(str(value.get("consent_public_key_sha256", ""))):
        raise SkillMemoryError("PREPARED journal consent key is invalid")
    if not isinstance(value.get("writes"), list) or not isinstance(
        value.get("deletes"), list
    ):
        raise SkillMemoryError("PREPARED journal writes/deletes must be lists")
    for item in value["writes"]:
        if (
            not isinstance(item, dict)
            or set(item) != {"relative_path", "sha256"}
            or not SHA256_RE.fullmatch(str(item.get("sha256", "")))
        ):
            raise SkillMemoryError("PREPARED journal has an invalid write record")
        _safe_child(root, str(item["relative_path"]))
    for item in value["deletes"]:
        if (
            not isinstance(item, dict)
            or set(item)
            != {
                "relative_path",
                "absolute_path",
                "quarantine_relative_path",
                "identity",
            }
            or not isinstance(item.get("identity"), dict)
        ):
            raise SkillMemoryError("PREPARED journal has an invalid delete record")
        _safe_child(root, str(item["relative_path"]))
        _safe_child(root, str(item["quarantine_relative_path"]))
    return value


def _current_registry_hash(root: Path) -> str:
    path = root / REGISTRY_FILE
    return _sha256_file(path) if path.is_file() else "ABSENT"


def _recovery_plan_payload(
    *,
    raw_root: str,
    trusted_consent_public_key: str,
    allow_lock: bool = False,
) -> dict[str, Any]:
    root = _resolve_root(raw_root)
    if _lock_path(root).exists() and not allow_lock:
        raise SkillMemoryError(f"Dynamic Skill memory store is locked: {_lock_path(root)}")
    public_key_path, _, public_key_sha256 = _load_consent_public_key(
        trusted_consent_public_key,
        root,
    )
    journal_path = _safe_child(root, PREPARED_FILE)
    journal = _load_prepared_journal(root)
    if journal["consent_public_key_sha256"] != public_key_sha256:
        raise SkillMemoryError(
            "Recovery key does not match the key bound by PREPARED"
        )
    current_hash = _current_registry_hash(root)
    if current_hash == journal["before_registry_sha256"]:
        recovery_mode = "ROLLBACK"
    elif current_hash == journal["after_registry_sha256"]:
        recovery_mode = "ROLL_FORWARD"
    else:
        raise SkillMemoryError(
            "Registry matches neither PREPARED before-state nor after-state"
        )
    core = {
        "schema_version": SCHEMA_VERSION,
        "operation": "recover",
        "recovery_mode": recovery_mode,
        "root": str(root),
        "root_identity": _root_identity(root),
        "journal_sha256": _sha256_file(journal_path),
        "current_registry_sha256": current_hash,
        "original_operation": journal["operation"],
        "skill_id": journal["skill_id"],
        "version": journal.get("version"),
        "consent_public_key_sha256": public_key_sha256,
        "trusted_consent_public_key_path": str(public_key_path),
        "quarantine": [
            {
                "relative_path": item["relative_path"],
                "quarantine_relative_path": item[
                    "quarantine_relative_path"
                ],
            }
            for item in journal["deletes"]
        ],
        "writes": [],
        "deletes": [],
        "prepared_journal": str(journal_path),
    }
    consent_id = "zyr-smc-" + _sha256_bytes(_canonical_json(core))[:24]
    plan = dict(core)
    plan["consent_id"] = consent_id
    plan["required_confirmation"] = f"APPROVE {consent_id}"
    plan["preview"] = (
        f"Recover interrupted {journal['operation']} by {recovery_mode}."
    )
    return {"plan": plan, "journal": journal}


def _registry_for_recovery(root: Path) -> dict[str, Any] | None:
    path = root / REGISTRY_FILE
    if not path.is_file():
        return None
    registry = _read_yaml_mapping(path, "dynamic Skill registry")
    _validate_registry_structure(registry)
    return registry


def _remove_file_and_empty_parents(root: Path, relative: str) -> None:
    path = _safe_child(root, relative)
    if not path.exists():
        return
    if not path.is_file() or _is_link_like(path) or path.stat().st_nlink > 1:
        raise SkillMemoryError(f"Recovery refuses unsafe planned file: {path}")
    path.unlink()
    parent = path.parent
    while parent != root:
        try:
            parent.rmdir()
        except OSError:
            break
        parent = parent.parent


def _restore_quarantine(
    root: Path,
    delete_records: Sequence[Mapping[str, Any]],
    lock_lease: _StoreLockLease,
) -> None:
    for record in reversed(list(delete_records)):
        _assert_lock_owner(lock_lease)
        relative = str(record["relative_path"])
        quarantine_relative = str(record["quarantine_relative_path"])
        target = _safe_child(root, relative)
        quarantine = _safe_child(root, quarantine_relative)
        if not quarantine.exists():
            if target.exists():
                continue
            raise SkillMemoryError(
                f"Neither original nor quarantined delete target exists: {relative}"
            )
        if target.exists():
            raise SkillMemoryError(
                f"Cannot restore quarantine over an existing path: {target}"
            )
        expected_identity = record["identity"]
        actual_identity = _directory_identity(root, quarantine_relative)
        if (
            actual_identity["target_device"] != expected_identity["target_device"]
            or actual_identity["target_inode"] != expected_identity["target_inode"]
            or actual_identity["tree_sha256"] != expected_identity["tree_sha256"]
        ):
            raise SkillMemoryError(
                f"Quarantined content changed before rollback: {quarantine_relative}"
            )
        target.parent.mkdir(parents=True, exist_ok=True)
        os.replace(quarantine, target)
        restored = _directory_identity(root, relative)
        if (
            restored["target_device"] != expected_identity["target_device"]
            or restored["target_inode"] != expected_identity["target_inode"]
            or restored["tree_sha256"] != expected_identity["tree_sha256"]
        ):
            raise SkillMemoryError(f"Restored delete target failed identity check: {relative}")


def _rebuild_derived_state(
    root: Path,
    registry: Mapping[str, Any],
    lock_lease: _StoreLockLease,
) -> None:
    _assert_lock_owner(lock_lease)
    _atomic_write(_safe_child(root, AUDIT_FILE), _audit_bytes(registry))
    _atomic_write(_safe_child(root, INDEX_FILE), _index_bytes(registry))
    expected_active: set[str] = set()
    for skill_id, record in registry["skills"].items():
        if record.get("state") != "ACTIVE":
            continue
        relative = _active_path(skill_id)
        expected_active.add(relative)
        version_record = record["versions"][str(record["active_version"])]
        version_path = _safe_child(root, str(version_record["path"]))
        if _sha256_file(version_path) != version_record["sha256"]:
            raise SkillMemoryError(
                f"Cannot rebuild ACTIVE projection from a drifted version: {skill_id}"
            )
        _atomic_write(_safe_child(root, relative), version_path.read_bytes())
    active_root = root / "active"
    if active_root.is_dir():
        for path in sorted(active_root.rglob("*"), reverse=True):
            if path.is_file():
                relative = path.relative_to(root).as_posix()
                if relative not in expected_active:
                    _remove_file_and_empty_parents(root, relative)


def _recover_prepared(
    root: Path,
    recovery: Mapping[str, Any],
    lock_lease: _StoreLockLease,
) -> str:
    plan = recovery["plan"]
    journal = recovery["journal"]
    if _root_identity(root) != plan["root_identity"]:
        raise SkillMemoryError("Store root changed after recovery planning")
    if _sha256_file(_safe_child(root, PREPARED_FILE)) != plan["journal_sha256"]:
        raise SkillMemoryError("PREPARED journal changed after recovery planning")
    if _current_registry_hash(root) != plan["current_registry_sha256"]:
        raise SkillMemoryError("Registry changed after recovery planning")
    mode = str(plan["recovery_mode"])
    if mode == "ROLLBACK":
        _restore_quarantine(root, journal["deletes"], lock_lease)
        registry = _registry_for_recovery(root)
        referenced_files: set[str] = set()
        if registry is not None:
            referenced_files.update(
                {
                    REGISTRY_FILE,
                    AUDIT_FILE,
                    INDEX_FILE,
                    TRUSTED_CONSENT_PUBLIC_KEY_FILE,
                }
            )
            referenced_files.update(
                str(event["authorization"]["receipt_path"])
                for event in registry["events"]
            )
            for skill_id, record in registry["skills"].items():
                if record.get("state") == "DELETED":
                    continue
                for version_record in record["versions"].values():
                    referenced_files.add(str(version_record["path"]))
                if record.get("state") == "ACTIVE":
                    referenced_files.add(_active_path(skill_id))
        for write in journal["writes"]:
            relative = str(write["relative_path"])
            if relative in referenced_files or relative == REGISTRY_FILE:
                continue
            path = _safe_child(root, relative)
            if path.is_file():
                if _sha256_file(path) != write["sha256"]:
                    raise SkillMemoryError(
                        f"Recovery refuses changed uncommitted write: {relative}"
                    )
                _remove_file_and_empty_parents(root, relative)
        if registry is None:
            for relative in (AUDIT_FILE, INDEX_FILE):
                path = _safe_child(root, relative)
                if path.is_file():
                    _remove_file_and_empty_parents(root, relative)
        else:
            _rebuild_derived_state(root, registry, lock_lease)
    elif mode == "ROLL_FORWARD":
        registry = _registry_for_recovery(root)
        if registry is None:
            raise SkillMemoryError("Committed recovery state has no registry")
        for write in journal["writes"]:
            path = _safe_child(root, str(write["relative_path"]))
            if not path.is_file() or _sha256_file(path) != write["sha256"]:
                raise SkillMemoryError(
                    f"Committed write is missing or drifted: {write['relative_path']}"
                )
        _clear_quarantine(root, journal["deletes"], lock_lease)
    else:
        raise SkillMemoryError(f"Unsupported recovery mode: {mode}")

    prepared_path = _safe_child(root, PREPARED_FILE)
    prepared_path.unlink()
    for directory in (
        _safe_child(root, QUARANTINE_DIR),
        prepared_path.parent,
    ):
        try:
            directory.rmdir()
        except OSError:
            pass
    if _registry_for_recovery(root) is not None:
        errors = verify_skill_memory_store(root, allow_lock=True)
        if errors:
            raise SkillMemoryError(
                "Recovered store failed verification:\n- " + "\n- ".join(errors)
            )
    return mode


def _apply_simulation(
    root: Path,
    simulation: Mapping[str, Any],
    *,
    lock_lease: _StoreLockLease,
    signed_attestation: Mapping[str, Any],
) -> Path:
    plan = simulation["plan"]
    _assert_lock_owner(lock_lease)
    if _root_identity(root) != plan["root_identity"]:
        raise SkillMemoryError("Dynamic Skill memory root identity changed after planning")
    current_registry_hash = (
        _sha256_file(root / REGISTRY_FILE)
        if (root / REGISTRY_FILE).is_file()
        else "ABSENT"
    )
    if current_registry_hash != plan["before_registry_sha256"]:
        raise SkillMemoryError("Dynamic Skill registry changed after planning")
    root.mkdir(parents=True, exist_ok=True)
    writes = dict(simulation["writes"])
    receipt_relative = str(
        plan["authorization_receipt"]["relative_path"]
    )
    writes[receipt_relative] = _authorization_receipt_bytes(
        plan,
        signed_attestation,
    )
    prepared_path = _safe_child(root, PREPARED_FILE)
    _atomic_write(
        prepared_path,
        _prepared_bytes(plan, _root_identity(root), writes),
    )
    _stage_deletes(root, plan["deletes"], lock_lease)
    for relative in sorted(writes):
        if relative == REGISTRY_FILE:
            continue
        _assert_lock_owner(lock_lease)
        _atomic_write(_safe_child(root, relative), writes[relative])
    _assert_lock_owner(lock_lease)
    _atomic_write(_safe_child(root, REGISTRY_FILE), writes[REGISTRY_FILE])
    _assert_lock_owner(lock_lease)
    return prepared_path


def _plan_payload(
    *,
    operation: str,
    raw_root: str,
    proposal: str = "",
    skill_id: str = "",
    version: int | None = None,
    evaluation: str = "",
    trusted_consent_public_key: str,
    allow_lock: bool = False,
) -> dict[str, Any]:
    root = _resolve_root(raw_root)
    _, consent_public_key, consent_public_key_sha256 = _load_consent_public_key(
        trusted_consent_public_key,
        root,
    )
    proposal_path = (
        _resolve_source_file(proposal, "Skill proposal", root) if proposal else None
    )
    evaluation_path = (
        _resolve_source_file(evaluation, "Skill evaluation", root)
        if evaluation
        else None
    )
    return _simulate_operation(
        operation=operation,
        root=root,
        proposal_path=proposal_path,
        skill_id=skill_id,
        version=version,
        evaluation_path=evaluation_path,
        consent_public_key=consent_public_key,
        consent_public_key_sha256=consent_public_key_sha256,
        allow_lock=allow_lock,
    )


def run_skill_memory_draft(
    trace_path: str,
    *,
    skill_id: str = "",
    json_output: bool = False,
) -> int:
    """Render a content-bound proposal from one verified trace without writing."""
    try:
        path = Path(trace_path).expanduser().resolve()
        proposal = _draft_from_trace(
            _read_yaml_mapping(path, "verified trace"),
            requested_skill_id=skill_id,
        )
        proposal.pop("_skill_markdown", None)
    except (SkillMemoryError, OSError, UnicodeError) as exc:
        print(f"Skill memory draft failed: {exc}", file=sys.stderr)
        return 1
    if json_output:
        print(json.dumps(proposal, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(
            yaml.dump(
                proposal,
                Dumper=_NoAliasSafeDumper,
                sort_keys=False,
                allow_unicode=True,
            ).rstrip()
        )
    return 0


def _print_plan(plan: Mapping[str, Any]) -> None:
    print("SKILL_MEMORY_PLAN: READ_ONLY")
    print(f"OPERATION: {plan['operation']}")
    print(f"ROOT: {plan['root']}")
    print(f"CONSENT_PUBLIC_KEY_SHA256: {plan['consent_public_key_sha256']}")
    print(f"SKILL_ID: {plan['skill_id']}")
    if plan.get("version") is not None:
        print(f"VERSION: {plan['version']}")
    for item in plan["writes"]:
        print(f"WRITE: {item['absolute_path']} sha256={item['sha256']}")
    for item in plan["deletes"]:
        print(f"DELETE: {item['absolute_path']}")
    print(
        "WRITE_SIGNED_AUTHORIZATION_RECEIPT: "
        f"{plan['authorization_receipt']['absolute_path']}"
    )
    print(f"PREPARED_JOURNAL: {plan['prepared_journal']}")
    if plan.get("preview"):
        print("PREVIEW_BEGIN")
        print(str(plan["preview"]).rstrip())
        print("PREVIEW_END")
    print(f"CONSENT_ID: {plan['consent_id']}")
    print(f"REQUIRED_CONFIRMATION: {plan['required_confirmation']}")
    print("HOST_ATTESTATION_REQUIRED: signed Ed25519 JSON bound to CONSENT_ID")
    print("No files written.")


def _deletion_receipt(
    *,
    root: Path,
    skill_id: str,
    delete_records: Sequence[Mapping[str, Any]],
    operation_consent_id: str,
    attestation: Mapping[str, Any],
) -> dict[str, Any]:
    registry = _load_registry(root)
    tombstone = registry["skills"].get(skill_id)
    if not isinstance(tombstone, dict) or tombstone.get("state") != "DELETED":
        raise SkillMemoryError("Deletion receipt requires a DELETED tombstone")
    core = {
        "schema_version": SCHEMA_VERSION,
        "skill_id": skill_id,
        "local_store_root": str(root),
        "deleted_event_sequence": tombstone["deleted_event_sequence"],
        "operation_consent_id": operation_consent_id,
        "host_attestation_id": attestation["attestation_id"],
        "verified_absent": [
            str(item["absolute_path"]) for item in delete_records
        ],
        "local_store_status": "LOCAL_STORE_DELETION_VERIFIED",
        "global_deletion_status": "DELETION_UNVERIFIED",
        "uninspected_copy_classes": [
            "exports",
            "backups",
            "git_history",
            "cloud_sync",
            "third_party_indexes",
        ],
    }
    return {
        **core,
        "receipt_id": "zyr-smdr-"
        + _sha256_bytes(_canonical_json(core))[:24],
    }


def run_skill_memory_plan(
    operation: str,
    raw_root: str,
    *,
    proposal: str = "",
    skill_id: str = "",
    version: int | None = None,
    evaluation: str = "",
    trusted_consent_public_key: str,
    json_output: bool = False,
) -> int:
    """Compute an exact read-only mutation plan and content-bound consent ID."""
    try:
        if operation == "recover":
            simulation = _recovery_plan_payload(
                raw_root=raw_root,
                trusted_consent_public_key=trusted_consent_public_key,
            )
        else:
            simulation = _plan_payload(
                operation=operation,
                raw_root=raw_root,
                proposal=proposal,
                skill_id=skill_id,
                version=version,
                evaluation=evaluation,
                trusted_consent_public_key=trusted_consent_public_key,
            )
    except (SkillMemoryError, OSError, UnicodeError, yaml.YAMLError) as exc:
        print(f"Skill memory plan failed: {exc}", file=sys.stderr)
        return 1
    plan = simulation["plan"]
    if json_output:
        print(json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        _print_plan(plan)
    return 0


def _run_skill_memory_recover_apply(
    raw_root: str,
    *,
    consent_id: str,
    consent_attestation: str,
    trusted_consent_public_key: str,
    json_output: bool,
) -> int:
    try:
        initial = _recovery_plan_payload(
            raw_root=raw_root,
            trusted_consent_public_key=trusted_consent_public_key,
        )
        plan = initial["plan"]
        if consent_id != plan["consent_id"]:
            raise SkillMemoryError(
                f"Consent mismatch: expected exact plan id {plan['consent_id']}"
            )
        root = Path(str(plan["root"]))
        _, public_key, public_key_sha256 = _load_consent_public_key(
            trusted_consent_public_key,
            root,
        )
        attestation = _verify_host_attestation(
            plan=plan,
            root=root,
            raw_attestation=consent_attestation,
            public_key=public_key,
            public_key_sha256=public_key_sha256,
        )
        with _exclusive_store_lock(root) as lock_lease:
            locked = _recovery_plan_payload(
                raw_root=raw_root,
                trusted_consent_public_key=trusted_consent_public_key,
                allow_lock=True,
            )
            if locked["plan"]["consent_id"] != consent_id:
                raise SkillMemoryError(
                    "Store changed after recovery planning; generate a new plan"
                )
            recovery_mode = _recover_prepared(root, locked, lock_lease)
            _assert_lock_owner(lock_lease)
            deletion_receipt = (
                _deletion_receipt(
                    root=root,
                    skill_id=str(plan["skill_id"]),
                    delete_records=initial["journal"]["deletes"],
                    operation_consent_id=initial["journal"]["consent_id"],
                    attestation=attestation,
                )
                if plan["original_operation"] == "delete"
                and recovery_mode == "ROLL_FORWARD"
                else None
            )
    except (SkillMemoryError, OSError, UnicodeError, yaml.YAMLError) as exc:
        print(f"Skill memory recovery failed: {exc}", file=sys.stderr)
        return 1
    payload = {
        "status": "RECOVERED_AND_VERIFIED",
        "operation": "recover",
        "recovery_mode": recovery_mode,
        "root": str(root),
        "original_operation": plan["original_operation"],
        "skill_id": plan["skill_id"],
        "consent_id": consent_id,
        "host_attestation": attestation,
    }
    if deletion_receipt is not None:
        payload["deletion_receipt"] = deletion_receipt
    if json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        for key, value in payload.items():
            print(f"{key.upper()}: {value}")
    return 0


def run_skill_memory_apply(
    operation: str,
    raw_root: str,
    *,
    consent_id: str,
    consent_attestation: str,
    trusted_consent_public_key: str,
    proposal: str = "",
    skill_id: str = "",
    version: int | None = None,
    evaluation: str = "",
    json_output: bool = False,
) -> int:
    """Apply a mutation only when the exact current plan matches consent_id."""
    if operation == "recover":
        return _run_skill_memory_recover_apply(
            raw_root,
            consent_id=consent_id,
            consent_attestation=consent_attestation,
            trusted_consent_public_key=trusted_consent_public_key,
            json_output=json_output,
        )
    try:
        initial = _plan_payload(
            operation=operation,
            raw_root=raw_root,
            proposal=proposal,
            skill_id=skill_id,
            version=version,
            evaluation=evaluation,
            trusted_consent_public_key=trusted_consent_public_key,
        )
        expected = str(initial["plan"]["consent_id"])
        if consent_id != expected:
            raise SkillMemoryError(
                f"Consent mismatch: expected exact plan id {expected}"
            )
        root = Path(str(initial["plan"]["root"]))
        _, consent_public_key, consent_public_key_sha256 = _load_consent_public_key(
            trusted_consent_public_key,
            root,
        )
        attestation = _verify_host_attestation(
            plan=initial["plan"],
            root=root,
            raw_attestation=consent_attestation,
            public_key=consent_public_key,
            public_key_sha256=consent_public_key_sha256,
        )
        with _exclusive_store_lock(root) as lock_lease:
            locked = _plan_payload(
                operation=operation,
                raw_root=raw_root,
                proposal=proposal,
                skill_id=skill_id,
                version=version,
                evaluation=evaluation,
                trusted_consent_public_key=trusted_consent_public_key,
                allow_lock=True,
            )
            if locked["plan"]["consent_id"] != consent_id:
                raise SkillMemoryError(
                    "Store or source changed after planning; generate a new plan and consent"
                )
            _assert_lock_owner(lock_lease)
            prepared_path = _apply_simulation(
                root,
                locked,
                lock_lease=lock_lease,
                signed_attestation=attestation["signed_record"],
            )
            errors = verify_skill_memory_store(
                root,
                allow_lock=True,
                allow_prepared=True,
            )
            if errors:
                raise SkillMemoryError(
                    "Post-apply verification failed:\n- " + "\n- ".join(errors)
                )
            _clear_quarantine(root, locked["plan"]["deletes"], lock_lease)
            _assert_lock_owner(lock_lease)
            prepared_path.unlink()
            try:
                prepared_path.parent.rmdir()
            except OSError:
                pass
            errors = verify_skill_memory_store(root, allow_lock=True)
            if errors:
                raise SkillMemoryError(
                    "Final post-journal verification failed:\n- "
                    + "\n- ".join(errors)
                )
            _assert_lock_owner(lock_lease)
            plan = locked["plan"]
            deletion_receipt = (
                _deletion_receipt(
                    root=root,
                    skill_id=str(plan["skill_id"]),
                    delete_records=plan["deletes"],
                    operation_consent_id=consent_id,
                    attestation=attestation,
                )
                if operation == "delete"
                else None
            )
    except (SkillMemoryError, OSError, UnicodeError, yaml.YAMLError) as exc:
        print(f"Skill memory apply failed: {exc}", file=sys.stderr)
        return 1
    payload = {
        "status": "APPLIED_AND_VERIFIED",
        "operation": operation,
        "root": plan["root"],
        "skill_id": plan["skill_id"],
        "version": plan.get("version"),
        "consent_id": consent_id,
        "host_attestation": attestation,
    }
    if deletion_receipt is not None:
        payload["deletion_receipt"] = deletion_receipt
    if json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        for key, value in payload.items():
            if value is not None:
                print(f"{key.upper()}: {value}")
    return 0


def _verify_historical_attestation(
    value: Mapping[str, Any],
    *,
    consent_id: str,
    public_key: _Ed25519PublicKey,
    public_key_sha256: str,
) -> tuple[str, str]:
    expected_keys = {
        "schema_version",
        "kind",
        "attestation_id",
        "actor_id",
        "decision",
        "plan_consent_id",
        "public_key_sha256",
        "issued_at",
        "expires_at",
        "nonce",
        "signature",
    }
    if set(value) != expected_keys:
        raise SkillMemoryError(
            "Persisted host attestation has missing or unexpected fields"
        )
    if (
        value.get("schema_version") != SCHEMA_VERSION
        or value.get("kind") != CONSENT_KIND
        or value.get("decision") != "APPROVE"
        or value.get("plan_consent_id") != consent_id
        or value.get("public_key_sha256") != public_key_sha256
    ):
        raise SkillMemoryError(
            "Persisted host attestation is not bound to this authorized plan"
        )
    attestation_id = _nonempty_string(
        value.get("attestation_id"),
        "persisted_attestation.attestation_id",
        maximum=128,
    )
    actor_id = _nonempty_string(
        value.get("actor_id"),
        "persisted_attestation.actor_id",
        maximum=128,
    )
    nonce = _nonempty_string(
        value.get("nonce"),
        "persisted_attestation.nonce",
        maximum=128,
    )
    if not ATTESTATION_ID_RE.fullmatch(attestation_id):
        raise SkillMemoryError("Persisted attestation id has an invalid format")
    if not ACTOR_ID_RE.fullmatch(actor_id):
        raise SkillMemoryError("Persisted attestation actor id has an invalid format")
    if not NONCE_RE.fullmatch(nonce):
        raise SkillMemoryError("Persisted attestation nonce has an invalid format")
    issued_at = _parse_utc_timestamp(
        value.get("issued_at"),
        "persisted_attestation.issued_at",
    )
    expires_at = _parse_utc_timestamp(
        value.get("expires_at"),
        "persisted_attestation.expires_at",
    )
    if expires_at <= issued_at or expires_at - issued_at > CONSENT_MAX_LIFETIME:
        raise SkillMemoryError(
            "Persisted attestation lifetime exceeds the 15-minute limit"
        )
    signature_text = _nonempty_string(
        value.get("signature"),
        "persisted_attestation.signature",
        maximum=256,
    )
    try:
        signature = base64.b64decode(signature_text, validate=True)
    except (ValueError, base64.binascii.Error) as exc:
        raise SkillMemoryError(
            "Persisted attestation signature is not valid base64"
        ) from exc
    signed = dict(value)
    signed.pop("signature")
    if not public_key.verify(signature, _canonical_json(signed)):
        raise SkillMemoryError("Persisted host attestation signature is invalid")
    return attestation_id, nonce


def _verify_authorization_receipts(
    root: Path,
    registry: Mapping[str, Any],
) -> set[str]:
    events = registry.get("events")
    if not isinstance(events, list) or not events:
        return set()
    public_key_sha256 = str(registry.get("consent_public_key_sha256", ""))
    public_key = _load_store_consent_public_key(root, public_key_sha256)
    expected_files = {TRUSTED_CONSENT_PUBLIC_KEY_FILE}
    seen_attestation_ids: set[str] = set()
    seen_nonces: set[str] = set()
    current_registry_sha256 = _sha256_bytes(_registry_bytes(registry))
    expected_plan_keys = {
        "schema_version",
        "operation",
        "root",
        "root_identity",
        "skill_id",
        "version",
        "before_registry_sha256",
        "after_registry_sha256",
        "source_sha256",
        "consent_public_key_sha256",
        "writes",
        "deletes",
        "prepared_journal",
        "event_sequence",
        "event_sha256",
        "authorization_receipt",
    }
    for event in events:
        sequence = int(event["sequence"])
        authorization = event["authorization"]
        receipt_relative = str(authorization["receipt_path"])
        if receipt_relative != _authorization_receipt_path(sequence):
            raise SkillMemoryError(
                f"Authorization receipt path is not deterministic: event {sequence}"
            )
        expected_files.add(receipt_relative)
        receipt_path = _safe_child(root, receipt_relative)
        receipt = _read_json_mapping(
            receipt_path,
            f"authorization receipt {sequence}",
            MAX_AUTHORIZATION_RECEIPT_BYTES,
        )
        if set(receipt) != {
            "schema_version",
            "kind",
            "event_sequence",
            "consent_id",
            "plan_core",
            "signed_attestation",
        }:
            raise SkillMemoryError(
                f"Authorization receipt {sequence} has invalid fields"
            )
        if (
            receipt.get("schema_version") != SCHEMA_VERSION
            or receipt.get("kind") != AUTHORIZATION_RECEIPT_KIND
            or receipt.get("event_sequence") != sequence
        ):
            raise SkillMemoryError(
                f"Authorization receipt {sequence} has invalid identity"
            )
        plan_core = receipt.get("plan_core")
        if not isinstance(plan_core, dict) or set(plan_core) != expected_plan_keys:
            raise SkillMemoryError(
                f"Authorization receipt {sequence} has invalid plan fields"
            )
        consent_id = "zyr-smc-" + _sha256_bytes(
            _canonical_json(plan_core)
        )[:24]
        if receipt.get("consent_id") != consent_id:
            raise SkillMemoryError(
                f"Authorization receipt {sequence} consent binding is invalid"
            )
        if (
            plan_core.get("schema_version") != SCHEMA_VERSION
            or plan_core.get("operation") != event.get("operation")
            or plan_core.get("root") != str(root)
            or plan_core.get("skill_id") != event.get("skill_id")
            or plan_core.get("version") != event.get("version")
            or plan_core.get("event_sequence") != sequence
            or plan_core.get("consent_public_key_sha256")
            != public_key_sha256
        ):
            raise SkillMemoryError(
                f"Authorization receipt {sequence} plan does not match event"
            )
        expected_receipt_record = {
            "relative_path": receipt_relative,
            "absolute_path": str(receipt_path),
        }
        if plan_core.get("authorization_receipt") != expected_receipt_record:
            raise SkillMemoryError(
                f"Authorization receipt {sequence} path binding is invalid"
            )
        if plan_core.get("event_sha256") != _sha256_bytes(
            _canonical_json(event)
        ):
            raise SkillMemoryError(
                f"Authorization receipt {sequence} event binding is invalid"
            )
        operation_binding = {
            "schema_version": SCHEMA_VERSION,
            "operation": plan_core["operation"],
            "root": plan_core["root"],
            "root_identity": plan_core["root_identity"],
            "skill_id": plan_core["skill_id"],
            "version": plan_core["version"],
            "before_registry_sha256": plan_core[
                "before_registry_sha256"
            ],
            "source_sha256": plan_core["source_sha256"],
            "public_key_sha256": public_key_sha256,
        }
        if authorization.get(
            "operation_binding_sha256"
        ) != _sha256_bytes(_canonical_json(operation_binding)):
            raise SkillMemoryError(
                f"Authorization receipt {sequence} operation binding is invalid"
            )
        signed_attestation = receipt.get("signed_attestation")
        if not isinstance(signed_attestation, dict):
            raise SkillMemoryError(
                f"Authorization receipt {sequence} lacks a signed attestation"
            )
        attestation_id, nonce = _verify_historical_attestation(
            signed_attestation,
            consent_id=consent_id,
            public_key=public_key,
            public_key_sha256=public_key_sha256,
        )
        if attestation_id in seen_attestation_ids or nonce in seen_nonces:
            raise SkillMemoryError(
                f"Authorization receipt {sequence} reuses an attestation id or nonce"
            )
        seen_attestation_ids.add(attestation_id)
        seen_nonces.add(nonce)
    latest_receipt = _read_json_mapping(
        _safe_child(
            root,
            str(events[-1]["authorization"]["receipt_path"]),
        ),
        "latest authorization receipt",
        MAX_AUTHORIZATION_RECEIPT_BYTES,
    )
    latest_plan = latest_receipt["plan_core"]
    if latest_plan.get("after_registry_sha256") != current_registry_sha256:
        raise SkillMemoryError(
            "Latest signed authorization does not bind the current registry"
        )
    return expected_files


def verify_skill_memory_store(
    root: Path,
    *,
    allow_lock: bool = False,
    allow_prepared: bool = False,
) -> list[str]:
    """Return structural errors without changing the store."""
    errors: list[str] = []
    try:
        if not root.is_dir():
            return [f"store root is missing: {root}"]
        if (root / LOCK_FILE).exists() and not allow_lock:
            errors.append(f"store lock is present: {root / LOCK_FILE}")
        if _safe_child(root, PREPARED_FILE).exists() and not allow_prepared:
            errors.append(f"prepared journal is present: {_safe_child(root, PREPARED_FILE)}")
        entry_count = 0
        observed_files: set[str] = set()
        for path in root.rglob("*"):
            entry_count += 1
            if entry_count > 4096:
                errors.append("dynamic Skill memory store exceeds 4096 entries")
                break
            if _is_link_like(path):
                errors.append(f"symlink or junction is forbidden in store: {path}")
            elif path.is_file() and path.stat().st_nlink > 1:
                errors.append(f"hardlink is forbidden in store: {path}")
            if path.is_file():
                observed_files.add(path.relative_to(root).as_posix())
        registry = _load_registry(root)
        authorization_files = _verify_authorization_receipts(root, registry)
        expected_registry = _registry_bytes(registry)
        registry_path = root / REGISTRY_FILE
        if registry_path.read_bytes() != expected_registry:
            errors.append("registry.yaml is not in canonical deterministic form")
        expected_audit = _audit_bytes(registry)
        audit_path = _safe_child(root, AUDIT_FILE)
        if not audit_path.is_file() or audit_path.read_bytes() != expected_audit:
            errors.append("audit/events.jsonl is missing or drifted")
        expected_index = _index_bytes(registry)
        index_path = _safe_child(root, INDEX_FILE)
        if not index_path.is_file() or index_path.read_bytes() != expected_index:
            errors.append("index/skill_catalog.json is missing or drifted")

        expected_skill_dirs: set[str] = set()
        expected_active_dirs: set[str] = set()
        expected_files = {
            REGISTRY_FILE,
            AUDIT_FILE,
            INDEX_FILE,
        }
        expected_files.update(authorization_files)
        if allow_lock and (root / LOCK_FILE).is_file():
            expected_files.add(LOCK_FILE)
        if allow_prepared and _safe_child(root, PREPARED_FILE).is_file():
            expected_files.add(PREPARED_FILE)
            expected_files.update(
                relative
                for relative in observed_files
                if relative.startswith("journal/quarantine/")
            )
        for skill_id, record in registry["skills"].items():
            if record.get("state") == "DELETED":
                if _safe_child(root, f"skills/{skill_id}").exists():
                    errors.append(f"deleted Skill payload remains: {skill_id}")
                if _safe_child(root, f"active/{skill_id}").exists():
                    errors.append(f"deleted active projection remains: {skill_id}")
                continue
            expected_skill_dirs.add(skill_id)
            for raw_version, version_record in record["versions"].items():
                expected_files.add(str(version_record["path"]))
                path = _safe_child(root, str(version_record["path"]))
                if not path.is_file():
                    errors.append(f"missing immutable version: {version_record['path']}")
                    continue
                actual = _sha256_file(path)
                if actual != version_record["sha256"]:
                    errors.append(
                        f"version hash mismatch: {skill_id} v{raw_version}"
                    )
            if record.get("state") == "ACTIVE":
                expected_active_dirs.add(skill_id)
                expected_files.add(_active_path(skill_id))
                active_path = _safe_child(root, _active_path(skill_id))
                version_record = record["versions"][str(record["active_version"])]
                version_path = _safe_child(root, version_record["path"])
                if not active_path.is_file() or active_path.read_bytes() != version_path.read_bytes():
                    errors.append(f"active projection drift: {skill_id}")
            elif _safe_child(root, f"active/{skill_id}").exists():
                errors.append(f"non-active Skill has active projection: {skill_id}")

        skills_root = root / "skills"
        if skills_root.is_dir():
            observed = {
                item.name
                for item in skills_root.iterdir()
                if item.is_dir() and not item.is_symlink()
            }
            for orphan in sorted(observed - expected_skill_dirs):
                errors.append(f"orphan Skill payload directory: {orphan}")
        active_root = root / "active"
        if active_root.is_dir():
            observed = {
                item.name
                for item in active_root.iterdir()
                if item.is_dir() and not item.is_symlink()
            }
            for orphan in sorted(observed - expected_active_dirs):
                errors.append(f"orphan active projection directory: {orphan}")
        for unexpected in sorted(observed_files - expected_files):
            errors.append(f"unexpected file in Markdown-only store: {unexpected}")
    except (SkillMemoryError, OSError, UnicodeError, yaml.YAMLError) as exc:
        errors.append(str(exc))
    return errors


def run_skill_memory_verify(raw_root: str, *, json_output: bool = False) -> int:
    """Verify registry, immutable payloads, active projections, audit, and index."""
    try:
        root = _resolve_root(raw_root)
        errors = verify_skill_memory_store(root)
    except SkillMemoryError as exc:
        errors = [str(exc)]
        root = Path(raw_root).expanduser().resolve(strict=False)
    payload = {
        "status": "PASS" if not errors else "FAIL",
        "root": str(root),
        "errors": errors,
    }
    if json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"SKILL_MEMORY_VERIFY: {payload['status']}")
        print(f"ROOT: {payload['root']}")
        for error in errors:
            print(f"ERROR: {error}")
    return 0 if not errors else 1


def _public_skill_record(skill_id: str, record: Mapping[str, Any]) -> dict[str, Any]:
    if record.get("state") == "DELETED":
        return {
            "id": skill_id,
            "state": "DELETED",
            "deleted_event_sequence": record.get("deleted_event_sequence"),
        }
    return {
        "id": skill_id,
        "description": record.get("description", ""),
        "state": record.get("state"),
        "active_version": record.get("active_version"),
        "versions": [
            {
                "version": int(raw_version),
                "state": version_record.get("state"),
                "sha256": version_record.get("sha256"),
            }
            for raw_version, version_record in sorted(
                (record.get("versions") or {}).items(),
                key=lambda item: int(item[0]),
            )
        ],
    }


def run_skill_memory_list(
    raw_root: str,
    *,
    include_deleted: bool = False,
    json_output: bool = False,
) -> int:
    """List registry metadata without loading Skill bodies."""
    try:
        root = _resolve_root(raw_root)
        registry = _load_registry(root)
        records = [
            _public_skill_record(skill_id, registry["skills"][skill_id])
            for skill_id in sorted(registry["skills"])
            if include_deleted or registry["skills"][skill_id].get("state") != "DELETED"
        ]
    except (SkillMemoryError, OSError, UnicodeError, yaml.YAMLError) as exc:
        print(f"Skill memory list failed: {exc}", file=sys.stderr)
        return 1
    payload = {"root": str(root), "skills": records}
    if json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"ROOT: {root}")
        if not records:
            print("No dynamic Skills.")
        for record in records:
            print(
                f"SKILL: {record['id']} state={record['state']} "
                f"active_version={record.get('active_version')}"
            )
    return 0


def _retrieval_terms(text: str) -> set[str]:
    lowered = text.lower()
    terms = set(re.findall(r"[a-z0-9][a-z0-9._-]{1,63}", lowered))
    cjk_runs = re.findall(r"[\u4e00-\u9fff]{2,64}", lowered)
    for run in cjk_runs:
        terms.add(run)
        terms.update(run[index : index + 2] for index in range(len(run) - 1))
    return terms


def run_skill_memory_search(
    raw_root: str,
    query: str,
    *,
    topk: int = 5,
    json_output: bool = False,
) -> int:
    """Search ACTIVE metadata lexically, then return progressive-disclosure paths."""
    try:
        root = _resolve_root(raw_root)
        integrity_errors = verify_skill_memory_store(root)
        if integrity_errors:
            raise SkillMemoryError(
                "ACTIVE retrieval integrity check failed:\n- "
                + "\n- ".join(integrity_errors)
            )
        registry = _load_registry(root)
        query_text = _nonempty_string(query, "query", maximum=4096)
        query_terms = _retrieval_terms(query_text)
        scored: list[dict[str, Any]] = []
        for skill_id, record in registry["skills"].items():
            if record.get("state") != "ACTIVE":
                continue
            haystack = " ".join(
                [
                    skill_id,
                    str(record.get("description", "")),
                    *[str(item) for item in record.get("retrieval_terms", [])],
                ]
            )
            matched = sorted(query_terms & _retrieval_terms(haystack))
            if matched:
                active_path = _safe_child(root, _active_path(skill_id))
                version_record = record["versions"][str(record["active_version"])]
                version_path = _safe_child(root, str(version_record["path"]))
                if (
                    _sha256_file(version_path) != version_record["sha256"]
                    or active_path.read_bytes() != version_path.read_bytes()
                ):
                    raise SkillMemoryError(
                        f"ACTIVE Skill changed during retrieval: {skill_id}"
                    )
                scored.append(
                    {
                        "id": skill_id,
                        "score": len(matched),
                        "matched_terms": matched,
                        "path": str(active_path),
                        "version": record.get("active_version"),
                    }
                )
        scored.sort(key=lambda item: (-item["score"], item["id"]))
        results = scored[: max(1, topk)]
    except (SkillMemoryError, OSError, UnicodeError, yaml.YAMLError) as exc:
        print(f"Skill memory search failed: {exc}", file=sys.stderr)
        return 1
    payload = {
        "root": str(root),
        "query": query,
        "retrieval_mode": "progressive-disclosure-lexical",
        "results": results,
    }
    if json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"RESULTS: {len(results)}")
        for item in results:
            print(
                f"SKILL: {item['id']} score={item['score']} "
                f"version={item['version']} path={item['path']}"
            )
    return 0
