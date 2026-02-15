# DEBUG_VIBE_CORE（导航页）

> **非规范文件（Non-normative）。** 唯一权威规范（SSOT）是：`skills/reproducibility/S430_debug_vibe_core.md`。
> 
> 本页只负责“怎么用/去哪看”，不再重复 MUST/SHALL 级规则，避免多处定义导致漂移。

---

## 1) 权威来源与配套模块

- **S430（唯一权威规范）**：`skills/reproducibility/S430_debug_vibe_core.md`
- **S431（闭环验证模板）**：`skills/reproducibility/S431_closed_loop_verification.md`
- **状态栏展示**：`boot/00_RESPONSE_STATUS_BANNER_v1.3.2.md`
- **HCP 最短展示模板**（语义仍以 S430 为准）：`boot/09_HCP_MINI_v1.3.2.md`

---

## 2) 使用方式（最短闭环）

当你提出任何“涉及代码/实验/结果”的请求时，按顺序做：
1) **先 HCP**：列出你/模型实际检查了哪些文件、运行了哪些命令；未检项标 UNKNOWN。
2) **先闭环再扩展**：用最小 epoch/fraction 验证 “入口→执行→产物→持久化→重载/验证”。
3) **最小回归矩阵**：baseline + 主变体 + 第二变体（至少 3 个）。

---

## 3) 术语与模式（只做指针，不复述定义）

- DEBUG_VIBE_CORE / VIBE(M2/M3) / HCP / Evidence Ledger / Closed-loop / Regression Matrix：
  - 统一看 **S430**。

---
