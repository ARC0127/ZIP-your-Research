# 2026-09-07 ZYR 执行效率修改与验证

已实施用户审阅后的第 1—6 项：渐进加载、按交付物选择技能、收窄默认
多 Agent 路由、限定 ZIP intake 适用范围、识别同一目标内的补充指导、
区分维护验证与科研能力评测。已更新源码和本机 153 个 ZYR 安装入口。

## 已验证结果

| 项目 | 修改前 | 修改后 |
|---|---:|---:|
| 153 个 ZYR `SKILL.md` 的字节总量 | 756,090 | 165,819 |
| 写作引擎 `SKILL.md` 字节数 | 202,247 | 1,359 |
| 普通权威检索的主要路由 | S660 | S204，单 Agent |
| 局部摘要润色 | writing_engine | S603 |
| 明确要求多 Agent | S660 | S660，保留完整能力门禁 |
| 全文统稿 | writing_engine + S640 | 保留 |

入口体积减少 **78.07%**。这是按需加载入口的字节指标，不是整轮上下文、
模型推理 token、API 费用或科学能力的改善比例。实际端到端 token 和时间
收益尚未进行等设置、等质量门槛的配对测量。

完整协议仍保存在 `references/source.md`；150 份映射源协议与当前仓库
逐字节一致。基线 1,229 个安装文件均保留，授权改动之外无哈希漂移。
`config.toml` 和 `claim/SKILL.md` 哈希未变，模型仍为 GPT-6 Astra / xhigh。

验证通过：构建一致性、v7_2、check --ci、33 个历史路由案例、15 个新增
路由与安装回滚测试，以及相关既有测试。既有测试与 check --ci 有重叠，
不能相加作为独立样本。安装计划核对 479 个目标，漂移为零。
332 个真实改动路径的首轮两阶段回滚已在隔离副本中重放，通过基线哈希检查。

机器可读证据：[verification.json](verification.json)。
执行规则：[resource profile v1](../../../boot/14_RESOURCE_PROPORTIONAL_EXECUTION_v1.md)。
维护说明：[RESOURCE_PROFILE_v1.md](../../RESOURCE_PROFILE_v1.md)。

## 备份与回滚

基线目录：`D:/codex/home/skill-backups/zyr-efficiency-20260907T105507/`。
其中 `repository-baseline.zip` 保存修改前受 Git 跟踪的源文件，
`installed-baseline.zip` 保存修改前的完整 ZYR 安装，`baseline.json` 保存哈希。

发布前复核补充了明确点名技能、独立审查、拒绝多 Agent 后仍继续普通检索的回归。
最终 21 项 profile 测试和完整 CI Python 测试集 74 项通过（1 项平台相关跳过）。
最终三阶段安装回滚也已在隔离副本验证。

安装回滚必须按最后修改优先的顺序执行：

```powershell
py -3 -B tools/install_codex_profile_v1.py --skills-root D:/codex/home/skills --restore D:/codex/home/skill-backups/zyr-efficiency-20260907T105507/git-preflight/receipt.json
py -3 -B tools/install_codex_profile_v1.py --skills-root D:/codex/home/skills --restore D:/codex/home/skill-backups/zyr-efficiency-20260907T105507/refinement/receipt.json
py -3 -B tools/install_codex_profile_v1.py --skills-root D:/codex/home/skills --restore D:/codex/home/skill-backups/zyr-efficiency-20260907T105507/applied/receipt.json
```

回滚工具拒绝覆盖后续用户修改。隔离验证没有回滚正在使用的安装。
首轮交付时未提交 Git；后续发布已获得用户授权，以 Git 提交记录为准。
既有 `.codex/` 内容未改动。
建议重启 Codex 后使用新任务，让技能发现和加载使用更新后的入口。
