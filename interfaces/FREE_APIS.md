# Free/Low-friction scholarly APIs you can plug into this pack

This prompt pack ships built-in providers for the APIs below. You can also add your own.

## OpenAlex (works search)
- Requires a **free API key** and uses the `api_key` query parameter.
- Credits/rate-limit model (free tier includes daily credits).
Docs: https://docs.openalex.org/  (see authentication and `api_key` usage). 

## Semantic Scholar Academic Graph API
- Many endpoints are available without authentication, but unauthenticated traffic is shared and can be throttled.
- Using a (free) API key gives you a dedicated rate limit.
Docs: https://api.semanticscholar.org/api-docs/

## Crossref REST API
- Public access is available with no auth.
- Using a `mailto` parameter is recommended for “polite pool” access and higher rate limits.
Docs: https://www.crossref.org/documentation/retrieve-metadata/rest-api/

## arXiv API
- Public API to search e-prints via the `export.arxiv.org/api/query` endpoint.
Docs: https://info.arxiv.org/help/api/

## How to add a new API (extension path)
1) Copy `interfaces/providers/_template_provider.py` → `interfaces/providers/my_provider.py`
2) Implement `search()`
3) Add config under `interfaces/config.yaml`
4) Test:
```bash
python3 tools/ra_cli.py providers search --provider my_provider --query "..." --limit 5
```

### Security note
Never commit API keys. Use environment variables (`*_API_KEY`) and reference them in config.
