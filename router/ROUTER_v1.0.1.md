# Router v1.0.1

This repository uses a **correctness-first routing taxonomy** to select skills.

## Domains (A–J)
- **A_logic**: logic/argument consistency audit  
- **B_method**: method correctness audit  
- **C_calculation**: calculation/derivation/numerical correctness  
- **D_paper_story**: paper storyline & contribution map  
- **E_innovation_correctness**: innovation feasibility & failure modes  
- **F_proof_idea**: proof skeleton / gap finding  
- **G_novelty_search**: novelty search or search plan (depends on web policy)  
- **H_experiment_completeness**: baselines/ablations/reporting completeness  
- **I_paper_interpretation**: deep reading & interview-style Q/A  
- **J_sentence_rewrite_retrieval**: rewrite + risk audit + retrieval

## Source of truth files
- Taxonomy: `router/taxonomy.yaml`
- Weights: `router/weights_v1.0.1.yaml`
- Intake interview: `router/intake_profile_v1.0.1.yaml`
- Readability policy: `boot/04_MODE_LOCK_FORMAT_v1.0.1.md`

## Deterministic router CLI
- Script: `router/route.py`
- Example:
  - `python router/route.py "请帮我做方法正确性核查" --topk 5`

**Important:** By default, routing metadata is internal. User-visible answers must be natural and readable.


## Pre-lock guardrail
Web browsing is disabled during bootstrap/intake. Routing decisions may be made, but execution starts only after CONFIRM.
