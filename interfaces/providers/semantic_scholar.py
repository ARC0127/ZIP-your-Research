from __future__ import annotations
from typing import Dict, Any, List
import os
from ._http_utils import http_get_json, q

def search(query: str, *, limit: int = 10, config: Dict[str, Any] | None = None) -> Dict[str, Any]:
    config = config or {}
    base_url = (config.get("base_url") or "https://api.semanticscholar.org/graph/v1").rstrip("/")
    api_key_env = config.get("api_key_env") or "S2_API_KEY"
    api_key = os.getenv(api_key_env, "")
    timeout_s = int(config.get("timeout_s") or 30)
    fields = config.get("fields") or "title,year,venue,authors,url,abstract,citationCount,externalIds"

    warnings: List[str] = []
    headers = {"User-Agent":"ZIP-your-Research/1.0"}
    if api_key:
        headers["x-api-key"] = api_key
    else:
        warnings.append(f"No Semantic Scholar API key set in env {api_key_env} (optional but recommended).")

    url = f"{base_url}/paper/search?query={q(query)}&limit={max(1,min(100,limit))}&fields={q(fields)}"
    data, err = http_get_json(url, timeout_s=timeout_s, headers=headers)
    if err or not data:
        return {"provider":"semantic_scholar","query":query,"items":[], "meta":{"warnings":warnings + ([err] if err else []), "raw_url":url}}

    items=[]
    for p in (data.get("data") or [])[:limit]:
        title = p.get("title") or ""
        year = p.get("year")
        venue = p.get("venue")
        url_out = p.get("url")
        abs_ = p.get("abstract")
        cited = p.get("citationCount")
        authors=None
        au = p.get("authors")
        if isinstance(au, list):
            authors=[a.get("name") for a in au if a.get("name")]
        ext = p.get("externalIds") or {}
        doi = ext.get("DOI")
        pid = p.get("paperId")
        items.append({
            "title": title,
            "year": year,
            "venue": venue,
            "authors": authors,
            "url": url_out,
            "id": doi or pid,
            "abstract": abs_,
            "cited_by": cited,
            "extra": {"paperId": pid, "externalIds": ext}
        })

    return {"provider":"semantic_scholar","query":query,"items":items,"meta":{"warnings":warnings, "raw_url":url}}
