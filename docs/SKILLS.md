# Skills Catalog (v1.3.2)

> 新手只看这一页：先学会 **FOCUS（A–J）** + **ONECHAT** 的最短闭环。

本仓库的目标不是“随便聊天”，而是把科研工作流拆成可复用的 **skills**，并用 **MODE_LOCK/LOCKED** 机制在用户扰动下保持稳定执行。

## A. FOCUS domains（你在 intake 里选择的“关注维度”）

> 这 10 个 domain 的**权威定义**在：`router/intake_profile_v1.3.2.yaml`（含推荐提问模板与主技能）。

- **A_logic**：思路/逻辑一致性核查（主技能：S226）
- **B_method**：方法正确性核查（主技能：S227）
- **C_calculation**：计算/推导/数值核查（主技能：S326）
- **D_paper_story**：论文整体叙事与贡献图谱（主技能：S229）
- **E_innovation_correctness**：创新正确性审计（主技能：S233）
- **F_proof_idea**：证明路线与缺口定位（主技能：S230 / S235）
- **G_novelty_search**：查新策略与对比框架（主技能：S231 / S234）
- **H_experiment_completeness**：实验完整性（主技能：S327 / S328）
- **I_paper_interpretation**：论文精读与面试式问答（主技能：S232）
- **J_sentence_rewrite_retrieval**：句子改写 + 风险审计（主技能：S526 / S527）

完整技能清单看：`INDEX.md`（自动生成，按目录列出所有 Sxxx）。

## B. 最短上手（10 分钟）

1) **只做 intake，不执行**：按 `boot/00_BOOTSTRAP_PROTOCOL_v1.3.2.md` 走到 CONFIRM。
2) 选一个 FOCUS（例如 A_logic），给最小材料范围（段落/公式/实验表）。
3) 回复 `CONFIRM` 后进入 LOCKED：严格按 `boot/10_LOCKED_SCOPE_GUARD_v1.3.md` 执行。

## C. ONECHAT 闭环（单对话最大化 GPT 能力）

ONECHAT 是“单个 ChatGPT 对话”下的科研闭环模板：

- Ideation：S201–S214
- Planning：S301–S308
- Experiment：S430–S432 + S421
- Writing：`skills/writing_engine/MASTER_v1.3.2.md`
- Review：S424 + S432
- Ops：S407 + S428 + `artifacts/release_checklist.md`

入口说明：`docs/ONBOARDING_FASTPATH_v1.3.md`、`boot/12_ONECHAT_DEEP_LOOP_v1.3.md`。

## D. Prompt Regression（抗扰动稳定性）

LOCKED 的“不会跑偏”依赖一套可复现测试：

- Corpus：`tests/prompt_regression/corpus_v1_3.jsonl`
- Schema：`tests/prompt_regression/corpus_schema_v1_3.json`
- Validator：`tools/validate_corpus_v1_3.py`
- Simulator：`tools/simulate_locked_regression_v1_3.py`

详见：`docs/PROMPT_REGRESSION.md`
