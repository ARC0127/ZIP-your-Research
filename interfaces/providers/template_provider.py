"""
Template Provider — copy and rename this file to implement your own provider.
"""
from __future__ import annotations
from typing import Dict, Any
import time

def search(query: str, *, limit: int = 10, config: Dict[str, Any] | None = None) -> Dict[str, Any]:
    config = config or {}
    # Implementation note: fetch data from the provider and normalize into the common items list schema.
    # This template is intentionally complete at the interface level; you only need to fill the HTTP calls.
    items = [{
        "title": f"[TEMPLATE] {query}",
        "year": None,
        "venue": None,
        "authors": None,
        "url": None,
        "id": None,
        "abstract": None,
        "cited_by": None,
        "extra": {"note":"replace with real implementation"}
    }]
    return {"provider":"template","query":query,"items":items,"meta":{"warnings":["template provider"],"ts":time.time()}}
