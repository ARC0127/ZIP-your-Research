# Writing Engine (suite v1.6.6; legacy modules preserved)

This pack preserves the original legacy modules verbatim and exposes **MASTER_v1.7.0.md** as the current copy/paste entrypoint.

## How to use (copy/paste)
1) Run `python tools/zyr.py build` to generate `skills/writing_engine/MASTER_v1.7.0.md`.
2) Copy `MASTER_v1.7.0.md` into your prompt or system instructions.

## Contents
- `modules/` — original legacy modules (legacy) (verbatim, unchanged)
- `legacy/` — legacy single-file prompts (verbatim)
- `MASTER_v1.7.0.md` — current generated aggregate prompt
- `MASTER_v1.3.2.md` — retained compatibility snapshot

## v1.3.2.1 Addendum (incremental; nothing removed)

- **MASTER_v1.3.2.md remains included** as a compatibility snapshot; use `MASTER_v1.7.0.md` for the current suite.
- The `legacy` artifact in this repo is a **single file** (not a folder). For clarity, v1.3.2.1 also provides:
  - `legacy_master_prompt.md` (a copy of `legacy`) for tools that expect a `.md` suffix.

### Recommended usage (copy/paste)
- Fast path: open `MASTER_v1.7.0.md` and paste it into a new ChatGPT conversation as your "system" or "instructions" prompt.
- If you want modular control, paste only the modules you need from `modules/`.

### Invariants (kept)
- Module texts under `modules/` remain verbatim.
- Evidence policy remains strict: **no fabrication**; label UNKNOWN; propose verification steps.
- Post-lock execution is completion-first: do not silently turn rewrite/review requests into advice, outline, or a smaller subset of the requested edits.
