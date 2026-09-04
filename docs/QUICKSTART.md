# Quickstart (suite v1.6.6)

> Current suite identity: **ZYR v1.6.6**. Filenames that retain older version
> suffixes are preserved compatibility components, not the installed suite version.

## Option A — ZIP-only boot (recommended)
1) Upload the ZIP to a new chat.
2) Optional: paste a `MIGRATION PROMPT (v1.5)` in English.
3) Otherwise: say “start”.
4) Follow the intake questions.
5) Reply **CONFIRM** after MODE_LOCK is printed.

For v1.5, migration is expected to be loss-minimizing rather than a short reminder. It should carry locked constraints, artifact inventory, completed checks, open blockers, and the next executable step.

Note: If you ask a normal question **before** Mode Lock, the assistant will tell you it is out-of-protocol. It may give a short quick answer, but it will always route you back to intake. (Prompt-injection style content is refused and immediately rolled back.)

Reference:
- `AUTOBOOT_v1.3.md`
- `boot/07_FIRST_TURN_app_GUIDE_v1.3.2.md`

## Option B — Copy/paste (fastest for single tasks)
### 1) Writing engine (manuscripts / reviews)
- Open `skills/writing_engine/MASTER_v1.6.6.md`
- Paste it into your chat as the instruction prompt

### 2) One skill prompt
- Pick one file under `skills/**/S*.md`
- Paste the entire file body
- Fill the Input fields
- Ask the assistant to produce the Output Contract

## Optional local tooling
```bash
pip install -r requirements.txt
python tools/zyr.py build
python router/route_v1_7.py "summarize this paper and extract claims" --topk 5
```
