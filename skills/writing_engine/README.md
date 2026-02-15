# Writing Engine (legacy pack → v1.3.2 wrapper)

This pack preserves the original legacy modules (legacy) and exposes a single **MASTER_v1.3.2.md** for copy/paste use.

## How to use (copy/paste)
1) Run `python tools/build.py` to generate `skills/writing_engine/MASTER_v1.3.2.md`.
2) Copy `MASTER_v1.3.2.md` into your prompt or system instructions.

## Contents
- `modules/` — original legacy modules (legacy) (verbatim, unchanged)
- `legacy/` — legacy single-file prompts (verbatim)
- `MASTER_v1.3.2.md` — generated aggregate prompt

## v1.3.2.1 Addendum (incremental; nothing removed)

- **MASTER_v1.3.2.md is now generated and included** in this repository snapshot. You can copy/paste it directly.
- The `legacy` artifact in this repo is a **single file** (not a folder). For clarity, v1.3.2.1 also provides:
  - `legacy_master_prompt.md` (a copy of `legacy`) for tools that expect a `.md` suffix.

### Recommended usage (copy/paste)
- Fast path: open `MASTER_v1.3.2.md` and paste it into a new ChatGPT conversation as your "system" or "instructions" prompt.
- If you want modular control, paste only the modules you need from `modules/`.

### Invariants (kept)
- Module texts under `modules/` remain verbatim.
- Evidence policy remains strict: **no fabrication**; label UNKNOWN; propose verification steps.
