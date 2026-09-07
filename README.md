# ZIP-your-Research (ZYR) v1.7.0

<p align="center">
  <picture>
    <source media="(max-width: 600px)" srcset="docs/assets/zyr-cover-mobile-v1.7.0.svg">
    <img src="docs/assets/zyr-cover-v1.7.0.svg" width="100%" alt="ZIP your Research — Make every claim earn its place. A workflow connecting research questions, evidence, and the next check.">
  </picture>
</p>

<p align="center">
  <a href="#quick-start"><strong>Get started</strong></a> &nbsp;·&nbsp;
  <a href="docs/SHOWCASE.md"><strong>Explore verified cases</strong></a> &nbsp;·&nbsp;
  <a href="docs/SKILLS.md">Browse skills</a> &nbsp;·&nbsp;
  <a href="docs/QUICKSTART.md">Documentation</a>
</p>

<p align="center">
  <a href="docs/VERSION_IDENTITY_v1.7.0.md"><img src="https://img.shields.io/badge/suite-v1.7.0-23382e?style=flat-square&amp;labelColor=172228" alt="Suite v1.7.0"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-23382e?style=flat-square&amp;labelColor=172228" alt="MIT license"></a>
  <a href="docs/SHOWCASE.md"><img src="https://img.shields.io/badge/router-33%2F33%20passed-23382e?style=flat-square&amp;labelColor=172228" alt="33 of 33 public router cases passed in the 2026-09-04 local snapshot"></a>
</p>

**让每个科研主张都有对应的证据。** ZYR 是可阅读、可复制的科研技能库，包含
149 个活动清单条目，覆盖问题定义、文献、实验、证明、写作与绘图。
你提供任务和材料，助手按对应技能交付结果；检索、代码执行和文件生成能力由
所用平台提供。只使用文本提示词时，也可以完成材料分析和方案设计。

<!-- ZYR_LATEST_UPDATE_START -->
## 最新更新 · 2026-09-07

**v1.7.0 仓库精简** · 保留完整使用说明与全部活动技能

- 本轮文件数 **760 → 648**，减少 **112 个（14.7%）**；根目录文件 **14 → 11**。
- 移除 41 个内容完全相同的技能别名、23 个重复参考副本、15 个 Python 缓存，
  以及 33 个过时入口、版本副本和维护工具。旧内容可从 Git 或清理备份恢复。
- 保留 **149 个活动技能清单条目、153 个本地 ZYR 入口**和实际依赖的源协议；
  同步迁移引用、简化版本与兼容检查，不靠重复文件满足旧校验。
- 日常回复默认不输出状态横幅；当前启动、Mode Lock 和本地入口统一为 v1.7.0。
  普通任务按需读取一个主技能，模型和推理强度由用户决定。

