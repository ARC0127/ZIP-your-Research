# Attribution & References

## Scope

ZYR is an open research workflow pack. Its protocol, routing, artifact, and verification design draws methodological inspiration from public papers, product writeups, public project descriptions, and open learning materials.

This file exists for two reasons:

- 明确说明哪些外部工作影响了 ZYR 的工程方向。
- 清楚区分 `方法学借鉴`、`公开描述来源`、`本地开发时核对过的主材料` 与 `ZYR 自己的转译实现`。

ZYR 不把这些外部工作的核心想法据为己有，也不把第三方运行时实现直接当作 ZYR 核心功能 vendoring 进来。对外部工作的使用方式，是 `阅读 -> 抽象机制 -> 受控转译 -> 在本仓库内重新实现为协议、技能、artifact 与 regression`。

## How to read this file

- `Primary source` 优先于二级报道。
- `FARS` 当前在 ZYR 中仍按 `public-description source` 处理，不把媒体表述当成正式论文结论。
- `Pessimistic Verification` 这条线，除了外部论文链接，开发时还核对过本地 PDF 与本地源码压缩包；这些本地材料不作为仓库公开依赖 vendoring。
- 更细的转译结论见：
  - `research/auto_research_inventory.md`
  - `research/engineering_alignment_matrix.md`
  - `research/fars_deep_dive.md`
  - `research/pessimistic_verification_lineage.md`

## Agentic / Deep-Research Architecture References

