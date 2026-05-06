#!/usr/bin/env python3
from pathlib import Path
import json, hashlib, sys

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "artifacts/integration/integr_manifest.json").read_text(encoding="utf-8"))
source_manifest = json.loads((ROOT / "manifests/src_manifest.json").read_text(encoding="utf-8"))
source_key = {
    "Research-Paper-Writing-Skills-main": "rpws",
    "awesome-ai-research-writing-main": "awesome",
    "figures4papers-main": "figures",
}
packed_by_source = {
    (item["source_key"], item["source_relpath"]): item["packed_relpath"]
    for item in source_manifest["files"]
}
missing = []
mismatch = []
for item in manifest["source_inventory"]:
    src_name = item["source"]
    key = source_key.get(src_name)
    if key is None:
        missing.append(f"UNKNOWN_SOURCE::{src_name}/{item['path']}")
        continue
    packed = packed_by_source.get((key, item["path"]))
    if packed is None:
        missing.append(f"UNMAPPED_SOURCE::{src_name}/{item['path']}")
        continue
    p = ROOT / packed
    if not p.exists():
        missing.append(packed)
        continue
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    if h != item["sha256"]:
        mismatch.append(packed)

required = [
    "skills/rwf_s340/S601_paper_story_section_arch.md",
    "skills/rwf_s340/S602_claim_evidence_reverse_outline_review.md",
    "skills/rwf_s340/S603_bilingual_human_voice_delta_rewrite.md",
    "skills/rwf_s340/S604_experiment_result_narrative_and_caption.md",
    "skills/rwf_s340/S621_publication_fig_design_theory.md",
    "skills/rwf_s340/S622_matplotlib_publication_script_builder.md",
    "skills/rwf_s340/S623_visual_claim_caption_audit.md",
    "skills/rwf_s340/S640_s340_global_paper_logic_language_audit.md",
    "skills/rwf_s340/S650_integrated_pack_no_omission_valid.md",
    "skills/master_integrated/MASTER_research_write_fig_stack_v1.0.md",
    "router/ext_router/ROUTER_ADDENDUM_research_write_figures_v1.0.md",
]
missing_required = [r for r in required if not (ROOT / r).exists()]
if missing or mismatch or missing_required:
    print("VALIDATION_FAILED")
    if missing:
        print("missing source files:", missing[:20])
    if mismatch:
        print("checksum mismatches:", mismatch[:20])
    if missing_required:
        print("missing required integrated files:", missing_required)
    sys.exit(1)
print("VALIDATION_OK")
print(f"source_files={len(manifest['source_inventory'])}")
print(f"new_skills={len(manifest['new_skills'])}")
