from __future__ import annotations
from typing import Dict, Any, List
import xml.etree.ElementTree as ET
from ._http_utils import http_get_text, q

NS = {"atom":"http://www.w3.org/2005/Atom"}

def search(query: str, *, limit: int = 10, config: Dict[str, Any] | None = None) -> Dict[str, Any]:
    config = config or {}
    base_url = (config.get("base_url") or "https://export.arxiv.org/api/query").rstrip("/")
    timeout_s = int(config.get("timeout_s") or 30)
    warnings: List[str] = []

    url = f"{base_url}?search_query=all:{q(query)}&start=0&max_results={max(1,min(100,limit))}&sortBy=submittedDate&sortOrder=descending"
    text, err = http_get_text(url, timeout_s=timeout_s, headers={"User-Agent":"ZIP-your-Research/1.0"})
    if err or not text:
        return {"provider":"arxiv","query":query,"items":[], "meta":{"warnings":warnings + ([err] if err else []), "raw_url":url}}

    items=[]
    try:
        root = ET.fromstring(text)
        for entry in root.findall("atom:entry", NS)[:limit]:
            title = (entry.findtext("atom:title", default="", namespaces=NS) or "").strip().replace("\n"," ")
            summary = (entry.findtext("atom:summary", default="", namespaces=NS) or "").strip()
            published = entry.findtext("atom:published", default="", namespaces=NS)
            year = int(published[:4]) if published and published[:4].isdigit() else None
            # id is a URL
            id_url = entry.findtext("atom:id", default="", namespaces=NS)
            authors = [a.findtext("atom:name", default="", namespaces=NS) for a in entry.findall("atom:author", NS)]
            authors = [a for a in authors if a]
            items.append({
                "title": title,
                "year": year,
                "venue": "arXiv",
                "authors": authors or None,
                "url": id_url or None,
                "id": id_url.split("/")[-1] if id_url else None,
                "abstract": summary or None,
                "cited_by": None,
                "extra": {"published": published}
            })
    except Exception as e:
        warnings.append(f"XML parse error: {e}")

    return {"provider":"arxiv","query":query,"items":items,"meta":{"warnings":warnings, "raw_url":url}}
