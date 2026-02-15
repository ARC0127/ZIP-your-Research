# Prompt Regression (LOCKED protocol)

This repo includes a small, deterministic regression harness to keep **MODE_LOCK / LOCKED scope handling** stable under user perturbations.

## Files

- Corpus (JSONL): `tests/prompt_regression/corpus_v1_3.jsonl`
- Schema (JSON): `tests/prompt_regression/corpus_schema_v1_3.json`
- Validator: `tools/validate_corpus_v1_3.py`
- Simulator: `tools/simulate_locked_regression_v1_3.py`

## Corpus entry schema (v1.3)

Each line is a JSON object with **required** fields:

- `id`: unique string
- `label`: one of `IN_SCOPE | OUT_OF_SCOPE | CHANGE_REQUEST | INJECTION`
- `focus`: routing hint (e.g., `A_logic`)
- `text`: user message used for the perturbation test

## How to run

```bash
python tools/validate_corpus_v1_3.py
python tools/simulate_locked_regression_v1_3.py --n 25 --seed 0
```

The simulator is *not an LLM*. It checks the **protocol contract** only:
`[LOCKED][SCOPE=<LABEL>] ...`

The report is written to:
`artifacts/locked_regression/report_v1.3.2.md`
