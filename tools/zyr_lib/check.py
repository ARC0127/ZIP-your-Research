"""Run the strict repository and generated-artifact checks.

Usage:
  python tools/zyr.py check
  python tools/zyr.py check --ci
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from .build import run_build_check
from .manifest import ROOT


def run_check(root: Path = ROOT, ci_mode: bool = False) -> int:
    """Run compatibility validator then the authoritative read-only build check."""
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [sys.executable, str(root / "tools" / "validate_v7_2.py")]
    completed = subprocess.run(command, cwd=str(root), env=environment, check=False)
    if completed.returncode != 0:
        return completed.returncode
    if ci_mode:
        closure_test = subprocess.run(
            [
                sys.executable,
                "-m",
                "unittest",
                "tests.integrity.test_manifest_closure",
                "tests.integrity.test_release_capabilities",
                "tests.skill_memory.test_skill_memory_v1",
            ],
            cwd=str(root),
            env=environment,
            check=False,
        )
        if closure_test.returncode != 0:
            return closure_test.returncode
    result = run_build_check(root)
    if result == 0:
        print(f"ZYR check passed: ci_mode={str(ci_mode).lower()}")
    return result
