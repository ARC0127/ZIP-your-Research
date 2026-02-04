---
id: S429
name: deterministic_seed_logging_policy
category: reproducibility
triggers:
- seed policy
- deterministic
- logging schema
- randomness control
- 复现 日志 随机种子
inputs_required:
- framework_env
- randomness_sources
- logging_stack
outputs_required:
- policy_doc
- schema
- verification_record
quality_gates:
- no_fabrication
- mark_UNKNOWN
- audit_first
- copy_paste_ready
---

> **Global invariant (ZIP your Research):** Truthfulness • Trustworthiness • Deep logical reasoning. If required info is missing → mark **UNKNOWN** and ask minimal questions.

# S429 Deterministic Seed & Logging Policy (ML/RL)

## Role
Define a project-wide policy for seeds, logging, and metadata to support reproducibility.

## Input
- Framework (PyTorch/JAX/TF) and environment (RL sim)
- What randomness sources exist (init, data shuffling, env stochasticity)
- Logging stack (wandb/tensorboard/plain files)

## Output Contract
1) Seed policy (global + per-run) and where to set them.
2) Determinism notes (what cannot be deterministic and how to report it).
3) Logging schema (run_id, git hash, config, env version, metrics).
4) Artifact naming + directory conventions.
5) Minimal “reproduce one run” checklist.
6) Verification record.

## Rules
- Do not claim determinism if environment/hardware cannot guarantee it; mark UNKNOWN.
