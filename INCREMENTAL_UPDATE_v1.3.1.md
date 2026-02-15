# Incremental Update v1.3.1

**Delta since v1.3.0** (clean-up + protocol regression simulation).

## Removed (de-bloat)
- Unused embedded archive (not referenced anywhere): `ZIP-your-Research_v1.3_release.zip` (~68KB)
- Legacy v1.2 artifacts that caused confusion / dead references:
  - `boot/*_v1.2.md`
  - skills/coding_engine/MASTER_v1.2.md
  - tests/prompt_regression/corpus_v1_2.jsonl, tests/prompt_regression/fuzz_payloads_v1_2.bin
  - INCREMENTAL_UPDATE_v1.2.md, AUTOBOOT_v1.0.1.md

## Renamed (canonical)
- tools/validate_v1_2.py → `tools/validate_v1_3.py`
- tools/drift_audit_v1_2.py → `tools/drift_audit_v1_3.py`

## Fixed
- Router now points to `skills/coding_engine/MASTER_v1.3.md` (no more v1.2 master path).
- coding_engine module header cleaned to avoid conflicting headings.
- CI & docs updated to reference `validate_v1_3.py` and `drift_audit_v1_3.py`.

## Added
- Deterministic LOCKED perturbation simulator:
  - `python tools/simulate_locked_regression_v1_3.py --n 25 --seed 0`
  - Output: `artifacts/locked_regression/report_v1.3.1.md`

## Commands
```bash
python tools/build_all.py
python tools/validate_v7_2.py
python tools/drift_audit_v1_3.py
python tools/simulate_locked_regression_v1_3.py --n 25 --seed 0
```
