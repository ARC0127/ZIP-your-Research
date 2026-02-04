from __future__ import annotations
from typing import Dict, Any, List
import os
from ._http_utils import http_get_json, q

def search(query: str, *, limit: int = 10, config: Dict[str, Any] | None = None) -> Dict[str, Any]:
    config = config or {}
    base_url = (config.get("base_url") or "https://api.openalex.org").rstrip("/")
    api_key_env = config.get("api_key_env") or "OPENALEX_API_KEY"
    api_key = os.getenv(api_key_env, "")
    timeout_s = int(config.get("timeout_s") or 30)
    select = config.get("select")  # optional optimization

    warnings: List[str] = []
    if not api_key:
        warnings.append(f"Missing OpenAlex API key env var: {api_key_env}")

    url = f"{base_url}/works?search={q(query)}&per-page={max(1,min(200,limit))}"
    if api_key:
        url += f"&api_key={q(api_key)}"
    if select:
        url += f"&select={q(select)}"

    data, err = http_get_json(url, timeout_s=timeout_s)
    if err or not data:
        return {"provider":"openalex","query":query,"items":[], "meta":{"warnings":warnings + ([err] if err else []), "raw_url":url}}

    items=[]
    for w in (data.get("results") or [])[:limit]:
        # OpenAlex uses display_name etc; keep best-effort
        title = w.get("display_name") or w.get("title") or ""
        year = w.get("publication_year")
        cited = w.get("cited_by_count")
        doi = w.get("doi")
        url_out = (w.get("id") or w.get("openalex_id") or w.get("url") or doi)
        venue = None
        hv = w.get("host_venue") or {}
        venue = hv.get("display_name") or hv.get("publisher")
        authors=None
        auths = w.get("authorships")
        if isinstance(auths, list):
            authors=[]
            for a in auths:
                au = (a.get("author") or {}).get("display_name")
                if au:
                    authors.append(au)
        items.append({
            "title": title,
            "year": year,
            "venue": venue,
            "authors": authors,
            "url": url_out,
            "id": doi or w.get("id"),
            "abstract": None,
            "cited_by": cited,
            "extra": {"openalex_id": w.get("id")}
        })

    return {"provider":"openalex","query":query,"items":items,"meta":{"warnings":warnings, "raw_url":url}}
