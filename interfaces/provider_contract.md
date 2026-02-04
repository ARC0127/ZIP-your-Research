# Provider Contract (stable in 1.0.x)

A Provider is a small Python module that implements a single function:

```python
def search(query: str, *, limit: int, config: dict) -> dict:
    ...
```

## Requirements
- Must return a JSON-serializable dict with keys:
  - `provider`: str
  - `query`: str
  - `items`: list[dict]
  - `meta`: dict (optional: rate_limit_notes, warnings, raw_url)
- Each item should be shaped as:
  - `title`: str
  - `year`: int | None
  - `venue`: str | None
  - `authors`: list[str] | None
  - `url`: str | None
  - `id`: str | None (DOI/arXiv id/OpenAlex id/etc)
  - `abstract`: str | None (if available)
  - `cited_by`: int | None (if available)
  - `extra`: dict (provider-specific)

## Config + secrets
- Providers read their settings from the `config` argument.
- Secrets (API keys) should be passed via environment variables and referenced in config by name.

## Reliability
- Use timeouts (default 30s).
- Never crash on partial failures; return `warnings` in meta and best-effort results.
