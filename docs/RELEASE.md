# Release packaging (v1.0.1)

This project is optimized for **copy/paste** usage. For distribution, you often want a zip that excludes repo history (`.git`) and caches.

## One-command release zip
From the repository root:

```bash
python tools/build_all.py
python tools/validate_v7_2.py
python tools/make_release.py --version v1.0.1
```

This creates:

- `ZIP-your-Research_v1.0.1_release.zip`

## Why exclude `.git`?
- Smaller downloads
- Less confusion for users who only want prompts
- Avoid accidentally shipping secrets in git history (still: do not commit secrets)

## CI recommendation
Keep `.github/workflows/ci_v7_2.yml` enabled so generated artifacts (INDEX and MASTER) remain in sync.
