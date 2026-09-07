# Release packaging — ZYR v1.7.0

The current builder is `tools/make_release_v1_7.py`; its suffix identifies the
builder, not the suite release. `VERSION`, `v`, and `skills_manifest.yaml` must
agree. The [release policy](../manifests/release_policy.yaml) controls allowed,
required, excluded, and third-party files.

Use a clean checkout with committed source. Do not remove unrelated user files
to make a working directory appear clean; create an isolated checkout instead.

```bash
python -B tools/zyr.py build --check
python -B tools/validate_v7_3.py
python -B tools/zyr.py check --ci
python -B tools/zyr.py route-test
python -B tools/prune_retired_docs_v1.py --root . --check
python -B tools/make_release_v1_7.py --out /tmp/ZIP-your-Research_release.zip
python -B tools/zyr.py release-audit /tmp/ZIP-your-Research_release.zip
```

Choose an output path outside the checkout. GitHub CI also extracts the archive
and verifies the packaged CLI. It rejects secrets, missing required files, and
unlicensed third-party assets. A successful package check does not establish
scientific capability or full model-behavior quality.

## Document maintenance

Keep one current guide per purpose. Put the latest concrete update in the single
README update section; use Git history for superseded operation reports. Keep
actual skill dependencies, attribution, source provenance, and test fixtures.
Generated local reports should remain untracked unless they support a current
published result such as the [verified examples](SHOWCASE.md).

The exact retirement list and baseline hashes are in
`manifests/retired_documents_v1.json`. To remove matching obsolete copies from an
older checkout or installed suite, run the cleanup tool with that root and a new
backup directory. It refuses modified copies and does not remove skill modules.
Restore uses the recorded receipt; no Git history is rewritten.