[使用方法](#quick-start) · [升级与回滚](docs/RESOURCE_PROFILE_v1.md) ·
[发布检查](docs/RELEASE.md) ·
[GitHub CI](https://github.com/ARC0127/ZIP-your-Research/actions/workflows/ci.yml)
<!-- ZYR_LATEST_UPDATE_END -->

## Quick start

**第一次用，先选一个具体任务。** 例如核对论文主张、设计一个实验，或润色一段
摘要。无需先学习所有技能编号，也无需每次启动完整科研流程。

| 你现在的环境 | 用法 |
|---|---|
| 只有一个聊天窗口 | 复制单个技能正文，再贴任务材料，见方式一 |
| Codex 能读取本地文件，或已安装 ZYR | 打开仓库或调用已安装技能，见方式二 |
| 希望用 ZIP 建立完整、有范围锁定的研究对话 | 上传 ZIP 并完成启动确认，见方式三 |

### 方式一：复制一个技能，立即使用

1. 在下表选任务并打开技能文件。点击 GitHub 的 **Raw**，复制文件正文。
2. 把正文粘贴到聊天窗口，再补充目标、原始材料、限制和交付格式。
3. 发送后检查结果是否包含该技能的交付项；缺少的证据应明确标为 `UNKNOWN`。

以核对论文主张为例，复制 [S203](skills/research_core/S203_claim_evidence_matrix.md)
正文后，接着粘贴以下内容，并替换方括号中的材料：

```text
请按上面的 S203 技能检查论文主张与证据是否一致。
主张：[粘贴摘要或贡献列表中的具体主张]
现有证据：[粘贴对应实验表、图注、统计结果或可读取的文件]
范围：只核查这些主张；保持原始数值，不补造实验或引用。
交付：主张—证据—状态矩阵、证据缺口、建议修改的措辞、下一步验证。
```

预期得到可逐项核对的证据表和修改建议。只写“我们优于基线”却未提供结果表，
不能得到已验证的结论；助手应指出缺哪项证据。单个技能无需上传整个仓库，
涉及额外协议时再提供其明确需要的文件。

### 方式二：在 Codex 中使用

**尚未安装技能：直接把仓库作为项目使用。** 在 GitHub 点击
**Code → Download ZIP** 并解压，或运行：

```bash
git clone https://github.com/ARC0127/ZIP-your-Research.git
```

在 Codex 中打开包含 `AGENTS.md`、`skills_manifest.yaml`、`skills/` 的目录，
然后发送下面的任务。此方式让助手读取本地协议，不需要先运行安装脚本：

```text
使用这个仓库的 ZYR 技能完成任务。
先遵循 boot/14_RESOURCE_PROPORTIONAL_EXECUTION_v1.md，
在 skills_manifest.yaml 中定位 S603，只加载本次需要的协议。
请润色以下英文摘要，保留公式、数值、引用和技术主张，只输出修改后的正文：
[粘贴摘要]
```

**已经安装 ZYR：在技能列表选择 `zip-your-research`，或在输入中明确调用：**

```text
$zip-your-research
请用 S603 润色下面的英文摘要，保留公式、数值、引用和技术主张，
只输出修改后的正文：[粘贴摘要]
```

也可以直接选择具体技能，例如 `zyr-s603-bilingual-human-voice-delta-rewrite`。
不知道编号时说明任务即可，由总入口选择技能。材料可以直接粘贴，也可以给出
助手实际可读取的文件路径；仅写一个不可访问的文件名不能替代材料。

已有完整安装的用户按 [升级与回滚说明](docs/RESOURCE_PROFILE_v1.md) 使用 v2
更新器。**v2 目前只支持升级已有的完整 ZYR 安装，不是首次安装器**；克隆仓库
也不会自动注册全局技能。更新后重新加载 Codex 或新建任务以读取新入口。

### 方式三：上传 ZIP，启动完整研究对话

适用于能读取 ZIP 内文件的聊天环境。在 GitHub 点击 **Code → Download ZIP**，
将下载的文件上传到新对话，然后发送：

```text
请读取上传的 ZYR ZIP。先应用 boot/14_RESOURCE_PROPORTIONAL_EXECUTION_v1.md，
再按 boot/00_BOOTSTRAP_PROTOCOL_v1.7.0.md 启动严格 ZIP 工作流。
这是新项目，没有迁移提示词。
研究目标：[用一两句话说明问题]
已有材料：[说明已上传的论文、代码、数据或草稿]
本次交付：[例如一份带证据的研究缺口分析和可执行的实验计划]
允许联网检索；先完成 intake 并生成 Mode Lock，待我回复 CONFIRM 后执行。
```

助手会先询问影响范围的缺失信息，整理任务范围、材料、联网策略和交付物。
核对 Mode Lock 后回复 **`CONFIRM`**，再进入执行。后续在同一目标内补充材料、
纠正要求可直接继续。若平台不能读取 ZIP，解压后改用方式一。

### 选哪个技能、给什么材料

下列是日常任务入口。完整清单见 [INDEX.md](INDEX.md)。

| 你的任务 | 技能 | 提供的材料 | 主要交付 |
|---|---|---|---|
| 把模糊想法变成研究问题 | [S201](skills/research_core/S201_problem_framing.md) | 想法、领域、约束 | 问题定义、假设与成功标准 |
| 搜索并筛选文献 | [S204](skills/research_core/S204_literature_triage_pipe.md) | 主题、时间范围、纳入标准 | 检索与筛选结果、分类摘要和缺口 |
| 核对主张是否被证据支持 | [S203](skills/research_core/S203_claim_evidence_matrix.md) | 主张、实验表或其他证据 | 证据矩阵、缺口与措辞校准 |
| 设计能支持或否定假设的实验 | [S301](skills/exp/S301_min_decidable_experiment.md) | 假设、数据、算力与时间限制 | 实验步骤、验收标准、失败信号与日志要求 |
| 润色一段中文或英文 | [S603](skills/rwf_s340/S603_bilingual_human_voice_delta_rewrite.md) | 原文、用途、必须保留的内容 | 修订正文或逐句修改说明 |
| 查找数学证明中的缺口 | [S235](skills/research_core/S235_proof_gap_finder.md) | 定理、假设、完整推导 | 缺口、所需引理与修复路径 |
| 设计论文图 | [S621](skills/rwf_s340/S621_publication_fig_design_theory.md) | 要表达的结论、数据、版面要求 | 图型、信息编码与版式方案 |

例如设计实验可以这样提问：

```text
用 S301 设计一个检验“加入模块 A 能改善小样本泛化”的实验。
现有资源：[数据划分、基线代码、算力]。可用时间：[实际预算]。
请给出控制变量、对照组、指标与预先确定的判定标准，
说明什么结果会否定假设，以及必须保存哪些日志。本次交付实验方案。
```

要实际运行实验时，再给出代码与数据路径并明确执行要求；输出方案本身不代表
实验已运行。文献检索需要联网工具，图像与文件生成需要对应后端；缺少能力时
应明确说明可完成的部分及剩余项。

### 完整流程与默认行为

整篇论文写作选择 `writing_engine`；证明验证选择 `proof_engine`；实际制图与
研究代码分别选择 `figure_engine`、`coding_engine`。跨阶段任务可说明最终
交付物，让助手按需要衔接技能，示例见 [工作流组合](docs/WORKFLOWS.md)。

普通任务从当前 Agent 和一个主技能开始。明确要求多 Agent 研究或独立交叉审查
时才选择 S660；S661 用于生成式技能记忆，保留其同意、认证与评估要求。
严格 ZIP 启动需要 `CONFIRM`；单项技能调用沿用当前任务授权。模型与推理强度
由用户决定，ZYR 不自动修改这些设置。

日常回复不再重复 `ZIP_MODE / STAGE / MEMORY / WEB` 等状态横幅。需要排查执行
状态时可以明确询问或开启 `DEBUG_TRACE=ON`；这不会替代实际执行或必要确认。

## Documentation

| Need | Current guide |
|---|---|
| Choose a skill | [Skills guide](docs/SKILLS.md) and [generated index](INDEX.md) |
| Install or update Codex skills | [Resource profile and installer](docs/RESOURCE_PROFILE_v1.md) |
| Combine workflows | [Workflow recipes](docs/WORKFLOWS.md) |
| Understand proof, writing, figure, and code integrations | [Engine guides](docs/how_to_use/README.md) |
| Inspect reproducible examples | [Verified cases](docs/SHOWCASE.md) |
| Build and publish a release | [Release guide](docs/RELEASE.md) |
| Extend the library | [Contributing](CONTRIBUTING.md), [skill authoring](docs/SKILL_AUTHORING_GUIDE.md), [developer API](docs/DEVELOPER_API.md) |
| Understand memory boundaries | [Visible memory](docs/memory/VISIBLE_MEMORY_PROTOCOL_v1.md) and [procedural skills](docs/memory/DYNAMIC_SKILL_MEMORY_PROTOCOL_v1.md) |
| Check release identity or licensing | [Version identity](docs/VERSION_IDENTITY_v1.7.0.md), [LICENSE](LICENSE), [third-party attribution](docs/EXTERNAL_SKILL_ATTRIBUTION_v1.6.md) |

## Development

```bash
python -m pip install -r requirements.txt
python -B tools/zyr.py build --check
python -B tools/validate_v7_3.py
python -B tools/zyr.py check --ci
python -B tools/zyr.py route "search and triage recent papers" --json
```

Model tools and external backends come from the host. Missing sources and
unverified claims remain `UNKNOWN` or explicitly unavailable. Repository tests
establish implemented behavior and package integrity; they do not establish
scientific benefit or measured token savings. Current execution rules are in
[the resource profile](boot/14_RESOURCE_PROPORTIONAL_EXECUTION_v1.md).

## Acknowledgments and references

ZYR is open work. Its design was shaped by public research systems,
proof-verification papers, open learning materials, and open-source
writing/figure-making repositories. These works informed the system; they are
not claimed here as original ZYR inventions.

Architecture and control-plane references include [Google AI
co-scientist](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/),
[OpenAI deep
research](https://openai.com/index/introducing-deep-research/), [A Vision for
Auto Research with LLM Agents](https://arxiv.org/abs/2504.18765),
[PiFlow](https://arxiv.org/abs/2505.15047),
[AI-Researcher](https://arxiv.org/abs/2505.18705),
[ResearStudio](https://arxiv.org/abs/2510.12194),
[FS-Researcher](https://arxiv.org/abs/2602.01566),
[OR-Agent](https://arxiv.org/abs/2602.13769),
[EvoScientist](https://arxiv.org/abs/2603.08127),
[ResearchPilot](https://arxiv.org/abs/2603.14629),
[AI-Supervisor](https://arxiv.org/abs/2603.24402), and the public-description
source for [FARS](https://www.thepaper.cn/newsDetail_forward_32600597).

The S660 orchestration and evaluation boundary also draws on the following
primary or first-party sources:

- production and scientific-agent architectures: [Anthropic's multi-agent
  research system](https://www.anthropic.com/engineering/multi-agent-research-system),
  the peer-reviewed [Co-Scientist
  study](https://www.nature.com/articles/s41586-026-10644-y), and the [OpenAI
  deep research system
  card](https://openai.com/index/deep-research-system-card/);
- task-level feedback without an implied weight update:
  [Reflexion](https://proceedings.neurips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html)
  and
  [Self-Refine](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html);
- multi-agent reasoning and its unresolved independence/consensus limits:
  [Multiagent Debate](https://arxiv.org/abs/2305.14325) and the controlled
  study [Can LLM Agents Really
  Debate?](https://arxiv.org/abs/2511.07784);
- research and citation evaluation:
  [BLADE](https://aclanthology.org/2024.findings-emnlp.815/),
  [ResearchArena](https://aclanthology.org/2025.findings-emnlp.303/),
  [ALCE](https://aclanthology.org/2023.emnlp-main.398/), and
  [CheckList](https://aclanthology.org/2020.acl-main.442/);
- governance, untrusted-content, and memory boundaries: [NIST AI
  600-1](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence),
  [OWASP AI Agent Security](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html),
  [MemBench](https://aclanthology.org/2025.findings-acl.989/), and the
  preprint [From Untrusted Input to Trusted
  Memory](https://arxiv.org/abs/2606.04329).

These sources motivate design and evaluation questions. Their results do not
establish that S660 improves a scientific outcome; that remains
`UNKNOWN_PENDING_BEHAVIORAL_EVAL` until a controlled evaluation is run.

The visible-memory retrieval design also considered
[Transformer-XL](https://arxiv.org/abs/1901.02860),
[RETRO](https://arxiv.org/abs/2112.04426),
[Memorizing Transformers](https://arxiv.org/abs/2203.08913), and
[HippoRAG](https://arxiv.org/abs/2405.14831). P0 deliberately does not train or
embed a new memory model. Canonical memory remains inspectable Markdown; a
Transformer embedding retriever, approximate-nearest-neighbor index,
cross-encoder reranker, or graph retriever is an optional, versioned,
rebuildable cache whose similarity score cannot change consent or epistemic
status.

The dynamic Skill-memory design additionally inspected
[DojoAgents](https://pypi.org/project/dojoagents/),
[MemSkill](https://arxiv.org/abs/2602.02474),
[Memento-Skills](https://github.com/Memento-Teams/Memento-Skills),
[Acontext](https://github.com/memodb-io/Acontext), the
[Agent Skills specification](https://agentskills.io/specification), and the
[OpenAI Agents SDK memory
guide](https://openai.github.io/openai-agents-js/guides/sandbox-agents/memory/).
These sources motivate Skill-as-memory, hard-case evolution, progressive
disclosure, and extraction/consolidation separation. They do not establish
that an automatically generated ZYR Skill improves research quality.

Comparative open-source systems inspected during the design include
[PaperQA2](https://github.com/Future-House/paper-qa) for scientific-document
retrieval with citations, [STORM/Co-STORM](https://github.com/stanford-oval/storm)
for multi-perspective knowledge curation, and
[The AI Scientist](https://github.com/SakanaAI/AI-Scientist) for an
experiment-to-paper workflow and its explicit arbitrary-code execution risk.
They are references, not bundled dependencies, and their reported results do
not transfer to ZYR.

For figure and diagram work, the comparison set includes the official
[draw.io](https://github.com/jgraph/drawio) editor and
[SciencePlots](https://github.com/garrettj403/SciencePlots), in addition to the
locally preserved figures4papers source. P0 adopts their source-editable and
publication-style lessons while keeping the SDR, data lineage, uncertainty,
and visual-claim audit authoritative; visual polish is not scientific
verification.

Proof and theory references include [Pessimistic Verification for Open-Ended
Math Questions](https://arxiv.org/abs/2511.21522),
[Hard2Verify](https://arxiv.org/abs/2510.13744), [Scaling Flaws of
Verifier-Guided Search in Mathematical
Reasoning](https://arxiv.org/abs/2502.00271), [Improving Value-based Process
Verifier via Low-Cost Variance
Reduction](https://arxiv.org/abs/2508.10539), [Asking LLMs to Verify First is
Almost Free Lunch](https://arxiv.org/abs/2511.21734), [AI
Mathematician](https://arxiv.org/abs/2505.22451),
[StepProof](https://arxiv.org/abs/2506.10558),
[Goedel-Prover](https://arxiv.org/abs/2502.07640),
[Goedel-Prover-V2](https://arxiv.org/abs/2508.03613),
[Leanabell-Prover-V2](https://arxiv.org/abs/2507.08649), and
[APOLLO](https://arxiv.org/abs/2505.05758).

Open learning and community references include [Hello-Agents
(Datawhale)](https://github.com/datawhalechina/hello-agent).

The full local working tree contains the following external sources for
attributed workflow use. Local presence and attribution do not by themselves
grant redistribution rights. The v1.7 fail-closed safety release includes only
assets that pass `manifests/THIRD_PARTY_ASSETS.yaml` and
`manifests/release_policy.yaml`.

- [Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills),
  present under `ext/src/rpws/`, for paper structure, section guides, and
  claim-evidence writing discipline. Its local MIT license is verified, so it
  is admitted by the current safety release policy.
- [Prof. Peng Sida's open research
  notes](https://github.com/pengsida/learning_research), acknowledged through
  the upstream attribution of Research-Paper-Writing-Skills.
- [awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing),
  present under `ext/src/awesome/`, for academic-writing prompts, bilingual
  rewriting patterns, and logic-checking examples. Its checked-in license
  evidence is currently `UNKNOWN`, so the safety release excludes it.
- [figures4papers](https://github.com/ChenLiu-1996/figures4papers), present
  under `ext/src/figures/`, for scientific figure-design principles, plotting
  scripts, demonstrations, and reusable figure-generation patterns. Its
  checked-in license evidence is currently `UNKNOWN`, so the safety release
  excludes it.

For detailed attribution and integration boundaries, see:

- `docs/ATTRIBUTION.md`
- `docs/EXTERNAL_SKILL_ATTRIBUTION_v1.6.md`
- `docs/integrated_external_skills/README_integrated_stack_v1.0.md`
- `research/auto_research_inventory.md`
- `research/engineering_alignment_matrix.md`
- `research/fars_deep_dive.md`
- `research/pessimistic_verification_lineage.md`
