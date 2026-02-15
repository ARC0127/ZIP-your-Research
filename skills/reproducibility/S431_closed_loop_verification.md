---
id: S431
name: closed_loop_verification
category: reproducibility
status: stable
triggers:
- closed loop
- 闭环
- verification
- 回归矩阵
- regression matrix
- sanity check
inputs_required:
- entrypoint_commands
- artifact_paths
- pass_criteria
outputs_required:
- closed_loop_plan
- verification_commands
- regression_matrix
quality_gates:
- no_fabrication
- mark_UNKNOWN
- copy_paste_ready
---

> **Non-negotiable global invariant:** Truthfulness • Trustworthiness • Deep logical reasoning.  
> **Authority note:** S430 defines the normative meaning of “closed-loop” and PASS criteria. This skill is a **template** for applying S430 with minimal friction.

# S431 CLOSED_LOOP_VERIFICATION（模板：把 S430 落到可执行命令）

## 0) 你给我什么（最小输入）
请用最少信息回答三件事（未知就写 UNKNOWN）：
1) **Entrypoints**：你实际用来跑的命令（train/val/infer/export）
2) **Artifacts**：产物路径（ckpt/log/metrics），以及保存/重载路径
3) **PASS**：什么算“修复/完成”（可观察、可断言）

---

## 1) 我会输出什么（固定格式）
### A) Closed-loop plan（分段定位断点）
- Entry → Build graph → Run → Save → Reload → Eval
- 我会标注每一段的“证据锚点”（日志/文件/指标/校验）

### B) Verification commands（可复制）
- 最短复现命令（MR）
- 最小闭环命令（CL）
- 重载验证命令（RL）
- 失败时的断点采样命令（BP）

### C) Regression matrix（至少 3 跑）
- baseline（原始）
- main variant（你的改动）
- second variant（对照改动/回滚/另一路线）

---

## 2) 输出模板（我将严格按此给出）
#### Closed-loop plan
- [Entry] ...
- [Run] ...
- [Save] ...
- [Reload] ...
- [Eval] ...

#### Verification commands
```bash
# MR (minimal repro)
...

# CL (closed-loop)
...

# RL (reload validation)
...
```

#### Regression matrix
| variant | command | expected artifact | PASS criteria |
|---|---|---|---|
| baseline | ... | ... | ... |
| main | ... | ... | ... |
| second | ... | ... | ... |

---

## 3) 失败时的约束（防幻觉）
- 如果我没看到你的入口命令/目录结构/保存逻辑，我会把对应项标 **UNKNOWN**，并给出我需要你补充的最小信息。
- 我不会说“已经修复/能跑/提升了”，除非闭环 PASS 条件满足（S430）。
