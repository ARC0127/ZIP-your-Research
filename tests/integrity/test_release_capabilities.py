from __future__ import annotations

import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import validate_v1_3  # noqa: E402


class ReleaseCapabilityContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        manifest = yaml.safe_load(
            (ROOT / "skills_manifest.yaml").read_text(encoding="utf-8")
        )
        cls.active_ids = [
            str(record["id"])
            for record in manifest["skills"]
            if isinstance(record, dict) and record.get("id")
        ]
        cls.capabilities, cls.errors = validate_v1_3.load_release_capabilities(
            cls.active_ids
        )

    def test_capability_manifest_is_strict_and_consistent(self) -> None:
        self.assertEqual(self.errors, [])
        by_id = {str(record["id"]): record for record in self.capabilities}
        self.assertEqual(
            by_id["research_paper_writing_skills_source"]["status"], "AVAILABLE"
        )
        self.assertEqual(
            by_id["figures4papers_source"]["status"], "SOURCE_UNAVAILABLE"
        )
        self.assertEqual(
            by_id["s340_original_source"]["status"], "SOURCE_UNAVAILABLE"
        )
        for capability_id in ("figures4papers_source", "s340_original_source"):
            response = str(by_id[capability_id].get("required_runtime_response", ""))
            self.assertIn("do not claim", response.lower())

    def test_missing_reference_exemption_is_skill_and_prefix_scoped(self) -> None:
        declared = validate_v1_3._declared_missing_reference
        self.assertTrue(
            declared(
                "ext/src/figures/fig_skill/SKILL.md",
                "S621",
                self.capabilities,
            )
        )
        self.assertTrue(
            declared(
                "ext/src/S340_v4.2_theory_global_skill_bundle/"
                "S340_v4.2_theory_global_skill.md",
                "S640",
                self.capabilities,
            )
        )
        self.assertFalse(
            declared(
                "ext/src/figures/fig_skill/SKILL.md",
                "S203",
                self.capabilities,
            )
        )
        self.assertFalse(
            declared(
                "manifests/not-real.yaml",
                "S621",
                self.capabilities,
            )
        )


if __name__ == "__main__":
    unittest.main()
