from __future__ import annotations
from typing import Dict, Any, List
from ._http_utils import http_get_json, q

def search(query: str, *, limit: int = 10, config: Dict[str, Any] | None = None) -> Dict[str, Any]:
    config = config or {}
    base_url = (config.get("base_url") or "https://api.crossref.org").rstrip("/")
    mailto = config.get("mailto") or ""
    timeout_s = int(config.get("timeout_s") or 30)

    warnings: List[str] = []
    if not mailto:
        warnings.append("Crossref mailto not set; consider adding it for polite pool access.")

    url = f"{base_url}/works?query.bibliographic={q(query)}&rows={max(1,min(1000,limit))}"
    if mailto:
        url += f"&mailto={q(mailto)}"

    data, err = http_get_json(url, timeout_s=timeout_s, headers={"User-Agent":"ZIP-your-Research/1.0 (mailto:unknown)"})
    if err or not data:
        return {"provider":"crossref","query":query,"items":[], "meta":{"warnings":warnings + ([err] if err else []), "raw_url":url}}

    items=[]
    message = (data.get("message") or {})
    for it in (message.get("items") or [])[:limit]:
        title = ""
        tt = it.get("title")
        if isinstance(tt, list) and tt:
            title = tt[0]
        year=None
        issued = it.get("issued",{}).get("date-parts")
        if isinstance(issued, list) and issued and isinstance(issued[0], list) and issued[0]:
            year = issued[0][0]
        doi = it.get("DOI")
        url_out = it.get("URL")
        venue = None
        ct = it.get("container-title")
        if isinstance(ct, list) and ct:
            venue = ct[0]
        authors=None
        au = it.get("author")
        if isinstance(au, list):
            authors=[]
            for a in au:
                name = " ".join([x for x in [a.get("given"), a.get("family")] if x])
                if name.strip():
                    authors.append(name.strip())
        items.append({
            "title": title,
            "year": year,
            "venue": venue,
            "authors": authors,
            "url": url_out,
            "id": doi,
            "abstract": None,
            "cited_by": None,
            "extra": {"type": it.get("type")}
        })

    return {"provider":"crossref","query":query,"items":items,"meta":{"warnings":warnings, "raw_url":url}}
