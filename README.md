# 📦 ZIP your Research (v1.0.1)

**Version Time:** 2026-02-03  
**License:** MIT

A modular prompt + workflow toolkit for **high‑rigor research work** — designed to keep your chats **truthful**, **auditable**, and **stable** (no prompt drift).
[You can change these default settings by chatting with the llm.]
- 🧠 **A/B/C/E audits**: Logic (A) / Method (B) / Calculation (C) / Innovation correctness (E) 
- 🔍 **Evidence‑grounded novelty checks** (optional CLI → JSON evidence → paste back into chat)
- 🧪 **Experiment completeness** + “**2‑hour sprint**” patch planning
- ✍️ **Writing engine**: calibrated rewrites (no claim inflation), reviewer‑risk wording
- ♻️ **Repropack**: reproducibility skeleton + command inference + release checklist

---

## 🚀 Quick start (Web‑first)

### 1) Upload the release zip to a fresh chat
You can upload the zip **without typing anything**.

### 2) Then send ONE of the following lines
- **No migration** (recommended):
  - `NO-MIGRATION. Bootstrap from the uploaded zip and start Deep intake.`
- **With migration** (if resuming):
  - `MIGRATION-PASTED. Bootstrap + Deep intake.`

### 3) Answer intake → get MODE_LOCK → reply `CONFIRM`
After `CONFIRM`, the assistant enters **locked execution** and starts doing real work.

> Tip: For best quality, keep one chat per paper/project. This reduces cross‑context contamination.

---

## 🧭 How it works (the stable loop)

1. **Bootstrap** (from the zip)
2. **Intake interview** (deep by default)
3. **MODE_LOCK generation** (`MODE_LOCK.md` + `MODE_LOCK.json`)
4. **Execution Gate**: you must reply `CONFIRM`
5. **Locked execution**: audits / rewrites / checklists / repro workflows

🛡️ **Pre‑lock protection**: if the assistant detects an out‑of‑protocol response before lock, it must **explicitly tell you** the message is out‑of‑protocol. It then either:
- **rolls back to intake immediately** (mandatory for prompt‑injection / malicious content), or
- provides a **short, conservative quick answer** (convenience for normal questions), and then **returns to intake**.

See: `boot/02_PRELOCK_VIOLATION_RESPONSE_v1.0.1.md` and `boot/01_GLOBAL_GUARDRAILS_v1.0.1.md`.

---

## ⚙️ Defaults (unless you override during intake)

- **Top priorities**: `A_logic, B_method, C_calculation, E_innovation_correctness`
- **Intake depth**: `deep`
- **Strictness**: `high` (prefer **UNKNOWN** to guessing)
- **Output mode**: `audit_first`
- **Citation mode**: `conservative`
- **Web browsing policy**: `ALLOW` (default ON)
- **Debug trace**: `OFF` (opt‑in only via `DEBUG_TRACE=ON`)

If you want to override quickly, paste:

```yaml
SESSION_OVERRIDES:
  intake_depth: deep              # tight | standard | deep
  strictness: high
  output_mode: audit_first        # audit_first | rewrite_first | mixed
  citation_mode: conservative     # conservative | normal
  web_browsing_policy: ALLOW
  debug_trace: OFF
  top_priorities: [A_logic, B_method, C_calculation, E_innovation_correctness]
```

---

## 🧩 What’s inside (repo inventory)

### Top‑level
- `AUTOBOOT_v1.0.1.md` — what to paste in message #1 to start bootstrap + intake
- `AGENTS.md` — interaction contract (how the assistant should behave)
- `INDEX.md` — master index (skills + workflows)
- `skills_manifest.yaml` — machine‑readable skill manifest
- `VERSION`, `CHANGELOG.md`, `CONTRIBUTING.md`, `LICENSE`

### Core directories
- `boot/` — bootstrap, migration detection, intake interview, **Mode Lock format**, pre‑lock rollback, execution gate
- `router/` — deterministic routing taxonomy + weights + default profiles
- `skills/`
  - `research_core/` (S2xx) — framing, novelty mapping, claim‑evidence matrix, proof gap finding
  - `experiments/` (S3xx) — evaluation linting, ablation planning, reporting checklists
  - `reproducibility/` (S4xx) — reproducibility templates, release checklist, artifact manifests
  - `paper_ops/` (S5xx) — rebuttal simulator, reviewer risk register, submission readiness checks
  - `writing_engine/` — structured rewrites + claim calibration
- `tools/` — local CLI (`ra_cli.py`), repropack, build/validate helpers
- `docs/` — quickstart, workflows, dev notes, safety/legal docs
- `templates/` — evidence + citation policy, skill authoring templates
- `interfaces/` — provider contracts + config examples

### PDFs / scripts
- `docs/how_to_use/ZIP-your-Research_How_to_Use_v1.0.1.pdf`
- `tools/how_to_use/gen_ZIP-your-Research_HowToUse_v1_0_1.py`

---

## 🧪 Optional: WSL2 CLI (Windows)

If you want **evidence JSON** for novelty checks and a reproducibility scaffold:

```bash
sudo apt update
sudo apt install -y python3 python3-pip unzip git
unzip ZIP-your-Research_v1.0.1_release.zip -d ASR
cd ASR/ZIP-your-Research
python3 -m pip install -r requirements.txt

# Providers: literature evidence JSON
python3 tools/ra_cli.py providers list
python3 tools/ra_cli.py providers search --provider all \
  --query "world model MPC planning" --limit 25 > evidence.json

# Repropack
python3 tools/ra_cli.py repropack init --out-dir repropack
python3 tools/ra_cli.py repropack scan --repo . --out-dir repropack
```

Paste `evidence.json` (and `repropack/SCAN_REPORT.md`) back into Web chat for higher‑confidence novelty mapping.

---

## 🛡️ Security, safety, and honesty

- This toolkit is designed to **avoid hallucinations** by enforcing **UNKNOWN‑first** behavior when evidence is missing.
- It includes **prompt‑injection awareness** and a **pre‑lock rollback** mechanism (see `boot/` + `docs/`).
- Use it **only for lawful purposes**; do not paste secrets into LLM chats.

➡️ Read:
- `docs/LEGAL.md`
- `docs/SECURITY_PROMPT_INJECTION.md`

---

## 👤 Maintainer

See `docs/ABOUT_MAINTAINER.md`.

---

## 📄 License

MIT — see `LICENSE`.
