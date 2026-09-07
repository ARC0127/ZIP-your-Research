"""Retired-document cleanup preserves edited files and supports exact recovery.

Usage:
  python -B -m unittest tests.integrity.test_document_retirement_v1
"""

import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import prune_retired_docs_v1 as cleanup


class DocumentRetirementTests(unittest.TestCase):
    def test_duplicate_can_retire_but_active_skill_cannot(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "skills").mkdir()
            (root / "skills/old.md").write_bytes(b"protocol")
            (root / "skills/current.md").write_bytes(b"protocol")
            (root / "skills_manifest.yaml").write_text("skills:\n- id: S001\n  path: skills/current.md\n", encoding="utf-8")
            row = {"path": "skills/old.md", "replacement": "skills/current.md", "sha256": hashlib.sha256(b"protocol").hexdigest()}
            self.assertEqual(list(cleanup.pending(root, [row])), ["skills/old.md"])
            row.update(path="skills/current.md", replacement="skills/old.md")
            with self.assertRaisesRegex(ValueError, "not a retired"):
                cleanup.pending(root, [row])

    def test_cleanup_and_recovery_preserve_bytes_and_unrelated_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "suite"
            root.mkdir()
            (root / "old.md").write_bytes(b"old\r\n")
            (root / "keep.md").write_bytes(b"keep")
            rows = [{"path": "old.md", "sha256": hashlib.sha256(b"old\n").hexdigest()}]
            historical = {**rows[0], "sha256": hashlib.sha256(b"newer\n").hexdigest(),
                          "previous_versions": [{"commit": "previous-release", "sha256": rows[0]["sha256"]}]}
            self.assertEqual(cleanup.pending(root, [historical]), {"old.md": b"old\r\n"})
            backup = Path(directory) / "backup"
            self.assertEqual(cleanup.apply(root, rows, backup), 1)
            self.assertFalse((root / "old.md").exists())
            self.assertEqual(cleanup.pending(root, rows), {})
            cleanup.restore(root, backup / "receipt.json")
            self.assertEqual((root / "old.md").read_bytes(), b"old\r\n")
            self.assertEqual((root / "keep.md").read_bytes(), b"keep")

    def test_edited_document_prevents_partial_deletion(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "suite"
            root.mkdir()
            (root / "old.md").write_bytes(b"old")
            (root / "edited.md").write_bytes(b"user edit")
            digest = hashlib.sha256(b"old").hexdigest()
            rows = [{"path": p, "sha256": digest} for p in ("old.md", "edited.md")]
            with self.assertRaisesRegex(ValueError, "preserving changed"):
                cleanup.apply(root, rows, Path(directory) / "backup")
            self.assertEqual((root / "old.md").read_bytes(), b"old")

    def test_paths_cannot_escape_root_or_remove_skill_modules(self):
        with tempfile.TemporaryDirectory() as directory:
            for path in ("../outside.md", "skills/active.md"):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    cleanup.pending(Path(directory), [{"path": path, "sha256": "unused"}])


if __name__ == "__main__":
    unittest.main()
