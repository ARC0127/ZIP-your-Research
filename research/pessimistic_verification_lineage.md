# Pessimistic Verification Lineage (v1.5)

## Purpose
- 这份文档服务于 ZYR v1.5 的 `理论推导审计` 与 `数学证明审计` 增强。
- 它不是一份“数学 benchmark 摘要”，而是一份 `proof audit / derivation audit / refinement loop / formal adapter` 的机制转译文档。
- 主问题只有一个：`Pessimistic Verification for Open-Ended Math Questions` 里哪些机制应该被 ZYR 吸收，哪些不应该。

## Source Basis

### Local primary sources
- 本地 PDF: `/home/arc/TRAIN/ZYR/2511.21522v1.pdf`
- 本地源码 archive: `/home/arc/TRAIN/ZYR/pverify-main.zip`
- 已核对的实现入口:
  - archive member utils/verifiers.py
  - archive member utils/prover_pipeline.py
  - archive member main.py

### External primary sources
- Anchor paper: [Pessimistic Verification for Open Ended Math Questions](https://arxiv.org/abs/2511.21522)
- Benchmark line:
  - [Hard2Verify: A Step-Level Verification Benchmark for Open-Ended Frontier Math](https://arxiv.org/abs/2510.13744)
  - [Scaling Flaws of Verifier-Guided Search in Mathematical Reasoning](https://arxiv.org/abs/2502.00271)
  - [Improving Value-based Process Verifier via Low-Cost Variance Reduction](https://arxiv.org/abs/2508.10539)
  - [Asking LLMs to Verify First is Almost Free Lunch](https://arxiv.org/abs/2511.21734)
- System/context line:
  - [AI Mathematician: Towards Fully Automated Frontier Mathematical Research](https://arxiv.org/abs/2505.22451)
- Formal-adapter line:
  - [StepProof: Step-by-step verification of natural language mathematical proofs](https://arxiv.org/abs/2506.10558)
  - [Goedel-Prover: A Frontier Model for Open-Source Automated Theorem Proving](https://arxiv.org/abs/2502.07640)
  - [Goedel-Prover-V2: Scaling Formal Theorem Proving with Scaffolded Data Synthesis and Self-Correction](https://arxiv.org/abs/2508.03613)
  - [Leanabell-Prover-V2: Verifier-integrated Reasoning for Formal Theorem Proving via Reinforcement Learning](https://arxiv.org/abs/2507.08649)
  - [APOLLO: Automated LLM and Lean Collaboration for Advanced Formal Reasoning](https://arxiv.org/abs/2505.05758)

## What Is Confirmed from the Anchor Paper
- 锚论文作者与机构在本地 PDF 首面可确认：Qiuzhen College、Dept. of Computer Science & Technology / Institute for AI、Institute for AI Industry Research (AIR)，均与清华大学关联。
- 锚论文明确提出三类 workflow:
  - simple pessimistic verification
  - vertical pessimistic verification
  - progressive pessimistic verification
- 核心思想不是“多投票取多数”，而是 `只要任何一次 review 发现致命错误，就把证明判成 false`。
- 论文的 case study 明确提醒：强模型上的部分 false negative 其实来自原 benchmark 的 annotation error 或 rigor requirement mismatch，而不一定是 verifier 真错。

## What Is Confirmed from the Local Repo
- archive member utils/verifiers.py 中的 `PessimisticVerifier` 明确写了 `FIRST review that reports an error ... as the final verdict for that proof`。
- 同一实现里保留 `last_majority_results`，说明 majority 被记录，但不是主判决。
- `VPessimisticVerifier` 把证明切成 line chunks，让 reviewer 聚焦局部 chunk，但仍保留 full problem 与 full proof 作为上下文。
- `ProgressivePessimisticVerifier` 实现了从 whole-proof 到 finer chunks 的多尺度检查。
- `PessimisticPruningVerifier` 实现了迭代 pruning，已经被判错的 proof 不再继续浪费后续 review 预算。
- archive member utils/prover_pipeline.py 的 `ProverPipeline` 不是只验证，它还做 reviewer feedback 驱动的 proof refinement，然后重新验证修订版 proof。

## Mechanism Extraction Table
| Paper claim | Repo implementation | Adopted in ZYR | Not adopted | Open question |
|---|---|---|---|---|
| `first-error-wins` 比 majority 更适合 proof verification | `PessimisticVerifier` 先找首个 negative review，再给 final verdict；majority 单独记录在 `last_majority_results` | `S240`、`S241`、`proof_engine`、`tests/proof_verification_v1_5/` 均采用 `first-error-wins` | 不把 majority 作为主 verdict | 未来是否需要区分 `fatal` 与 `correctable major` 两级 negative |
| 同一 proof 上做多次并行 review 能提高 error detection | `--reviewer pessimistic` + `--reviews` in `main.py` | `S240` 规定同一 proof 做 `n` 次 parallel review | 不复制 pverify 的 CLI / dataset workflow | ZYR 默认 `n` 应该是固定值还是由 proof length 自适应 |
| Vertical review 应该聚焦 chunk，但不能丢 full proof context | `VPessimisticVerifier` 按 chunk_length 切 proof，同时仍提供 full problem/full proof | `S241` 强制 `chunk review with full context retained` | 不把 chunk verdict 误当全局 verdict | ZYR 是否需要对长 proof 再加入 lemma-aware chunking |
| Progressive multiscale verification 可以先粗看、再细查 | `ProgressivePessimisticVerifier` 逐步细化 chunk granularity | `S241` 与 `proof_engine` 采用 `whole proof -> chunk drill-down` | 不直接复制原 repo 的所有迭代超参 | 未来是否按 theorem type 自适应 chunk policy |
| Pruning 可节约预算 | `PessimisticPruningVerifier` 对已判错样本停止继续评审 | `S241` 输出 `pruned_branch_list` | 不做 benchmark-oriented token optimization | ZYR 需要记录多少 pruning diagnostic 才够用 |
| Negative review 必须给 error explanation | verifiers 的 prompt 要求错误时返回 concise harmful error | `S240` / `S241` / `S235` 要求 negative verdict 附解释 | 不接受裸 `false` 无解释 | 是否要再强制定位到 lemma / line / assumption |
| Annotation error / rigor mismatch 需要单独标注 | 论文 case study 明示大量 false negative 其实是 annotation / rigor 问题 | `proof_verification_profile.annotation_or_rigor_mismatch_label=enabled`，并在 `S240` / `S241` 中保留 `verification_incomplete` | 不强行二值化所有 proof | 后续是否把这类情况单独抽成 fourth status |
| Verification 与 proof generation 可以形成 refinement loop | `ProverPipeline` 读取 reviewer feedback，生成 corrected self-contained proof，再继续 verify | `proof_engine` 增加 reviewer-feedback refinement loop；`refinement suggestion` 与 `verified` 严格分离 | 不把 ZYR 变成 autonomous theorem proving loop | 未来是否需要把 refinement 预算写进 MODE_LOCK |
| Token-efficient test-time scaling 可优于长 CoT | 论文实验声称 simple / progressive pessimistic methods 的 test-time efficiency 可优于 extended long-CoT | ZYR 借鉴的是 verification ordering，不是 benchmark token race | 不围绕 benchmark token efficiency 优化协议 | 用户任务中的最优 review budget 如何选 |

## Verification / Benchmark Contrast Line
| Work | Core idea | 对 ZYR proof audit / derivation audit / refinement loop / formal adapter 的启发 | Adopt / Adapt / Reject |
|---|---|---|---|
| [Hard2Verify](https://arxiv.org/abs/2510.13744) | step-level benchmark，要求定位 first error 或提供 step annotations | 直接启发 `S235 step_verdict_table`、`S326 first_failing_line`、`tests/proof_verification_v1_5/` 的场景设计 | `Adopt` |
| [Scaling Flaws of Verifier-Guided Search](https://arxiv.org/abs/2502.00271) | verifier-guided search 会因 misranking / pruning 产生 scale flaws | 告诉 ZYR 不能把 verifier 当万能 oracle；proof_engine 只能做 verification gate，不能自动主导大规模 search | `Adopt` |
| [Improving Value-based Process Verifier via Low-Cost Variance Reduction](https://arxiv.org/abs/2508.10539) | process verifier 的噪声很多来自高方差估计 | 启发 ZYR 在 `verification_record` 里显式记录 unresolved / noisy 部分，而不是假装 verdict 很稳 | `Adapt` |
| [Asking LLMs to Verify First is Almost Free Lunch](https://arxiv.org/abs/2511.21734) | 先验证再生成，作为低成本 reverse reasoning trick | 可以作为 ZYR prompt-level启发，但不足以替代 `S240/S241` 的 artifact-level审计 | `Adapt` |

## System / Context Line
| Work | Core idea | 对 ZYR 的明确启发 | Adopt / Adapt / Reject |
|---|---|---|---|
| [AI Mathematician](https://arxiv.org/abs/2505.22451) | 探索机制 + pessimistic reasonable verification，用于研究级数学任务 | 说明 pessimistic verification 不是孤立技巧，而是大系统里的核心可靠性 gate；ZYR 借鉴 gate，不借鉴 autonomous research ambition | `Adapt` |

## Formal-Adapter Line
| Work | Core idea | 对 ZYR formal adapter 的明确启发 | Adopt / Adapt / Reject |
|---|---|---|---|
| [StepProof](https://arxiv.org/abs/2506.10558) | 把自然语言 proof 拆成多个可验证 subproof，做 step-by-step autoformalization | 直接启发 `S433` 的 `autoformalization_candidates` 与细粒度 subproof decomposition；也支持 `S235` 的 step verdict 表 | `Adapt` |
| [Goedel-Prover](https://arxiv.org/abs/2502.07640) | 大规模 formal statement/proof synthesis，目标是 Lean 4 formal proof generation | 告诉 ZYR formal adapter 应输出 theorem normalization、lemma inventory、Lean sketch，但 ZYR 不承担 formal proof 生成目标 | `Adapt` |
| [Goedel-Prover-V2](https://arxiv.org/abs/2508.03613) | scaffolded data synthesis + self-correction，强化 formal proving | 对 ZYR 的最有价值启发是 `formal self-correction` 与 `compiler-like feedback` 可以进入 adapter，但必须保持 optional | `Adapt` |
| [Leanabell-Prover-V2](https://arxiv.org/abs/2507.08649) | verifier-integrated reasoning + RL + multi-turn feedback | 启发 `formal adapter` 与 `refinement loop` 的接口设计：formal verifier feedback 可以作为附加证据，但不能污染自然语言主 verdict | `Adopt` |
| [APOLLO](https://arxiv.org/abs/2505.05758) | Lean compiler + LLM + proof repair pipeline，在低采样预算下反复修补 formal proof | 启发 ZYR 把 `formal repair` 作为未来可选子流程；当前仅吸收 `repair then re-verify` 的接口思想 | `Adapt` |

## ZYR v1.5 Translation

### Protocol layer
- `boot/04_MODE_LOCK_FORMAT_v1.3.2.md`
  - 新增 `Proof Verification Profile`
  - 默认：
    - `verifier_mode: pessimistic_progressive`
    - `first_error_wins: true`
    - `proof_refinement_loop: on`
    - `majority_vote: diagnostic_only`
    - `formal_adapter: optional`
    - `annotation_or_rigor_mismatch_label: enabled`
- 路由保持现有 `C_calculation` 与 `F_proof_idea` 顶层 focus，不新增字母，但新增 `proof_engine` 作为 composite candidate

### Skill layer
- 新增:
  - `S237_theorem_assumption_normalizer`
  - `S240_pessimistic_proof_verification`
  - `S241_progressive_proof_verification`
  - `S433_formal_proof_adapter`
  - `skills/proof_engine/`
- 强化:
  - `S230` 加 theorem normalization / lemma dependency graph / falsification matrix
  - `S235` 加 step verdict / first failing step / gap severity / alternative routes
  - `S326` 加 derivation ledger / local verdict / counterexample pack / first failing line

### Test layer
- 新增 `tests/proof_verification_v1_5/`
- 当前 proof regression 覆盖:
  - majority 误放过但单个 fatal negative 成立
  - theorem condition mismatch
  - long proof 局部 derivation error
  - missing lemma / unjustified step
  - annotation / rigor mismatch
  - harmless typo vs fatal flaw
  - refinement then re-verify
  - formal adapter requested but unavailable

## Adopt / Adapt / Reject Summary

### Adopt
- `first-error-wins`
- `parallel pessimistic review`
- `vertical review with full-context retention`
- `progressive multiscale verification`
- `majority vote diagnostic only`
- `error explanation required`
- `annotation_or_rigor_mismatch_label`
- `refinement must re-verify before verified`

### Adapt
- `formal adapter`
- `compiler/verifier feedback as auxiliary signal`
- `proof repair loop`
- `step-level autoformalization ideas`

### Reject
- 直接 vendoring pverify benchmark / CLI / dataset workflow
- 把 ZYR 变成 autonomous theorem proving system
- 让 formal proof adapter 反向控制自然语言主 verdict
- 用 majority 或 “大部分看起来对” 覆盖单个 fatal flaw

## Bottom Line
- 对 ZYR 来说，`Pessimistic Verification` 最重要的价值不是“数学能力更强”，而是把 proof verification 从“乐观背书器”改造成“悲观拒绝器”。
- 这条线和 ZYR v1.5 的 `completion-first` 并不冲突；它真正补上的，是 `完成任务` 之前必须先过 `proof / derivation verification gate`。
- 因此 ZYR 在 1.5 的证明增强主线被明确锁定为：
  - `natural-language verification first`
  - `first-error-wins`
  - `proof repair must re-verify`
  - `formal adapter is optional and non-blocking`