| Reference | Primary source | What ZYR learned |
|---|---|---|
| Google AI co-scientist | [Google Research blog](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/), [arXiv:2502.18864](https://arxiv.org/abs/2502.18864) | 借鉴 `explicit supervisor/control plane`、`artifact-first scientific handoff`、`verification before finalization`。 |
| OpenAI deep research | [OpenAI product note](https://openai.com/index/introducing-deep-research/) | 借鉴 `long-horizon research execution` 与 `source-bearing report` 的产品形态，但不照搬其默认浏览姿态。 |
| A Vision for Auto Research with LLM Agents | [arXiv:2504.18765](https://arxiv.org/abs/2504.18765) | 作为 auto-research 生命周期全景参考；ZYR 主要把它当作对照项，而不是目标架构。 |
| PiFlow | [arXiv:2505.15047](https://arxiv.org/abs/2505.15047) | 借鉴 `principle-aware reasoning` 与 `verification-before-synthesis`。 |
| AI-Researcher | [arXiv:2505.18705](https://arxiv.org/abs/2505.18705) | 作为 benchmark-oriented autonomous science 参考；ZYR 明确拒绝其 `unattended factory` 姿态。 |
| ResearStudio | [arXiv:2510.12194](https://arxiv.org/abs/2510.12194) | 借鉴 `human-intervenable plan`、`planner-executor separation`、`controllability by design`。 |
| FS-Researcher | [arXiv:2602.01566](https://arxiv.org/abs/2602.01566) | 借鉴 `durable workspace`、`source archive`、`hierarchical knowledge base`。 |
| OR-Agent | [arXiv:2602.13769](https://arxiv.org/abs/2602.13769) | 借鉴 `structured reflection` 与 `memory compression`，但不默认引入自动多分支搜索。 |
| EvoScientist | [arXiv:2603.08127](https://arxiv.org/abs/2603.08127) | 借鉴 `persistent ideation / experiment memory` 与失败路径保留。 |
| ResearchPilot | [arXiv:2603.14629](https://arxiv.org/abs/2603.14629) | 借鉴 `local-first transparent stack`、`typed artifact flow`、`citation-aware synthesis`。 |
| AI-Supervisor | [arXiv:2603.24402](https://arxiv.org/abs/2603.24402) | 借鉴 `world-model flavored supervision` 与 `self-correcting loops` 的控制思想。 |
| FARS | [ThePaper public-description source](https://www.thepaper.cn/newsDetail_forward_32600597) | 借鉴 `Ideation -> Planning -> Experiment -> Writing` 的模块分层与 `shared filesystem as workspace` 的公开描述；当前仍按公开报道而非正式论文处理。 |

## Proof / Theory / Verification References

| Reference | Primary source | What ZYR learned |
|---|---|---|
| Pessimistic Verification for Open-Ended Math Questions | [arXiv:2511.21522](https://arxiv.org/abs/2511.21522) | 是 `proof_engine` 的锚点来源，直接引入 `first-error-wins`、`parallel pessimistic review`、`progressive multiscale verification`、`repair then re-verify`。 |
| Hard2Verify | [arXiv:2510.13744](https://arxiv.org/abs/2510.13744) | 借鉴 `step-level first-error localization`，用于 proof regression 与 derivation ledger 设计。 |
| Scaling Flaws of Verifier-Guided Search in Mathematical Reasoning | [arXiv:2502.00271](https://arxiv.org/abs/2502.00271) | 提醒 verifier 不是万能 oracle，避免把 proof verifier 升级成自动搜索主控。 |
| Improving Value-based Process Verifier via Low-Cost Variance Reduction | [arXiv:2508.10539](https://arxiv.org/abs/2508.10539) | 借鉴 `verifier uncertainty should be recorded, not hidden` 的意识。 |
| Asking LLMs to Verify First is Almost Free Lunch | [arXiv:2511.21734](https://arxiv.org/abs/2511.21734) | 借鉴 `verify-first ordering`，但 ZYR 把它落成 artifact-level contract，而不只停留在 prompt trick。 |
| AI Mathematician | [arXiv:2505.22451](https://arxiv.org/abs/2505.22451) | 作为研究级数学系统背景参考，说明 pessimistic verification 可以是大系统中的可靠性 gate。 |
| StepProof | [arXiv:2506.10558](https://arxiv.org/abs/2506.10558) | 借鉴 `step-by-step verification` 与 `subproof decomposition`，用于 theorem normalization 与 step verdict 设计。 |
| Goedel-Prover | [arXiv:2502.07640](https://arxiv.org/abs/2502.07640) | 借鉴 `formal theorem/proof structuring`，但 ZYR 不把 formal proof generation 设为默认主线。 |
| Goedel-Prover-V2 | [arXiv:2508.03613](https://arxiv.org/abs/2508.03613) | 借鉴 `self-correction with formal feedback` 作为 optional adapter 启发。 |
| Leanabell-Prover-V2 | [arXiv:2507.08649](https://arxiv.org/abs/2507.08649) | 借鉴 `verifier-integrated reasoning`，影响了 ZYR 的 `formal adapter is auxiliary` 设计。 |
| APOLLO | [arXiv:2505.05758](https://arxiv.org/abs/2505.05758) | 借鉴 `repair then re-verify` 以及 formal feedback 作为辅助证据的接口思路。 |

## Open Learning / Community References

| Reference | Primary source | What ZYR learned |
|---|---|---|
| Hello-Agents (Datawhale) | [GitHub](https://github.com/datawhalechina/hello-agent) | 借鉴 `从原理到范式到实践` 的教学组织方式，用于早期 onboarding、技能目录与单对话 agentic 教学路线。 |

## Internal Translation Targets

这些外部参考不是停留在“灵感清单”，而是被转译进了 ZYR 的具体实现：

- `boot/`:
  - `completion-first`
  - `scientific-discipline-first`
  - `loss-minimizing migration`
  - `proof verification profile`
- `skills/`:
  - `writing_engine`
  - `coding_engine`
  - `proof_engine`
  - `S430` / `S431` / `S432`
  - `S237` / `S240` / `S241` / `S433`
- `artifacts/`:
  - `evidence_ledger.csv`
  - `source_archive_manifest.yaml`
  - `proof_casebook.md`
  - `negative_result_ledger.md`
  - `run_state.json`
- `tests/`:
  - `completion_compliance`
  - `scientific_discipline`
  - `proof_verification`

## Bottom line

ZYR 的目标不是把所有外部系统揉成一个新的“自动科研大一统平台”。相反，这些参考主要帮助 ZYR 明确三件事：

- 什么机制值得 `Adopt`
- 什么机制只能 `Adapt`
- 什么姿态必须 `Reject`

对 ZYR 最重要的外部影响不是“自治程度更高”，而是：

- 更强的控制平面
- 更耐久的 artifact substrate
- 更严格的 proof / derivation verification
- 更诚实的研究执行边界
