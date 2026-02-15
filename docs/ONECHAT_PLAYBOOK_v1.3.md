# ONECHAT Playbook (v1.3)

本手册用于 **仅用一个 ChatGPT 对话**，最大化发挥 GPT 的理解/推理/代码/上下文能力，同时保持可审计与不跑偏。

## 1) 你（用户）要做的最少动作
- 提供最小材料（文字/代码/日志/目标）
- 对 MODE_LOCK 回复 `CONFIRM`
- 每次变更目标时，用 `CHANGE_REQUEST:` 开头写清楚差异

## 2) 助手的强制动作（你可以用来验收）
每回合必须输出：
- 当前阶段（Ideation/Planning/Experiment/Writing/Review/Ops）
- 当前 focus（A/B/C/E/...）
- 本回合产物（新增/修改了哪些 artifact）
- 下一步最小命令/最小材料需求

## 3) 单对话“多智能体仿真”
- Ideation：用 S20x 形成问题与假设
- Planning：用 S30x 形成实验与消融计划
- Experiment：用 S430+S431 做闭环验证与最小 diff
- Writing：用 writing_engine 做保守改写
- Review：用 S432 做抗扰动 + 用 S424 做引用与归因审计
- Ops：用 S407/S428 做可复现打包

## 4) 最常见失败模式与修复
- 跑偏：触发 LOCKED_SCOPE_GUARD → 回到 MODE_LOCK
- 夸大：触发 claim language linter → 降格措辞
- 代码“堆功能”：触发 Patch Style → 删除/推迟非必要模块
