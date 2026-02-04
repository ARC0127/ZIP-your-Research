# 07 First-turn Application Guide v1.0.1

## Minimal user action
1) Upload the ZIP.
2) Optional: paste a MIGRATION PROMPT (English) if you are resuming a previous chat.
3) Otherwise: say “start” (or say nothing).

## Defaults (if you don't override)
```yaml
SESSION_OVERRIDES:
  top_priorities: [A_logic, B_method, C_calculation, E_innovation_correctness]
  intake_depth: deep              # tight | standard | deep
  strictness: high
  output_mode: audit_first        # audit_first | rewrite_first | mixed
  citation_mode: conservative     # conservative | normal
  web_browsing_policy: ALLOW      # default is ALLOW
  debug_trace: OFF                # default is OFF (only ON if you explicitly request)
```

## What happens next
- You answer the intake questions (A/B/C/E ask 5 questions in deep mode; others ask 3).
- I will generate MODE_LOCK.md + MODE_LOCK.json.
- You reply **CONFIRM**.
- Then I execute tasks under the lock.

## Readability guarantee
By default, I will NOT show any internal routing metadata.
If you explicitly send `DEBUG_TRACE=ON`, I will append a short Debug Trace section.


## Pre-lock behavior (to prevent drift)
- Before you reply `CONFIRM`, I will **not** execute substantive research work (no literature summary, no novelty conclusions, no proofs).
- If you send a task request early (e.g., “check world model novelty”), I will treat it as **scope selection** and ask only the minimal intake questions needed to lock that mode.
- Web browsing is **disabled during bootstrap/intake**, and starts only **after Mode Lock is confirmed** (even if default policy is ALLOW).
