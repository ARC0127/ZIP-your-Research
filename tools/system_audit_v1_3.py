#!/usr/bin/env python3
"""System-level audit (v1.3.2).

Goals:
- Verify the repo is logically self-consistent (paths, versions, core workflows).
- Run the canonical deterministic checks.

This is intentionally *minimal* (no external deps).

Usage:
  python tools/system_audit_v1_3.py

Output:
  artifacts/system_audit/report_v1.3.2.md
"""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "artifacts" / "system_audit"
OUT = OUTDIR / "report_v1.3.2.md"

FORBIDDEN_SUFFIXES = {".zip", ".7z", ".tar", ".gz", ".bz2", ".xz"}
FORBIDDEN_VERSION_MARKERS = ["_v1.0.1", "_v1.2"]


def run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return p.returncode, p.stdout


def scan_forbidden_files() -> list[str]:
    bad: list[str] = []
    for p in ROOT.rglob("*"):
        if p.is_dir():
            continue
        if p.suffix.lower() in FORBIDDEN_SUFFIXES:
            bad.append(str(p.relative_to(ROOT)))
        rel = p.as_posix()
        for mk in FORBIDDEN_VERSION_MARKERS:
            if mk in rel:
                bad.append(str(p.relative_to(ROOT)))
                break
    return sorted(set(bad))


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    lines: list[str] = []
    lines.append(f"# System Audit Report — v{version}\n\n")
    lines.append(f"- generated_at: {now}\n")

    # 0) forbidden files scan
    bad = scan_forbidden_files()
    lines.append("\n## 0) Forbidden file scan\n")
    if bad:
        lines.append("Result: **FAIL**\n\n")
        for x in bad[:200]:
            lines.append(f"- {x}\n")
        if len(bad) > 200:
            lines.append(f"- ... and {len(bad)-200} more\n")
    else:
        lines.append("Result: **PASS**\n")

    # 1) build_all
    steps = [
        ([sys.executable, "tools/build_all.py"], "1) build_all"),
        ([sys.executable, "tools/validate_v7_2.py"], "2) validate_v7_2"),
        ([sys.executable, "tools/validate_corpus_v1_3.py"], "3) validate_corpus_v1_3"),
        ([sys.executable, "tools/simulate_locked_regression_v1_3.py", "--n", "25", "--seed", "0"], "4) simulate_locked_regression"),
        ([sys.executable, "tools/drift_audit_v1_3.py"], "5) drift_audit_v1_3"),
    ]

    ok = (len(bad) == 0)

    for cmd, title in steps:
        code, out = run(cmd)
        ok = ok and (code == 0)
        lines.append(f"\n## {title}\n")
        lines.append(f"Return code: `{code}`\n\n")
        lines.append("```\n")
        lines.append(out.rstrip() + "\n")
        lines.append("```\n")

    lines.append("\n## Summary\n")
    lines.append(f"- overall: {'PASS' if ok else 'FAIL'}\n")

    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")

    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
