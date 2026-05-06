from __future__ import annotations
from typing import Dict, Any, Optional, Tuple
import json, urllib.parse, urllib.request

def http_get_json(url: str, *, headers: Dict[str,str] | None = None, timeout_s: int = 30) -> Tuple[Optional[Dict[str,Any]], Optional[str]]:
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            data = resp.read().decode("utf-8", errors="replace")
        return json.loads(data), None
    except Exception as e:
        return None, str(e)

def http_get_text(url: str, *, headers: Dict[str,str] | None = None, timeout_s: int = 30) -> Tuple[Optional[str], Optional[str]]:
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            data = resp.read().decode("utf-8", errors="replace")
        return data, None
    except Exception as e:
        return None, str(e)

def q(s: str) -> str:
    return urllib.parse.quote(s, safe="")
