# Engineering Alignment Matrix (v1.5)

## Purpose
- 把外部 auto-research / deep-research 架构转译成 ZYR 可执行的工程选择。
- 不是问“先进不先进”，而是问“会不会帮助 chat-first、lock-first、completion-first 的 ZYR”。

## Translation Rules
- `Adopt`: 直接对 ZYR 的 chat-first 执行质量有增益，且不会鼓励 silent decomposition / silent simplification。
- `Adapt`: 值得借鉴，但只能受控引入，不能默认打开。
- `Reject`: 会提高 scope drift、自动拆题、自动改任务、或无人值守倾向。

## Matrix
| Mechanism | Seen In | Why It Helps / Hurts | Adopt / Adapt / Reject | ZYR Translation |
|---|---|---|---|---|
| Persistent workspace / note substrate | FS-Researcher, ResearchPilot, FARS, AI-Supervisor | 解决长上下文衰减，让代理有 durable state；但若无控制平面也会把错误持久化 | `Adopt` | 保持 `research/`、`artifacts/`、evidence ledger、verification record 为 first-class artifact，而不是只靠对话历史 |
| Artifact-first handoff | Google AI co-scientist, FARS, ResearchPilot | 把协作落到可审计对象，而不是模糊自然语言记忆 | `Adopt` | 强化 `MODE_LOCK`、verification report、research notes、compliance report 等中间产物 |
| Explicit supervisor / control plane | Google AI co-scientist, AI-Supervisor, ResearStudio | 能防止自由漂移，但如果 supervisor 目标错了会系统性偏航 | `Adopt` | 继续把 `boot/` + `router/` + `MODE_LOCK` 作为 control plane；v1.5 已补 `completion-first` 与 anti-shortcut 规则 |
| Human-intervenable live plan | ResearStudio | 显著降低 fire-and-forget 风险；把人重新放回 loop | `Adopt` | 当前不做复杂 UI，但保留 `CONFIRM` / `CONFIRM CHANGE` / explicit diff / partial completion label 这一套交互契约 |
| Verification before synthesis | PiFlow, OpenAI deep research, AI Mathematician, Pessimistic Verification line | 直接抑制“先编一个再说”；但 verifier 质量差时会误伤 | `Adopt` | 把 falsify-before-finalize 写入 `S430/S431` 和 `boot/11`; 让验证先于“宣布完成” |
| First-error-wins proof gate | Pessimistic Verification, Hard2Verify | 单个 fatal flaw 比多数“看起来对”更重要；特别适合 theorem/proof audit | `Adopt` | 在 `proof_engine`、`S240`、`S241`、`tests/proof_verification_v1_5/` 中把 fatal flaw 设为主 verdict 控制器 |
| Progressive multiscale proof verification | Pessimistic Verification, StepProof | 长证明不能只看整体，也不能只看局部；需要 whole-proof 与 chunk-level 结合 | `Adopt` | `proof_engine` 先整体审，再逐层 chunk drill-down，并输出 `chunk_verdict_matrix` |
| Formal adapter as optional evidence channel | StepProof, Goedel-Prover, Leanabell-Prover-V2, APOLLO | formal verifier 很强，但 formalization 不完整时不能卡死主流程 | `Adapt` | 通过 `S433` 提供 `autoformalization_candidates` / `Lean sketch` / `formal_gap_record`，默认 non-blocking |
| Reviewer-feedback repair loop | Pessimistic Verification repo, APOLLO | proof 修订有价值，但修订文本本身不等于已验证通过 | `Adopt` | `proof_engine` 允许 refine，但必须 re-verify 通过后才能标记 `verified_true` |
| Local-first transparent stack | ResearchPilot | 对可审计性和可复制性很好；对 ZYR 这种 ZIP 分发方式尤其友好 | `Adopt` | 研究与测试产物优先本地化、文件化、自校验 |
| Structured reflection + memory compression | OR-Agent, EvoScientist | 能提升长程搜索效率；但也会激励默认多阶段拆题 | `Adapt` | 只借鉴 retrospection / memory summary，不默认引入 autonomous branching search |
| Principle-aware / world-model guidance | PiFlow, AI-Supervisor | 有助于减少无目的搜索；但建模成本高、错误也更“结构化” | `Adapt` | 未来可考虑 lightweight problem-state schema；当前先不做 KG / formal world model |
| Benchmark-first self-evaluation | AI-Researcher, Hard2Verify, Google AI co-scientist | 有利于防自嗨；但 benchmark 本身会诱导“为了过基准而不是为了完成用户任务” | `Adapt` | 保留 prompt regression 与 compliance regression，但以 lawful task completion 为主目标，不为 benchmark 优化而改用户体验 |
| End-to-end unattended research factory | AI-Researcher, FARS, EvoScientist | 与 ZYR 当前“用户把包发给 GPT/Codex，在单会话里完成明确请求”的现实完全不匹配 | `Reject` | 不做 full auto-research，不默认自主生成新目标、新分支、新项目 |
| Default multi-agent decomposition | OR-Agent, broad auto-research visions | 容易把一个清晰请求拆成多个内部子问题后只完成最轻的一部分 | `Reject` | v1.5 明确禁止 silent decomposition；内部 staging 允许，但不允许 user-visible 缩 scope |
| Scope mutation without explicit confirmation | many autonomous systems by design | 对开放探索有利，但会直接冲掉 MODE_LOCK | `Reject` | 任何 scope mutation 必须显式走 `CONFIRM CHANGE` |
| Lean-first or formal-first default routing | formal theorem proving systems | formal pipeline 很容易把自然语言 proof audit 变成工具驱动任务，压垮 chat-first 体验 | `Reject` | 1.5 坚持 `natural-language verification first`，formal adapter 只作可选增强层 |
| Pre-lock browsing / free exploration | deep-research products by default | 对效率有帮助，但会让 ZYR 在锁定前更容易漂移和幻觉 | `Reject` | 保持 pre-lock browsing OFF；仅在 lock 后允许浏览 |

## Immediate Translation into This Workspace
- `boot/11_COMPLETION_FIRST_ANTI_SHORTCUT_v1.5.md`
  - 对齐的是 `supervisor/control plane + anti-shortcut`
- `router/intake_profile_v1.3.2.yaml`
  - 增加 `deliver_full_requested_scope=true`、`silent_simplification=forbid`、`silent_decomposition=forbid`
- `S430` / `S431` / `S432`
  - 对齐的是 `verification-before-synthesis`、`partial completion labeling`、`scope firewall`
- `tests/compliance_v1_5/`
  - 对齐的是 `benchmark-first`, 但 benchmark 的目标改成“合法请求完成性”而不是“自主科研得分”
- `skills/proof_engine/` + `tests/proof_verification_v1_5/`
  - 对齐的是 `first-error-wins`、`progressive proof verification`、`repair then re-verify`、`optional formal adapter`

## Bottom Line
- ZYR v1.5 应该成为 `chat-first controlled research execution system`，不是 `full auto-research factory`。
- 真正需要对齐的是：`durable workspace`、`artifact-first execution`、`verification before finalization`、`human-governed scope control`。
- 明确不要对齐的是：默认多 agent 拆题、自动 scope mutation、以及把 autonomy 当成功能本身。
