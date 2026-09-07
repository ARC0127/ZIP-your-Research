"""Discovery coverage and installer scope invariants.

Usage:
  python -B -m unittest tests.integrity.test_astra_instructions_v1
"""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import install_codex_profile_v2 as installer


class AstraInstructionTests(unittest.TestCase):
    def test_discovery_covers_every_preserved_identity(self):
        self.assertEqual(len(installer.descriptions()), 150)

    def test_description_edit_preserves_protocol_and_other_metadata(self):
        original = b'---\nname: sample\ndescription: old\nversion: 1.6.6\nmetadata:\n  custom: preserved\n---\n# Protocol\nExact approval required.\n'
        updated = installer.with_description(original, "Audit a proof.")
        before = installer.base.front(original.decode())
        after = installer.base.front(updated.decode())
        before.pop("description")
        after.pop("description")
        self.assertEqual(before, after)
        self.assertEqual(original.split(b"---", 2)[2], updated.split(b"---", 2)[2])

    def test_personal_instructions_are_opt_in(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(installer.base, "plan", return_value={}):
            root = Path(directory)
            normal = installer.plan(root)
            self.assertTrue(all(path.startswith("skills/zip-your-research/") for path in normal))
            with self.assertRaisesRegex(ValueError, "existing AGENTS"):
                installer.plan(root, True)
            (root / "AGENTS.md").write_text("existing", encoding="utf-8")
            for name in ("headroom", "theory-claim-audit"):
                dest = root / "skills" / name / "SKILL.md"
                dest.parent.mkdir(parents=True)
                dest.write_text("existing", encoding="utf-8")
            personal = installer.plan(root, True)
            extras = set(personal) - set(normal)
            self.assertEqual(extras, {
                "AGENTS.md", "instructions/archive-protocol.md",
                "instructions/engineering.md", "instructions/research-writing.md",
                "skills/headroom/SKILL.md", "skills/theory-claim-audit/SKILL.md",
            })
            self.assertFalse(any(path == "config.toml" or path.startswith("memories/") or path.startswith("skills/claim/") for path in personal))


if __name__ == "__main__":
    unittest.main()
