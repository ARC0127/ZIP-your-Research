# Release packaging (v1.3.2)

This project is optimized for **copy/paste** usage. For distribution, you often want a zip that excludes repo history (`.git`) and caches.

## One-command release zip
From the repository root:

```bash
python tools/build_all.py
python tools/validate_v7_2.py
python tools/make_release.py --version v1.3.2
```

This creates:

- `ZIP-your-Research_v1.3.2_release.zip`

## Why exclude `.git`?
- Smaller downloads
- Less confusion for users who only want prompts
- Avoid accidentally shipping secrets in git history (still: do not commit secrets)

## CI recommendation
Keep `.github/workflows/ci_v7_2.yml` enabled so generated artifacts (INDEX and MASTER) remain in sync.

---

## v1.2 recommended commands (drift-free)

From repo root:

```bash
python tools/build_all.py
python tools/validate_v7_2.py
python tools/make_release.py --version v1.2
```

Notes:
- `tools/validate_v7_2.py` is now a shim to the strict validator `tools/validate_v1_3.py`.
- CI should run strict validation to prevent doc/tool drift.


---

## v1.3 recommended commands (ONECHAT + onboarding)

From repo root:

```bash
python tools/build_all.py
python tools/validate_v7_2.py
python tools/gen_skills_catalog_v1_3.py
python tools/make_release.py --version v1.3
```

This creates:
- `ZIP-your-Research_v1.3_release.zip`

Notes:
- `build_all.py` will additionally generate `MASTER_v1.3` prompts if present.
- The release should include the v1.3 onboarding docs and regression corpus.
