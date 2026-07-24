"""Forward stable facade commands to bounded repository CLIs.

Usage:
  python tools/zyr.py route "query"
  python tools/zyr.py route-test
  python tools/zyr.py release-audit release.zip
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Sequence

from .manifest import ROOT, RepositoryContractError, resolve_repo_path


def run_repository_cli(
    script_relative: str, arguments: Sequence[str], root: Path = ROOT
) -> int:
    """Run one fixed repository CLI and preserve its process exit code."""
    try:
        script = resolve_repo_path(root, script_relative, "forwarded CLI")
    except RepositoryContractError as exc:
        print(f"Forwarding failed: {exc}", file=sys.stderr)
        return 1
    if not script.is_file():
        print(f"Forwarding failed: missing CLI {script_relative}", file=sys.stderr)
        return 1
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, str(script), *arguments],
        cwd=str(root),
        env=environment,
        check=False,
    )
    return completed.returncode
