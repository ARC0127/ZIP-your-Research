from __future__ import annotations

import json
import os
import urllib.parse
import unittest
from unittest import mock

from interfaces.providers import openalex


class OpenAlexRedactionTests(unittest.TestCase):
    def test_success_response_never_returns_api_key(self) -> None:
        secret = "openalex-" + ("S" * 32)
        captured: dict[str, str] = {}

        def fake_get(url: str, *, timeout_s: int):
            captured["url"] = url
            return {"results": []}, None

        with mock.patch.dict(os.environ, {"OPENALEX_API_KEY": secret}, clear=False):
            with mock.patch.object(openalex, "http_get_json", side_effect=fake_get):
                result = openalex.search("safe query", limit=2)

        self.assertIn(secret, captured["url"])
        rendered = json.dumps(result, ensure_ascii=False)
        self.assertNotIn(secret, rendered)
        parsed = urllib.parse.urlsplit(result["meta"]["raw_url"])
        self.assertEqual(urllib.parse.parse_qs(parsed.query)["api_key"], ["[REDACTED]"])

    def test_error_text_and_raw_url_are_redacted(self) -> None:
        secret = "openalex-" + ("E" * 32)

        def fake_get(url: str, *, timeout_s: int):
            return None, f"request failed for {url}"

        with mock.patch.dict(os.environ, {"OPENALEX_API_KEY": secret}, clear=False):
            with mock.patch.object(openalex, "http_get_json", side_effect=fake_get):
                result = openalex.search("failure query")

        rendered = json.dumps(result, ensure_ascii=False)
        self.assertNotIn(secret, rendered)
        self.assertIn("[REDACTED]", urllib.parse.unquote(rendered))

    def test_redact_url_covers_token_aliases(self) -> None:
        raw = "https://example.invalid/path?q=ok&token=secret-value&access_token=other-secret"
        safe = openalex.redact_url(raw)
        values = urllib.parse.parse_qs(urllib.parse.urlsplit(safe).query)
        self.assertEqual(values["q"], ["ok"])
        self.assertEqual(values["token"], ["[REDACTED]"])
        self.assertEqual(values["access_token"], ["[REDACTED]"])


if __name__ == "__main__":
    unittest.main()
