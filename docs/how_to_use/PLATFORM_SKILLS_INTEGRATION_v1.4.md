# Platform skills integration (DOCX • PDF • Spreadsheet) — ZYR v1.4.0

**Status:** repo-native guidance distilled from the runtime path `zyr_runtime_skills/**`.  
**Goal:** 把“平台内置的交付闭环（渲染→逐页验收）”变成 ZYR 的可迁移流程，并显式标注环境耦合点。

---

## 0) 总原则（ZYR 优先级不变）
1) **ZYR 仍是主协议**：banner + PRE-LOCK/LOCKED gate + UNKNOWN 标注 + 可审计输出。
2) 平台 skills 只提供 **工艺流程**（特别是视觉验收闭环），不改变 ZYR 的真值/证据纪律。
3) 任何“环境特有能力”（例如某些渲染/重算/导出引擎）只能作为**可选加速器**，不得写进对用户可复制的代码路径。

---

## 1) DOCX：`python-docx` 编辑 + 视觉验收闭环（强推荐）

### 1.1 闭环命令（可复制粘贴）
```bash
# 输入：input.docx
# 输出：artifacts/docx_render/input.pdf + artifacts/docx_render/input-1.png ...

OUTDIR=artifacts/docx_render
mkdir -p "$OUTDIR"

# DOCX -> PDF（必须隔离 UserInstallation，避免 LibreOffice 超时/锁）
soffice -env:UserInstallation=file:///tmp/lo_profile_$$ \
  --headless --convert-to pdf --outdir "$OUTDIR" input.docx

# PDF -> PNG（逐页）
pdftoppm -png "$OUTDIR/input.pdf" "$OUTDIR/input"

# 人工验收：逐页打开 PNG（100% zoom）
ls -1 "$OUTDIR" | sed -n '1,20p'
```

### 1.2 适用场景
- 你用 `python-docx` 批量改格式/表格/分页/图片布局时。
- 你做“可交付文档”而不是仅提取文本时。

### 1.3 迁移风险（必须显式声明）
- `soffice` 与 `pdftoppm` 在某些机器上可能不存在：需要在 `skills/reproducibility/S404_environment_capture_spec` 的环境捕获里列为依赖。

---

## 2) PDF：`reportlab` 生成 + 逐页验收（ZYR 已有基线）

### 2.1 推荐闭环
```bash
# 生成（ZYR 已提供示例脚本）
python tools/how_to_use/gen_ZIP-your-Research_HowToUse_v1_3_2.py

# 验收（逐页渲染）
mkdir -p artifacts/pdf_render
pdftoppm -png docs/how_to_use/ZIP-your-Research_How_to_Use_v1.3.2.pdf artifacts/pdf_render/how_to_use
```

### 2.2 迁移风险
- reportlab 版本差异通常可控，但仍建议在环境捕获里固定版本。

---

## 3) Spreadsheet：openpyxl 生成 + viewer 验收（公式/图表/CF）

### 3.1 基线原则（可迁移）
- **生成阶段**：openpyxl 写入 values / formulas / formats。
- **验收阶段（强制）**：
  - 用 Excel 或 LibreOffice 打开并保存，确认：
    - 公式结果显示正确（避免缓存空值/错误引用）。
    - 图表/条件格式渲染符合预期。

> 说明：openpyxl 本身通常不负责“计算公式结果”。不要把任何环境特有的“公式重算能力”当作用户必备依赖。

### 3.2 ZYR 内已有模板资产
- 参见审计：`docs/audits/AUDIT_platform_spreadsheets_examples_vs_ZYR_v1.3.2_addendum_20260222.md`
  - T1–T14：写入、样式、表格、图表、条件格式、引用列等。

### 3.3 常见坑（把它当 checklist 用）
- **动态数组函数**（如 XLOOKUP/SORT/FILTER/SEQUENCE）：迁移兼容性风险高 → 默认禁用。
- **图表/条件格式**：写入成功 ≠ 渲染成功 → 必须 viewer 目视验收。
- **来源引用**：web/外部数据 → 用“Source URL 列”或“cell comment”，避免 tool-internal token。

---

## 4) 与平台 `zyr_runtime_skills` 的关系（审计入口）
- 全量审计与对齐差异：
  - `docs/audits/AUDIT_platform_zyr_skills_docs_pdfs_spreadsheets_vs_ZYR_v1.4.0_20260222.md`



---

## v1.4.1 入口变更（模块化）
从 v1.4.1 起，平台 skills 的内容以独立模块形式沉淀在：
- `skills/platform_zyr_skills/`

本文件保留作为 legacy 入口页；权威内容请以模块内文档与审计表为准。
