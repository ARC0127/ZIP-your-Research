# Agentic Architecture (v1.3)

## Why agentic inside one chat?
你规划的 2.0 会走“API + 多 agent 协作”。但在 1.3 阶段，我们用 **严格协议 + 工件契约**，在单对话中模拟 agentic pipeline。

## Reference (FARS / 日行迹)
FARS（Fully Automated Research System）在公开报道中被描述为由 Ideation、Planning、Experiment、Writing 四个智能体模块构成，并在共享文件系统中协作，文件系统同时承担工作空间与持久记忆。  
本项目 1.3 的 ONECHAT_LOOP 以此为灵感：在单对话中用“阶段门控 + artifacts”去模拟“共享文件系统的持久记忆”。  
(外部引用见本仓库 `docs/ATTRIBUTION_v1.3.md`)

## Layers
- Control Plane: boot/ + router/（锁、范围、路由、验收）
- Skill Plane: skills/（最小可组合单元）
- Artifact Plane: templates/ + docs/workflows/（可审计工件）

## Design rules (minimalism)
- 先闭环再扩展：任何功能必须先可运行、可验证。
- 最小 diff：优先修改已有文件，不新增“未来可能用到”的脚手架。
- UNKNOWN > 猜测：对事实/引用不确定就标注 UNKNOWN。
