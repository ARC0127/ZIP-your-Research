"""Regression tests for active-canonical plus explicit-legacy skill closure.

Usage:
  python -m unittest tests.integrity.test_manifest_closure
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.zyr_lib.manifest import (
    ROOT,
    RepositoryContractError,
    SKILL_FILENAME_RE,
    load_active_manifest,
    validate_legacy_overlay,
)


class ManifestClosureTests(unittest.TestCase):
    def test_current_tree_is_canonical_plus_declared_legacy(self) -> None:
        _, active_entries = load_active_manifest(ROOT)
        legacy_count = validate_legacy_overlay(active_entries, ROOT)
        canonical_count = sum(
            1
            for item in active_entries
            if SKILL_FILENAME_RE.fullmatch(Path(str(item["path"])).name)
        )
        physical_count = sum(
            1
            for path in (ROOT / "skills").rglob("*.md")
            if SKILL_FILENAME_RE.fullmatch(path.name)
            and "platform_zyr_skills/rewrites/" not in path.relative_to(ROOT).as_posix()
        )
        self.assertEqual(physical_count, canonical_count + legacy_count)
        self.assertGreaterEqual(canonical_count, 144)
        self.assertGreaterEqual(legacy_count, 48)
        self.assertGreaterEqual(physical_count, 192)

    def test_unmanifested_new_skill_id_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="zyr-manifest-closure-") as temporary:
            root = Path(temporary)
            (root / "manifests").mkdir()
            (root / "skills").mkdir()
            (root / "manifests" / "legacy_nonroutable.yaml").write_text(
                "schema_version: 1\n"
                "hash_algorithm: sha256\n"
                "entries: []\n",
                encoding="utf-8",
            )
            (root / "skills" / "S999_unmanifested.md").write_text(
                "---\n"
                "id: S999\n"
                "name: unmanifested\n"
                "category: research_core\n"
                "---\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                RepositoryContractError, "no active manifest mapping"
            ):
                validate_legacy_overlay([], root)


if __name__ == "__main__":
    unittest.main()
