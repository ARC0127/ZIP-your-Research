from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

import yaml

from tools.audit_release_v1_7 import audit_release
from tools.make_release_v1_7 import (
    ReleaseError,
    _load_yaml,
    _zip_info,
    build_release,
    path_is_allowed,
    path_is_denied,
    required_exact_paths,
)


class ReleaseFixture:
    def __init__(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.root = self.base / "repo"
        self.root.mkdir()
        self.policy_path = self.root / "manifests" / "release_policy.yaml"
        self.third_party_path = self.root / "manifests" / "THIRD_PARTY_ASSETS.yaml"
        self.out1 = self.base / "release-1.zip"
        self.out2 = self.base / "release-2.zip"

        self._git("init", "-q")
        self._git("config", "user.email", "release-test@example.invalid")
        self._git("config", "user.name", "Release Test")
        self.write("LICENSE", "fixture license\n")
        self.write("VERSION", "vtest\n")
        self.write("src/ok.txt", "safe fixture\n")
        self.write("docs/memory/VISIBLE_MEMORY_PROTOCOL_v1.md", "public memory protocol\n")
        self.write("templates/memory/MEMORY_CONSENT.md", "public memory template\n")
        self.write("memory/session.txt", "private runtime memory\n")
        self.write("local/state.txt", "private local state\n")
        self.write("transcripts/run.txt", "private transcript\n")
        self.write("vendor/rpws/LICENSE", "MIT fixture\n")
        self.write("vendor/rpws/data.txt", "redistributable fixture\n")
        self.write_yaml(self.root / "skills_manifest.yaml", self.skill_manifest())
        self.write_yaml(
            self.root / "manifests" / "COMPATIBILITY.yaml",
            self.compatibility(),
        )
        self.write_yaml(
            self.root / "manifests" / "RELEASE_CAPABILITIES.yaml",
            self.capabilities(),
        )
        self.write_yaml(
            self.root / "manifests" / "generated_files.yaml",
            self.generated_files(),
        )
        self.write_yaml(
            self.root / "manifests" / "legacy_nonroutable.yaml",
            self.legacy_nonroutable(),
        )
        self.write_yaml(self.policy_path, self.policy())
        self.write_yaml(self.third_party_path, self.third_party())
        self.commit("baseline")

    def close(self) -> None:
        self.temp.cleanup()

    def _git(self, *args: str) -> None:
        subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True)

    def write(self, rel: str, value: str) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")
        return path

    @staticmethod
    def write_yaml(path: Path, value: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")

    def commit(self, message: str) -> None:
        self._git("add", "-A")
        self._git("commit", "-q", "-m", message)

    @staticmethod
    def policy() -> dict:
        return {
            "schema_version": 1,
            "policy_version": "test",
            "archive_root": "ZIP-your-Research",
            "default_version_file": "VERSION",
            "allow": {
                "exact": ["LICENSE", "VERSION", "skills_manifest.yaml"],
                "prefixes": [
                    "src/",
                    "docs/",
                    "templates/",
                    "manifests/",
                    "vendor/rpws/",
                    "memory/",
                    "local/",
                    "transcripts/",
                ],
            },
            "deny": {
                "prefixes": ["memory/", "local/", "transcripts/"],
                "path_parts": ["__pycache__"],
                "basenames": [".env"],
                "name_globs": ["*.key", "*.zip"],
            },
            "third_party": {
                "allowed_asset_ids": ["rpws"],
                "capabilities_manifest": "manifests/RELEASE_CAPABILITIES.yaml",
                "require_license_status": "VERIFIED_LOCAL",
                "require_redistribution_status": "ALLOWED",
                "block_unknown_or_unlisted": True,
            },
            "required": {
                "active_skill_count": 1,
                "legacy_skill_count": 0,
                "generated_file_count": 1,
                "exact": [
                    "LICENSE",
                    "VERSION",
                    "skills_manifest.yaml",
                    "src/ok.txt",
                    "vendor/rpws/LICENSE",
                    "manifests/COMPATIBILITY.yaml",
                    "manifests/RELEASE_CAPABILITIES.yaml",
                    "manifests/THIRD_PARTY_ASSETS.yaml",
                    "manifests/generated_files.yaml",
                    "manifests/legacy_nonroutable.yaml",
                    "manifests/release_policy.yaml",
                ],
            },
            "secrets": {
                "max_text_scan_bytes": 2_097_152,
                "patterns": [
                    {
                        "id": "openai_key",
                        "regex": r"(?<![A-Za-z0-9])sk-(?:proj-)?[A-Za-z0-9_-]{20,}",
                    }
                ],
            },
            "zip": {
                "max_entries": 100,
                "max_archive_bytes": 10_000_000,
                "max_entry_uncompressed_bytes": 1_000_000,
                "max_total_uncompressed_bytes": 10_000_000,
                "max_compression_ratio": 100,
                "timestamp_utc": [1980, 1, 1, 0, 0, 0],
                "compresslevel": 9,
                "file_mode": "0644",
                "generated_manifest_path": "RELEASE_MANIFEST_v1_7.json",
            },
        }

    @staticmethod
    def skill_manifest() -> dict:
        return {
            "version": "vtest",
            "skills": [
                {
                    "id": "Sfixture",
                    "name": "fixture",
                    "category": "research_core",
                    "path": "src/ok.txt",
                }
            ],
        }

    @staticmethod
    def compatibility() -> dict:
        return {
            "schema_version": 1,
            "public_cli": {"path": "src/ok.txt"},
            "compatibility_entrypoints": [],
        }

    @staticmethod
    def capabilities() -> dict:
        return {
            "schema_version": 1,
            "capabilities": [
                {
                    "id": "fixture_source",
                    "asset_id": "rpws",
                    "status": "AVAILABLE",
                    "bundled_path": "vendor/rpws",
                    "allowed_missing_ref_prefixes": [],
                    "affected_skill_ids": ["Sfixture"],
                    "missing_behavior": "FAIL_CLOSED",
                }
            ],
        }

    @staticmethod
    def generated_files() -> dict:
        return {
            "schema_version": 1,
            "generated_files": [
                {
                    "path": "src/ok.txt",
                    "builder": "fixture",
                    "inputs": ["src/"],
                }
            ],
        }

    @staticmethod
    def legacy_nonroutable() -> dict:
        return {
            "schema_version": 1,
            "hash_algorithm": "sha256",
            "entries": [],
        }

    @staticmethod
    def third_party() -> dict:
        return {
            "schema_version": 1,
            "assets": [
                {
                    "id": "rpws",
                    "local_path": "vendor/rpws",
                    "pin": {"status": "UNKNOWN", "revision": "UNKNOWN"},
                    "license": {
                        "status": "VERIFIED_LOCAL",
                        "spdx_id": "MIT",
                        "license_path": "vendor/rpws/LICENSE",
                    },
                    "redistribution": {"status": "ALLOWED"},
                }
            ],
        }

    def build(self, out: Path | None = None) -> dict:
        return build_release(
            root=self.root,
            out=out or self.out1,
            policy_path=self.policy_path,
            third_party_path=self.third_party_path,
            release_version="vtest",
        )


class MakeReleaseV17Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = ReleaseFixture()

    def tearDown(self) -> None:
        self.fixture.close()

    def test_archive_is_deterministic_and_auditable(self) -> None:
        first = self.fixture.build(self.fixture.out1)
        second = self.fixture.build(self.fixture.out2)
        self.assertEqual(self.fixture.out1.read_bytes(), self.fixture.out2.read_bytes())
        self.assertEqual(first["archive_sha256"], second["archive_sha256"])
        result = audit_release(
            archive_path=self.fixture.out1,
            policy_path=self.fixture.policy_path,
            third_party_path=self.fixture.third_party_path,
        )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["release_version"], "vtest")
        with zipfile.ZipFile(self.fixture.out1) as archive:
            manifest = json.loads(
                archive.read(
                    "ZIP-your-Research/RELEASE_MANIFEST_v1_7.json"
                ).decode("utf-8")
            )
        self.assertEqual(manifest["release_version"], "vtest")
        released_paths = {record["path"] for record in manifest["files"]}
        self.assertIn("VERSION", released_paths)
        self.assertIn("docs/memory/VISIBLE_MEMORY_PROTOCOL_v1.md", released_paths)
        self.assertIn("templates/memory/MEMORY_CONSENT.md", released_paths)
        self.assertNotIn("memory/session.txt", released_paths)
        self.assertNotIn("local/state.txt", released_paths)
        self.assertNotIn("transcripts/run.txt", released_paths)

    def test_version_mismatch_refuses_release(self) -> None:
        with self.assertRaisesRegex(ReleaseError, "does not match"):
            build_release(
                root=self.fixture.root,
                out=self.fixture.out1,
                policy_path=self.fixture.policy_path,
                third_party_path=self.fixture.third_party_path,
                release_version="vother",
            )
        self.assertFalse(self.fixture.out1.exists())

    def test_atomic_write_failure_preserves_existing_archive(self) -> None:
        self.fixture.build(self.fixture.out1)
        existing_archive = self.fixture.out1.read_bytes()

        with mock.patch.object(
            zipfile.ZipFile,
            "writestr",
            side_effect=OSError("simulated disk write failure"),
        ):
            with self.assertRaisesRegex(ReleaseError, "Atomic ZIP write failed"):
                self.fixture.build(self.fixture.out1)

        self.assertEqual(self.fixture.out1.read_bytes(), existing_archive)
        temporary_pattern = f".{self.fixture.out1.name}.*.tmp"
        self.assertEqual(list(self.fixture.out1.parent.glob(temporary_pattern)), [])

    def test_auditor_rejects_zip_bomb_before_reading_payload(self) -> None:
        bomb = self.fixture.base / "high-compression.zip"
        with zipfile.ZipFile(
            bomb,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        ) as archive:
            archive.writestr("ZIP-your-Research/bomb.txt", b"A" * 65_536)

        with mock.patch.object(
            zipfile.ZipFile,
            "read",
            side_effect=AssertionError("payload read must not happen before ZIP preflight"),
        ) as read:
            with self.assertRaisesRegex(ReleaseError, "compression ratio exceeds"):
                audit_release(
                    archive_path=bomb,
                    policy_path=self.fixture.policy_path,
                    third_party_path=self.fixture.third_party_path,
                )
        read.assert_not_called()

    def test_auditor_rejects_single_file_self_reported_archive(self) -> None:
        truncated = self.fixture.base / "self-reported-truncated.zip"
        policy = _load_yaml(self.fixture.policy_path)
        generated_path = "ZIP-your-Research/RELEASE_MANIFEST_v1_7.json"
        self_report = json.dumps(
            {
                "schema_version": 1,
                "release_version": "vtest",
                "files": [],
            },
            sort_keys=True,
        ).encode("utf-8")
        with zipfile.ZipFile(truncated, "w") as archive:
            archive.writestr(_zip_info(generated_path, policy), self_report)

        with mock.patch.object(
            zipfile.ZipFile,
            "read",
            side_effect=AssertionError("required.exact must fail before payload read"),
        ) as read:
            with self.assertRaisesRegex(ReleaseError, "omits required exact paths"):
                audit_release(
                    archive_path=truncated,
                    policy_path=self.fixture.policy_path,
                    third_party_path=self.fixture.third_party_path,
                )
        read.assert_not_called()

    def test_untracked_dotenv_refuses_release(self) -> None:
        self.fixture.write(".env", "NOT_A_REAL_SECRET=test\n")
        with self.assertRaisesRegex(ReleaseError, "Untracked files"):
            self.fixture.build()

    def test_api_key_pattern_refuses_release(self) -> None:
        secret = "sk-proj-" + ("A" * 32)
        self.fixture.write("src/config.txt", f"credential={secret}\n")
        self.fixture.commit("secret mutation")
        with self.assertRaisesRegex(ReleaseError, "Secret pattern 'openai_key'"):
            self.fixture.build()
        self.assertFalse(self.fixture.out1.exists(), "a refused secret must not produce a ZIP")

    def test_unknown_license_asset_refuses_release(self) -> None:
        policy = self.fixture.policy()
        policy["allow"]["prefixes"].append("vendor/unknown/")
        policy["third_party"]["allowed_asset_ids"].append("unknown")
        third_party = self.fixture.third_party()
        third_party["assets"].append(
            {
                "id": "unknown",
                "local_path": "vendor/unknown",
                "pin": {"status": "UNKNOWN", "revision": "UNKNOWN"},
                "license": {
                    "status": "UNKNOWN",
                    "spdx_id": "UNKNOWN",
                    "license_path": "UNKNOWN",
                },
                "redistribution": {"status": "BLOCKED"},
            }
        )
        self.fixture.write("vendor/unknown/data.txt", "blocked fixture\n")
        self.fixture.write_yaml(self.fixture.policy_path, policy)
        self.fixture.write_yaml(self.fixture.third_party_path, third_party)
        self.fixture.commit("unknown-license mutation")
        with self.assertRaisesRegex(ReleaseError, "UNKNOWN or unverified license"):
            self.fixture.build()

    def test_tracked_symlink_refuses_release(self) -> None:
        link = self.fixture.root / "src" / "linked.txt"
        link.symlink_to("ok.txt")
        self.fixture.commit("symlink mutation")
        with self.assertRaisesRegex(ReleaseError, "Symlink refuses release"):
            self.fixture.build()

    def test_cli_has_stable_json_and_exit_codes(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        builder = repo_root / "tools" / "make_release_v1_7.py"
        auditor = repo_root / "tools" / "audit_release_v1_7.py"
        out = self.fixture.base / "cli-release.zip"
        common = [
            "--root",
            str(self.fixture.root),
            "--policy",
            "manifests/release_policy.yaml",
            "--third-party",
            "manifests/THIRD_PARTY_ASSETS.yaml",
        ]
        built = subprocess.run(
            [sys.executable, str(builder), *common, "--out", str(out)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(built.returncode, 0, built.stderr)
        self.assertEqual(json.loads(built.stdout)["archive"], str(out.resolve()))

        audited = subprocess.run(
            [
                sys.executable,
                str(auditor),
                str(out),
                *common,
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(audited.returncode, 0, audited.stderr)
        self.assertEqual(json.loads(audited.stdout)["status"], "PASS")

        self.fixture.write(".env", "NOT_A_REAL_SECRET=test\n")
        refused = subprocess.run(
            [
                sys.executable,
                str(builder),
                *common,
                "--out",
                str(self.fixture.base / "refused.zip"),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(refused.returncode, 1)
        self.assertTrue(refused.stderr.startswith("ERROR:"))
        self.assertNotIn("Traceback", refused.stderr)


class RepositoryPolicyTests(unittest.TestCase):
    def test_repository_policy_includes_public_memory_and_blocks_private_roots(self) -> None:
        root = Path(__file__).resolve().parents[2]
        policy = _load_yaml(root / "manifests" / "release_policy.yaml")
        self.assertTrue(path_is_allowed("VERSION", policy))
        self.assertTrue(path_is_allowed("docs/memory/VISIBLE_MEMORY_PROTOCOL_v1.md", policy))
        self.assertFalse(path_is_denied("docs/memory/VISIBLE_MEMORY_PROTOCOL_v1.md", policy))
        self.assertTrue(path_is_allowed("templates/memory/MEMORY_CONSENT.md", policy))
        self.assertFalse(path_is_denied("templates/memory/MEMORY_CONSENT.md", policy))
        self.assertTrue(path_is_denied("memory/session.txt", policy))
        self.assertTrue(path_is_denied("local/state.txt", policy))
        self.assertTrue(path_is_denied("transcripts/run.txt", policy))

    def test_repository_policy_blocks_unknown_license_vendors(self) -> None:
        root = Path(__file__).resolve().parents[2]
        policy = _load_yaml(root / "manifests" / "release_policy.yaml")
        self.assertTrue(path_is_allowed("ext/src/rpws/LICENSE", policy))
        self.assertFalse(path_is_denied("ext/src/rpws/LICENSE", policy))
        self.assertFalse(path_is_denied("ext/src/rpws/paper_skill/ref/ex/index.md", policy))
        self.assertFalse(path_is_allowed("ext/src/figures/README.md", policy))
        self.assertTrue(path_is_denied("ext/src/figures/README.md", policy))
        self.assertFalse(path_is_allowed("ext/src/awesome/README.md", policy))
        self.assertTrue(path_is_denied("ext/src/awesome/README.md", policy))

    def test_repository_policy_requires_all_memory_templates_and_safe_carriers(self) -> None:
        root = Path(__file__).resolve().parents[2]
        policy = _load_yaml(root / "manifests" / "release_policy.yaml")
        required = required_exact_paths(policy)
        memory_templates = {
            "templates/memory/DECISION_LOG.md",
            "templates/memory/FAILED_PATHS.md",
            "templates/memory/LONG_TERM_MEMORY.md",
            "templates/memory/MEMORY_AUDIT.md",
            "templates/memory/MEMORY_CONSENT.md",
            "templates/memory/MEMORY_EXPORT.md",
            "templates/memory/MEMORY_PROPOSAL.md",
            "templates/memory/SHORT_TERM_MEMORY.md",
        }
        self.assertEqual(len(memory_templates), 8)
        self.assertTrue(memory_templates <= required)
        skill_memory_files = {
            "docs/memory/DYNAMIC_SKILL_MEMORY_PROTOCOL_v1.md",
            "skills/research_orchestrator/S661_dynamic_skill_memory.md",
            "templates/skill_memory/SKILL_CHANGE_CONSENT.md",
            "templates/skill_memory/SKILL_DELETION_RECEIPT.md",
            "templates/skill_memory/SKILL_EVALUATION.md",
            "templates/skill_memory/SKILL_PROPOSAL.md",
            "templates/skill_memory/TRACE_RECORD.md",
            "tests/skill_memory/test_skill_memory_v1.py",
            "tools/zyr_lib/skill_memory.py",
        }
        self.assertTrue(skill_memory_files <= required)
        self.assertIn("manifests/RELEASE_CAPABILITIES.yaml", required)
        self.assertIn("tests/integrity/test_release_capabilities.py", required)
        safe_carriers = {
            "artifacts/evidence_ledger.csv",
            "artifacts/negative_result_ledger.md",
            "artifacts/proof_casebook.md",
            "artifacts/run_state.json",
        }
        self.assertTrue(safe_carriers <= required)
        self.assertTrue(all(path_is_allowed(path, policy) for path in safe_carriers))
        self.assertTrue(all(not path_is_denied(path, policy) for path in safe_carriers))
        self.assertFalse(path_is_allowed("artifacts/runlog.jsonl", policy))


if __name__ == "__main__":
    unittest.main()
