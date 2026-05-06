#!/usr/bin/env python3
"""Backward-compatible wrapper for v1.6.4 CI commands.

The v1.6.5 release uses tools/cleanup_legacy_duplicate_paths_v1_6_5.py.
This wrapper is intentionally kept so older GitHub workflows or in-place
upgrades that still call the v1.6.4 filename do not fail before validation.
"""
from __future__ import annotations

import runpy
from pathlib import Path

TARGET = Path(__file__).with_name("cleanup_legacy_duplicate_paths_v1_6_5.py")

if not TARGET.exists():
    raise SystemExit(f"Missing target cleanup script: {TARGET}")

runpy.run_path(str(TARGET), run_name="__main__")
