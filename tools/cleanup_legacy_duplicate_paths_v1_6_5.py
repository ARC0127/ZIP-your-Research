#!/usr/bin/env python3
"""Remove stale duplicate skill paths from pre-v1.6.5 in-place upgrades.

Why this exists:
- v1.6 introduced Windows-safe short paths, e.g. skills/experiments/ -> skills/exp/.
- If a release ZIP is copied over an existing Git checkout without deleting old files,
  both old and new paths remain, causing duplicate S### IDs in CI.
- This script removes only known stale aliases when the canonical replacement exists.

Usage:
  python tools/cleanup_legacy_duplicate_paths_v1_6_5.py --dry-run
  python tools/cleanup_legacy_duplicate_paths_v1_6_5.py
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Entire stale directory replaced by skills/exp/.
STALE_DIRS = [
    "skills/experiments",
]

# Stale alias files that duplicated canonical short names.
STALE_FILES = [
    # research-writing / figure wrapper duplicates; canonical route is skills/rwf_s340/
    "skills/rw/S601_paper_story_section_arch.md",
    "skills/rw/S602_claim_evidence_reverse_outline_review.md",
    "skills/rw/S603_bilingual_human_voice_delta_rewrite.md",
    "skills/rw/S604_experiment_result_narrative_and_ta_122557d2.md",
    "skills/fig_ops/S621_publication_fig_design_theory.md",
    "skills/fig_ops/S622_matplotlib_publication_script_builder.md",
    "skills/fig_ops/S623_visual_claim_caption_audit.md",
    # paper_ops long-name aliases
    "skills/paper_ops/S509_author_contribution_statement.md",
    "skills/paper_ops/S512_figure_table_audit.md",
    "skills/paper_ops/S513_title_abstract_optimizer.md",
    "skills/paper_ops/S515_open_source_release_plan.md",
    "skills/paper_ops/S517_figure_table_caption_rewrite.md",
    "skills/paper_ops/S521_contribution_statement_refinement.md",
    "skills/paper_ops/S524_open_source_release_note_generator.md",
    # reproducibility long-name aliases
    "skills/reproducibility/S415_data_pipeline_invariance_tests.md",
    "skills/reproducibility/S423_security_review_open_source.md",
    # research_core long-name aliases
    "skills/research_core/S204_literature_triage_pipeline.md",
    "skills/research_core/S207_contribution_claim_refinement.md",
    "skills/research_core/S217_contribution_type_selector.md",
]

CANONICAL_CHECKS = [
    "skills/exp/S301_min_decidable_experiment.md",
    "skills/rwf_s340/S601_paper_story_section_arch.md",
    "skills/rwf_s340/S621_publication_fig_design_theory.md",
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="print planned deletions without modifying files")
    args = ap.parse_args()

    missing = [rel for rel in CANONICAL_CHECKS if not (ROOT / rel).exists()]
    if missing:
        raise SystemExit("Refusing cleanup because canonical files are missing:\n" + "\n".join(f"- {m}" for m in missing))

    removed: list[str] = []
    skipped: list[str] = []

    for rel in STALE_DIRS:
        path = ROOT / rel
        if path.exists():
            removed.append(rel + "/")
            if not args.dry_run:
                shutil.rmtree(path)
        else:
            skipped.append(rel + "/")

    for rel in STALE_FILES:
        path = ROOT / rel
        if path.exists():
            removed.append(rel)
            if not args.dry_run:
                path.unlink()
        else:
            skipped.append(rel)

    mode = "DRY-RUN" if args.dry_run else "APPLIED"
    print(f"Legacy duplicate cleanup: {mode}")
    print(f"planned_or_removed={len(removed)} skipped_absent={len(skipped)}")
    for rel in removed:
        print(f"- {rel}")


if __name__ == "__main__":
    main()
