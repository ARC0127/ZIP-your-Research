"""Fail-closed tests for first-build generated active paths."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from zyr_lib.manifest import RepositoryContractError, load_active_manifest  # noqa: E402


class GeneratedBootstrapTests(unittest.TestCase):
    def _fixture(self, root: Path) -> None:
        manifest = {
            "version": "1.6.6",
            "skills": [
                {
                    "id": "generated_engine",
                    "name": "generated_engine",
                    "category": "composite",
                    "path": "generated/MASTER_v1.6.6.md",
                },
                {
                    "id": "ordinary_skill",
                    "name": "ordinary_skill",
                    "category": "research_core",
                    "path": "skills/S999_ordinary.md",
                },
            ],
        }
        (root / "skills").mkdir(parents=True)
        (root / "skills" / "S999_ordinary.md").write_text("ordinary\n", encoding="utf-8")
        (root / "skills_manifest.yaml").write_text(
            yaml.safe_dump(manifest, sort_keys=False),
            encoding="utf-8",
        )

    def test_only_explicit_generated_output_may_be_missing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            self._fixture(fixture)

            with self.assertRaises(RepositoryContractError):
                load_active_manifest(fixture)

            _, entries = load_active_manifest(
                fixture,
                {"generated/MASTER_v1.6.6.md"},
            )
            self.assertEqual(len(entries), 2)

    def test_unallowlisted_missing_path_still_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            self._fixture(fixture)
            (fixture / "skills" / "S999_ordinary.md").unlink()

            with self.assertRaises(RepositoryContractError):
                load_active_manifest(
                    fixture,
                    {"generated/MASTER_v1.6.6.md"},
                )


if __name__ == "__main__":
    unittest.main()
