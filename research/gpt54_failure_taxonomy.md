# GPT-5.4 Failure Taxonomy (v1.5)

## Purpose
- 记录当前升级要正面解决的 failure pattern。
- 这些 pattern 不是学术 benchmark 先提出的，而是来自用户对 GPT-5.4 实际使用体验的明确问题陈述，再结合外部 auto-research / verification 文献做协议翻译。

## Taxonomy
| Failure Pattern | Description | Typical Symptom | Contract Impact | Proposed Countermeasure |
|---|---|---|---|---|
| simplify_without_permission | 模型把合法但较大的请求缩成更小、更容易交付的版本 | 用户要求“全量修复”，模型只给最小示例或单点建议 | completion failure | `boot/11` + MODE_LOCK 默认 `deliver_full_requested_scope=true` |
| split_without_permission | 模型擅自把任务拆成多个子任务，并停在拆分或第一步 | 只返回 plan / subtasks / “先做 A” | execution drift | 禁止 silent decomposition；内部 staging 允许，但不得替代执行 |
| premature_stop | 模型在诊断、总结、计划后提前收尾 | “我已经分析完了，下一步你可以……” | partial completion disguised as completion | 引入 `FULLY_COMPLETED / PARTIALLY_COMPLETED / BLOCKED` 标签 |
| convert_execution_to_advice | 模型把“请做”改写成“你可以这样做” | 给建议、原则、注意事项，不真正动手 | execution reframing | coding/writing engines 明确禁止 advice-only downgrade |
| over_ask_when_discoverable | 模型重复向用户索取仓库里已存在的信息 | entrypoint、日志路径、配置位置都重新问一遍 | throughput collapse | `discover_before_asking=true` + minimal blocker questions |
| under_deliver_on_lawful_scope | 混合请求只完成最容易的那一项 | 只改摘要，不查文献；只给 patch，不给验证 | scope violation | new compliance corpus 强制检查 multi-component completion |
| mixed_request_easy_part_only | 混合任务中只做“最顺手”的一段 | 对“查文献+改写+风险审计”只做改写 | task-selection bias | `EXECUTE_ALL_COMPONENTS` cases in v1.5 corpus |
| large_scope_downgrade_to_mvp | 大任务被私自降成 MVP / sample / outline | 用户没要求最小版，但模型给了最小版 | implicit scope mutation | `NO_MVP_DOWNGRADE` cases + explicit permission requirement |
| plan_only_without_permission | 模型把执行请求先变成方案书 | “我先给你一个详细 plan” | user asked for execution, got planning | `NO_PLAN_ONLY` cases + boot/11 |
| partial_as_done | 模型把 patch 当作 fix，把验证计划当作验证完成 | 改了代码但没跑、没闭环却说“已修复” | false closure | `S431` 新增“不能把验证计划冒充验证完成” |
| blocker_question_overreach | 模型被一点点阻塞后，重新做整轮 intake | 让用户把整个需求再说一遍 | interaction bloat | `ASK_MINIMAL_IF_BLOCKED` policy |
| discoverable_local_context | 模型对本地 discoverable context 视而不见 | README、Makefile、日志都不看就发问 | execution laziness | tests + S430 “inspect repo/logs before asking” |

## Evidence Log
- `2026-03-30 user report`
  - 用户明确指出：GPT-5.4 升级后更容易不遵守 skill 运行，尤其容易 `拆分问题`、`简化问题`、`不完成合法要求`。
- `package baseline before v1.5`
  - 原协议更强调 lock 与 anti-drift，但没有把 `completion-first / anti-shortcut` 写成显式默认字段。
- `external alignment evidence`
  - Deep-research / auto-research 系统普遍在强化 `workspace / planning / multi-agent / verification`，但默认 autonomy 也更容易引入 silent decomposition 与 scope mutation。
- `v1.5 local response`
  - 新增 `boot/11_COMPLETION_FIRST_ANTI_SHORTCUT_v1.5.md`
  - 新增 `tests/compliance_v1_5/`
  - 更新 `S430/S431/S432` 与 coding/writing engine modules

## Regression Targets
| Corpus ID | Pattern | What It Prevents |
|---|---|---|
| `v1_5_c001` | simplify_without_permission | 防止把 repo-wide fix 悄悄缩成最小示例 |
| `v1_5_c002` | split_without_permission | 防止把多组件修复只做一段 |
| `v1_5_c003` | premature_stop | 防止写作任务做到一半提前收尾 |
| `v1_5_c004` | convert_execution_to_advice | 防止“直接改写”被改成“如何改写” |
| `v1_5_c005` | over_ask_when_discoverable | 防止仓库/日志可发现信息仍反复追问 |
| `v1_5_c006` | under_deliver_on_lawful_scope | 防止 mixed deliverable 只做一项 |
| `v1_5_c007` | mixed_request_easy_part_only | 防止“文献+改写+风险”只做摘要改写 |
| `v1_5_c008` | large_scope_downgrade_to_mvp | 防止 submission gate 被降成 sample output |
| `v1_5_c009` | plan_only_without_permission | 防止“直接修”被改成“先规划” |
| `v1_5_c010` | partial_as_done | 防止 patch without verification 被宣称完成 |
| `v1_5_c011` | blocker_question_overreach | 防止被小阻塞后重新做整轮 intake |
| `v1_5_c012` | discoverable_local_context | 防止本地 entrypoint 明明可找却不去找 |

## Current Implementation Status
- 规则层已落地：`boot/11`、`MODE_LOCK` execution posture、`router/intake_profile` defaults。
- skill 层已落地：`S430`、`S431`、`S432`、coding engine、writing engine。
- 测试层已落地：
  - `python tools/validate_completion_corpus_v1_5.py`
  - `python tools/simulate_completion_compliance_v1_5.py`
- 下一阶段需要做的不是再加更多 failure 名字，而是把这些 failure 绑定到更细粒度的 real-task eval。
