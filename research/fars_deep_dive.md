# FARS Deep Dive (v1.5)

## Purpose
- FARS 目前按 `public-description source` 处理，不把媒体稿当论文替代。
- 本文档严格拆分为四层：`已公开事实`、`媒体转述`、`推断机制`、`未知项`。
- 任何进入 ZYR 协议层的结论，必须先落在“公开事实”或“明确标注为推断”的层级里。

## Source Ledger
| Date | Source | Type | URL | Status | Notes |
|---|---|---|---|---|---|
| 2026-02-13 | ThePaper: 复旦 MOSS 团队核心成员发布 FARS | public-description source | [ThePaper](https://www.thepaper.cn/newsDetail_forward_32600597) | read | 当前最完整的公开描述链路 |

## Public Facts
- 按 ThePaper 的报道，FARS（Fully Automated Research System）由上海日行迹于 `2026-02-12` 发布，报道发表于 `2026-02-13`。
- 公开描述把 FARS 定位为一个可自动完成“文献调研、假设生成、代码编写、实验执行、论文撰写”等科研全流程的多智能体系统。
- 报道明确给出 4 个模块：`Ideation`、`Planning`、`Experiment`、`Writing`。
- 报道明确给出一个共享文件系统，且说明它同时承担 `workspace` 与 `persistent memory` 的作用。
- 报道明确给出高算力执行底座：团队把一个 `160 卡 GPU 集群` 封装成训练与推理工具供智能体调用。
- 报道明确给出统一调用端口，可调用闭源与开源模型。
- 报道明确给出产物倾向：输出以“短论文”形式组织，每篇聚焦一个边界清晰的研究贡献。
- 报道明确给出失败结果策略：系统鼓励报告失败结果，而不是只保留正结果。
- 报道明确给出一个公开部署计划：预计直播运行一个月，目标生成 `100 篇` 学术论文。

## Media Transcriptions
- 媒体转述的核心叙事是：现有科研体系高门槛、高试错成本，而自动化研究系统能降低探索成本，并让失败结果也成为知识产物。
- 媒体把 FARS 的“第一性原理”表述为：每项研究成果都应具备清晰假设和可靠验证结果，正负结果都应被报告。
- 媒体把 FARS 的协作机制表述为：上游智能体连续提出并评估假设，通过后再交给下游模块依次处理，最终生成完整论文。
- 媒体把公开直播部署表述为一种反馈收集机制，目标读者包括研究者、审稿人和工程师。

## Inferred Mechanisms
- `推断 1：artifact-first handoff`。4 模块之间大概率不是口头消息传递，而是通过共享文件系统中的文件产物交接。这与“shared file system = workspace + persistent memory”的公开说法一致。
- `推断 2：hypothesis gate before expensive execution`。报道写到“假设被生成且通过自动化评估后交由后续智能体处理”，这意味着 FARS 在 Ideation 与 Planning/Experiment 之间存在一个自动 gate。
- `推断 3：high-throughput batch experimentation`。既然其公开强调 160 卡集群封装与持续批量运行，系统很可能偏向流水线吞吐而非单任务深度对话。
- `推断 4：failure result preservation as first-class artifact`。短论文且允许失败结果，说明其 artifact model 不是只产出“成功论文”，而是把 negative result 也固化为独立单元。
- `推断 5：shared FS replaces richer world model`。公开描述没有提知识图谱或对象级 world model；当前更像“共享文件系统驱动的 agent assembly line”，而不是 AI-Supervisor 那种显式 KG world model。

## Unknowns
- 没有公开论文、技术报告、系统卡或 benchmark 结果，因而以下均为 `UNKNOWN`：
  - 具体模型栈
  - 任务调度策略
  - 自动评估器的设计
  - 失败恢复策略
  - 安全与对齐机制
  - 论文质量评测标准
  - 100 篇直播部署的最终结果质量
- 公开描述没有给出 prompt / planner / memory schema，因此不能把它当作可直接复刻的 protocol。
- 公开描述没有解释人类在运行中的介入方式，因此“human override points”仍属 UNKNOWN。

## ZYR Alignment
### What to Adapt
- `shared workspace as memory`: 这是 FARS 最值得借鉴的部分，但对 ZYR 应保留为 `chat-first + artifact-first`，而不是改成全自动流水线。
- `small bounded artifacts`: “短论文 / 单贡献单元”这个思路适合转译为 ZYR 的 bounded deliverable 和 failure artifact，而不是无边界大任务。
- `negative-result preservation`: ZYR 可以把失败结果、未通过验证的假设、局部无效路径都记入 artifact ledger，而不是仅保留“成功答案”。

### What to Reject
- `unattended end-to-end full automation`: 这与 ZYR 的 lock-first、人类确认、completion-first 目标冲突。
- `default multi-agent decomposition`: ZYR 当前主要使用方式仍是把包交给 GPT/Codex 后在单会话中执行，不应默认把用户请求拆成无人监督的多代理流水线。
- `scope mutation by throughput pressure`: FARS 的吞吐导向适合批量探索，不适合 ZYR 当前强调的“完成单个合法请求”。

### Immediate Engineering Translation for ZYR
- 保留单会话主线，但强化 `workspace / artifact ledger / verification record`。
- 把“失败结果也应被显式记录”落到 `research/` 和 `artifacts/`，而不是让失败路径消失在对话里。
- 不把 FARS 当作协议模板；只把它当作 `artifact-first + durable workspace` 的工程启发。
