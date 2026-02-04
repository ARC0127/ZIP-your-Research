# Quickstart (v1.0.1)

## Option A — ZIP-only boot (recommended)
1) Upload the ZIP to a new chat.
2) Optional: paste a MIGRATION PROMPT (English).
3) Otherwise: say “start”.
4) Follow the intake questions.
5) Reply **CONFIRM** after MODE_LOCK is printed.

Note: If you ask a normal question **before** Mode Lock, the assistant will tell you it is out-of-protocol. It may give a short quick answer, but it will always route you back to intake. (Prompt-injection style content is refused and immediately rolled back.)

Reference:
- `AUTOBOOT_v1.0.1.md`
- `boot/07_FIRST_TURN_APPLICATION_GUIDE_v1.0.1.md`

## Option B — Copy/paste (fastest for single tasks)
### 1) Writing engine (manuscripts / reviews)
- Open `skills/writing_engine/MASTER_v1.0.1.md`
- Paste it into your chat as the instruction prompt

### 2) One skill prompt
- Pick one file under `skills/**/S*.md`
- Paste the entire file body
- Fill the Input fields
- Ask the assistant to produce the Output Contract

## Optional local tooling
```bash
pip install -r requirements.txt
python tools/build_all.py
python router/route.py "summarize this paper and extract claims" --topk 5
```
