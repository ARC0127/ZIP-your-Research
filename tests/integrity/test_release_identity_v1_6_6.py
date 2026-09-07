"""Regression tests for the ZYR v1.7.0 release-identity gate."""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from validate_release_identity_v1_7_0 import validate  # noqa: E402


IDENTITY_FIXTURE = (
    "VERSION",
    "v",
    "skills_manifest.yaml",
    "README.md",
    "AGENTS.md",
    ".claude/skills/zip-your-research/SKILL.md",
    ".github/skills/zip-your-research/SKILL.md",
    "boot/00_RESPONSE_STATUS_BANNER_v1.7.0.md",
    "boot/01_GLOBAL_GUARDRAILS_v1.7.0.md",
    "boot/00_BOOTSTRAP_PROTOCOL_v1.7.0.md",
    "boot/04_MODE_LOCK_FORMAT_v1.7.0.md",
    "boot/08_MODE_LOCK_SCHEMA_v1.7.0.json",
    "boot/01_MIGRATION_PROMPT_TEMPLATE_v1.7.0.md",
    "router/intake_profile_v1.7.0.yaml",
    "boot/00_RESPONSE_STATUS_BANNER_v1.3.2.md",
    "boot/01_GLOBAL_GUARDRAILS_v1.3.2.md",
    "docs/VERSION_IDENTITY_v1.7.0.md",
    "manifests/ACKNOWLEDGMENTS_BASELINE_v1.6.6.sha256",
    "skills/writing_engine/MASTER_v1.7.0.md",
    "skills/writing_engine/MASTER_v1.3.2.md",
    "skills/coding_engine/MASTER_v1.7.0.md",
    "skills/coding_engine/MASTER_v1.3.2.md",
    "router/SKILL_MAP_v1.7.0.md",
    "router/SKILL_MAP_v1.3.2.md",
)


class ReleaseIdentityTests(unittest.TestCase):
    def test_old_session_versions_are_rejected(self) -> None:
        for relative, original, changed in (
            ("boot/04_MODE_LOCK_FORMAT_v1.7.0.md", '"version": "v1.7.0"', '"version": "v1.3.2"'),
            ("boot/08_MODE_LOCK_SCHEMA_v1.7.0.json", '"const": "v1.7.0"', '"const": "v1.3.2"'),
            ("boot/01_MIGRATION_PROMPT_TEMPLATE_v1.7.0.md", "Repo version: v1.7.0", "Repo version: v1.5.0"),
        ):
            with self.subTest(path=relative), tempfile.TemporaryDirectory() as directory:
                fixture = Path(directory)
                for item in IDENTITY_FIXTURE:
                    target = fixture / item
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(ROOT / item, target)
                target = fixture / relative
                text = target.read_text(encoding="utf-8")
                self.assertIn(original, text)
                target.write_text(text.replace(original, changed), encoding="utf-8")
                self.assertTrue(validate(fixture))

    def test_current_repository_passes(self) -> None:
        self.assertEqual(validate(ROOT), [])

    def test_active_suite_regression_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            for relative in IDENTITY_FIXTURE:
                source = ROOT / relative
                target = fixture / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)

            agents = fixture / "AGENTS.md"
            text = agents.read_text(encoding="utf-8").replace(
                "# AGENTS.md (suite v1.7.0)",
                "# AGENTS.md (v1.3.2)",
                1,
            )
            agents.write_text(text, encoding="utf-8")

            errors = validate(fixture)
            self.assertTrue(
                any("active suite" in error or "suite v1.7.0" in error for error in errors),
                errors,
            )


if __name__ == "__main__":
    unittest.main()
