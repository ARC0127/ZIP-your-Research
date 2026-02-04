# v1.0.1 Intake Checklist (Deep)

Priority domains: **A_logic / B_method / C_calculation / E_innovation_correctness** (5 questions each)

Other domains: 3 questions each

Source of truth: `router/intake_profile_v1.0.1.yaml`

## A_logic — 思路/逻辑一致性核查
1. 你要核查的对象是什么：段落/推导/实验论证/整体story？请粘贴范围并给最小上下文。
2. 请列出你当前的核心 claim（1–3条），以及你认为支持它的证据/推理链在哪里。
3. 你认为最可能错在哪里？定义、前提、推理跳步、因果方向、还是结论外推？
4. 如果让我“强挑刺”，你允许我提出反例/构造极端情况/指出循环论证吗？哪些假设不可动？
5. 验收标准是什么：必须给出反例/必须形式化重写/必须输出决策（保留/改写/删除）？

## B_method — 方法正确性核查
1. 方法的输入-输出-假设分别是什么？请给最小形式化定义（变量/空间/约束）。
2. 这方法要解决的痛点是什么？相对 baseline 的关键差异点是什么（机制层面）？
3. 你担心的正确性点：收敛性/一致性/可辨识性/偏差来源/实现对齐/分布外？
4. 方法与证据的对齐：你现有实验/理论能覆盖哪些假设？哪些是假设未验证？
5. 你希望的产物：错误定位+修复方案，还是证明草图+边界条件，或二者都要？

## C_calculation — 计算正确性核查（算式/推导/数值）
1. 请标注你要核查的具体计算段（逐行编号/截图/LaTeX）。
2. 请说明符号约定与单位/量纲（如有），以及边界条件/初始条件。
3. 你希望核查粒度：代数变形、微积分步骤、期望/概率推导、还是数值实现一致性？
4. 是否需要我做“独立复算”（从上一行推到下一行），并指出最小错误点？
5. 如果发现错误，是否允许我给出替代推导 + 可复现检查清单（sanity checks）？

## E_innovation_correctness — 创新思路正确性审计（想法是否站得住）
1. 你的创新点用一句话表述是什么？它依赖哪些关键假设（列出）？
2. 你的创新试图打破的瓶颈是什么？你认为它为什么能打破（机制解释）？
3. 这条创新的“致命失败模式”是什么（反例/不可实现/违反约束/与已知定理冲突）？
4. 你更希望我采用：反驳式审计（强挑刺）还是建设式改造（保留核心、替换脆弱环节）？
5. 验收标准：你希望最后得到“可写进论文的创新表述+范围+局限”，还是“是否应放弃/改方向”的决策？

## D_paper_story — 论文整体思路核查（storyline & contribution map）
1. 你的贡献点清单（<=5条）是什么？每条贡献对应哪一节/哪一实验/哪一理论？
2. 读者最可能误解的点是什么？你希望如何防止误解（结构/措辞/图表）？
3. 你更在意：逻辑自洽、叙事张力、还是审稿人预期对齐？

## F_proof_idea — 证明思路核查（proof roadmap, gap finding）
1. 你现在的证明结构分哪几步？每一步用到哪些引理/假设？
2. 你最不确定的是哪一步？是技术引理、不等式、构造、还是边界条件？
3. 你希望输出：proof skeleton（可写进论文）还是 gap list + alternative route？

## H_experiment_completeness — 实验完整性检查（coverage, baselines, ablations, reporting）
1. 你的实验目标是什么：SOTA、消融解释、还是验证关键假设？
2. 你现在已有的实验有哪些？缺口是什么（baseline/ablation/metric/seed/reporting）？
3. 你希望我给出：2小时最小补全清单，还是投稿级完整 checklist？

## G_novelty_search — 创新点搜索/查新策略（可验证检索计划）
1. 你要查的新颖性对象是：问题设定/方法/理论/实验协议/系统工程？
2. 你允许我提出哪些检索关键词/同义词/子领域迁移关键词？（语言：中/英）
3. 查新产物要到什么程度：候选论文清单+对比表，还是仅检索策略？

## I_paper_interpretation — 论文解读（精读→claim map→风险点）
1. 你要解读的论文材料是什么（PDF/摘要/段落）？你希望我优先读哪部分？
2. 你更关注：核心机制、理论假设、实验可信度、还是与自己工作的关联？
3. 输出希望：面试式问答、复现式解释、还是可直接写 related work？

## J_sentence_rewrite_retrieval — 句子改写 + 风险审计（证据对齐）
1. 请给原句，并说明它的功能（claim/motivation/summary/limitation）。
2. 你允许的改写幅度：轻改措辞/重写结构/重排段落？语气偏保守还是偏强？
3. 你是否需要：替代表述 + 风险提示（夸大/不可证/不合规）？


## Fast path (focus one domain)
If the user wants to work on a single domain only, they may reply with:
- `FOCUS=<domain_key>` and optionally `intake_depth=tight`

Assistant behavior (pre-lock):
- Ask only the minimal questions for that domain.
- Generate Mode Lock for that scope.
- Wait for `CONFIRM` before doing any substantive work.
