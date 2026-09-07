#!/usr/bin/env python3
from pathlib import Path
import json, hashlib, sys

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "artifacts/integration/integr_manifest.json").read_text(encoding="utf-8"))

def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

missing = []
mismatch = []

for item in manifest.get("source_inventory", []):
    rel = item.get("packed_relpath")
    if not rel:
        source = item.get("source", "UNKNOWN")
        source_path = item.get("path", "UNKNOWN")
        root_rel = manifest.get("preserved_source_roots", {}).get(source)
        rel = f"{root_rel}/{source_path}" if root_rel else None
    if not rel:
        missing.append(f"UNRESOLVED::{item}")
        continue
    p = ROOT / rel
    if not p.exists():
        missing.append(rel)
        continue
    actual = sha(p)
    expected = item.get("sha256")
    if expected and actual != expected:
        mismatch.append(rel)

required = [
    "skills/writing_engine/MASTER_v1.3.2.md",
    "skills/writing_engine/MASTER_v1.7.0.md",
    "skills/figure_engine/MASTER_v1.6.5.md",
    "skills/rwf_s340/S601_paper_story_section_arch.md",
    "skills/rwf_s340/S602_claim_evidence_reverse_outline_review.md",
    "skills/rwf_s340/S603_bilingual_human_voice_delta_rewrite.md",
    "skills/rwf_s340/S604_experiment_result_narrative_and_caption.md",
    "skills/rwf_s340/S621_publication_fig_design_theory.md",
    "skills/rwf_s340/S622_matplotlib_publication_script_builder.md",
    "skills/rwf_s340/S623_visual_claim_caption_audit.md",
    "skills/rwf_s340/S640_s340_global_paper_logic_language_audit.md",
    "skills/rwf_s340/S650_integrated_pack_no_omission_valid.md",
    "router/ext_router/ROUTER_req_BINDING_RWF_S340_v1.6.md",
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
print(f"source_files={len(manifest.get('source_inventory', []))}")
print(f"integrated_wrappers={len(manifest.get('integrated_wrappers', []))}")
