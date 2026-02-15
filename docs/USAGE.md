# Usage (v1.3.2)

This repository supports two modes:

## 1) ZIP-only boot + Mode Lock (recommended for multi-step projects)
- Upload the ZIP.
- Run intake.
- Generate MODE_LOCK.
- Reply CONFIRM.
This yields stable behavior across a long research session (no drift).

### Pre-lock behavior (important)
If you ask a question **before** Mode Lock is confirmed, the assistant must:
1) **Explicitly tell you** your message is out-of-protocol (pre-lock),
2) Optionally provide a **short, conservative quick answer** (for normal questions),
3) Then **return to intake** and wait for your answers.

Prompt-injection / malicious content is refused and always rolled back to intake without answering.

## 2) Copy/paste prompts (recommended for quick single tasks)
Each `skills/**/S*.md` file contains:
- YAML front matter (metadata)
- A self-contained prompt body you can paste into ChatGPT

### Fast path
1) Manuscript / reviews / venue constraints:
   - Use `skills/writing_engine/MASTER_v1.3.2.md`
2) Single task (ablation plan, repro audit, method check):
   - Pick a skill and paste it as-is.

## Defaults that matter
- Web browsing policy: **ALLOW** by default (unless explicitly forbidden).
- Readability: no debug YAML in user-visible output by default.

See:
- `boot/04_MODE_LOCK_FORMAT_v1.3.2.md`
