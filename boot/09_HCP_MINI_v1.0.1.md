# 09 HCP MINI（永远显示、保持短）

> **模板（Non-normative）**：HCP 的规范含义以 `skills/reproducibility/S430_debug_vibe_core.md` 为准。

## HCP-MINI（输出时必须出现；建议 6~10 行）
1) **证据台账**：我实际读取/运行/对比了哪些文件与日志？否则写 **UNKNOWN**，并给出可执行验证命令。
2) **改动面**：本次改动触达哪些入口（train/val/export/load/ckpt/metrics）？
3) **最小闭环**：是否具备“入口→执行→产物→持久化→重载/验证”的最小闭环测试？没有就先补。
4) **回归矩阵**：至少跑 baseline + 主变体 + 第二变体；确保改 A 不坏 B。
5) **可复现钉死**：版本、seed、命令、路径是否完整？是否会被默认行为改变输出目录/保存对象？
6) **安全加载**：`torch.load`/checkpoint 视为不可信输入；优先只取 `state_dict`（或使用 `weights_only=True`）并在隔离环境验证。
