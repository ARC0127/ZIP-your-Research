# ARCHIVE (NON-NORMATIVE SNAPSHOT)

This file preserves an earlier playbook snapshot for reference. Canonical requirements live in `skills/reproducibility/S430_debug_vibe_core.md` (SSOT).

---

# DEBUG_VIBE_CORE Playbook (v1.0.1 addendum)

本单元把“vibe coding / LLM-assisted debugging”当成科研与工程的核心能力来设计：
- 目标不是“写得快”，而是 **闭环更快、回归更少、证据更强**。
- 任何结论必须可追溯到：代码差异 → 运行日志 → 产物 → 可重载验证。

---

## 0. 关联模块（不要重复发明轮子）
- **状态栏**：`boot/00_RESPONSE_STATUS_BANNER_v1.0.1.md`（永远显示 DEBUG_VIBE_CORE / VIBE / HCP）。
- **HCP 最短模板**：`boot/09_HCP_MINI_v1.0.1.md`。
- **核心技能**：`skills/reproducibility/S430_debug_vibe_core.md`（全流程模板）。
- **闭环验证**：`skills/reproducibility/S431_closed_loop_verification.md`（最小闭环 + 回归矩阵 + gate）。

---

## 1. 两种 VIBE 模式（默认 M3，但要让用户可选 M2）
### M2（受限增量模式：更稳、更可控）
- 适用：你需要“尽量不引入新结构/新脚本”，先把 pipeline 打通。
- 原则：**最小差异**（surgical patch），只改动必要文件。
- 新增文件上限：**由用户在对话中设定**（默认不假设）。
- 输出必须包含：回归矩阵 + 最小闭环命令 + 证据台账（见 S430）。

### M3（强力调试模式：更快闭环，但要“紧牵绳”）
- 适用：你允许为了彻底解决结构性 bug 进行模块封装/重排，但仍需可控。
- 原则：**先打通闭环，再做清理**：
  1) 先用最小改动让闭环 PASS（能 train → save → reload → val）。
  2) 再把临时补丁收敛成可维护结构（去冗余、统一入口、加测试）。
- 任何“新增脚本/新抽象”必须说明：它替代了哪个旧入口？能否删除旧的？

---

## 2. 闭环是第一性原理：定义、产物、证据
把任何复杂问题拆成三个判据：
1) **训练图是否包含目标模块**（结构证据，如 named_params / module repr）。
2) **checkpoint 是否持久化目标参数**（state_dict key/param cnt）。
3) **reload/val 是否可用**（不崩溃、输出一致、版本可复现）。

> 只要 (2) 或 (3) 失败，这次 run 就是 **无效对比**，不得用于结论。

---

## 3. 标准作业流（建议每轮 15~30 分钟闭环）
### Step A：锁定入口与不变量
- 入口：train/val/export/load 的真实调用链（不要靠猜）。
- 不变量：路径、seed、版本、设备、输出目录规则。
- 产物：run_dir 结构、best/last、metrics、plots。

### Step B：最小闭环（fast path）
- 数据子采样/epoch=1/fraction=0.05 等，只为验证“能跑通 + 能保存 + 能重载”。
- 成功后再扩展到多 seed、多 epoch。

### Step C：回归矩阵（至少 3×N）
- 基线（origin） + 主要变体 + 其它变体，全部至少跑 1 个短闭环。
- 任何改动都要保证“改了 A，不把 B 弄坏”。

### Step D：证据归档（可被第三方复现）
- 记录：git diff、命令行、stdout/stderr、关键日志片段、产物哈希。
- 输出：summary.json（pass/fail + 错误码 + 样例 keys）。

---

## 4. 反模式（最容易把项目拖死）
1) **脚本爆炸**：为每个小问题加一个脚本，入口越来越多，最后没人知道跑哪个。
2) **沉默失败**：异常吞掉但不打 gate；表面“跑完了”，实际对比无效。
3) **猴补 forward**：对实例方法做 monkey patch，导致 pickle/unpickle/reload 崩。
4) **只 patch model 不 patch EMA**：保存时用 EMA 权重，导致 best.pt 没有目标参数。
5) **只看 preflight 不看 checkpoint**：训练图里有模块，但权重没保存（或保存了别的对象）。

---

## 5. Codex/LLM 工具链绑定建议（不强依赖，但要“接口化”）
- 你可以把“生成代码”交给模型，但**验证闭环**必须由协议驱动。
- 最佳实践：把模型当成“代码合成器 + 诊断助手”，而不是“真相来源”。
- 约束方式：
  - 给它明确的回归矩阵与 gate；
  - 限制文件改动面；
  - 强制它在输出里列出“我实际检查了哪些文件”。

---

## 6. 可复制模板（建议直接 copy/paste 到每轮对话）
### 6.1 Patch Plan（最小差异）
- 目标：
  - 修复 X（给出报错/日志证据）
  - 保证三变体短闭环 PASS
- 修改面：
  - 文件列表（最多 K 个）
  - 预计新增文件数（与用户协商）
- Gate：
  - train_ok, artifacts_ok, keys_ok, reload_ok

### 6.2 Evidence Ledger（我实际检查了什么）
- 读取的文件：
- 运行的命令：
- 关键输出/哈希：
- UNKNOWN（未检项）：

### 6.3 Regression Matrix（最小必跑）
| variant | train(1ep) | save(best/last) | keys>0(if expected) | reload+val | pass |
|---|---|---|---|---|---|
| origin |  |  | n/a |  |  |
| variant_A |  |  |  |  |  |
| variant_B |  |  |  |  |  |

