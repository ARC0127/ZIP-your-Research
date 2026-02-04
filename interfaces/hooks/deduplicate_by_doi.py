from __future__ import annotations
from typing import Dict, Any, List, Tuple

def deduplicate(items: List[Dict[str,Any]]) -> Tuple[List[Dict[str,Any]], Dict[str,Any]]:
    """
    Deduplicate by DOI if available; fallback to (title, year).
    Returns (deduped_items, meta).
    """
    seen=set()
    out=[]
    removed=0
    for it in items:
        doi=None
        _id = it.get("id")
        if isinstance(_id, str) and _id.lower().startswith("10."):
            doi=_id.lower()
        key = doi or ((it.get("title") or "").strip().lower(), it.get("year"))
        if key in seen:
            removed += 1
            continue
        seen.add(key)
        out.append(it)
    return out, {"dedup_removed": removed}
