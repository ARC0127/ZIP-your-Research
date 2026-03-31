# Audit: `/home/oai/skills` (DOCX • PDF • Spreadsheet) → Reusable Templates → Alignment vs ZIP-your-Research (v1.4.0)

**Audit date:** 2026-02-22 (America/Los_Angeles)  
**Scope:** platform runtime guidance + scripts under `/home/oai/skills/**` (local filesystem audit).  
**Goal:** 查漏补缺：把 `/home/oai/skills` 全部文件做成 **可移植模板** + **与 ZYR 协议的对齐差异**，并落到 repo 内文档，避免“只存在于运行环境”的知识丢失。  

> 本文不复制平台文件原文到 ZYR（尤其涉及环境内置/专用组件的部分），只做**审计摘要 + 可复用模板（repo-native）**。

---

## 0) 背景：为什么需要把平台 skill 做 repo 化
- `/home/oai/skills` 是**运行环境注入的工作流规范与示例**，不属于 ZYR release zip。若不沉淀为 repo 文档，会导致：
  - 换环境后无法复现同样的交付质量（例如 DOCX/PDF 的“渲染→逐页 PNG 视觉验收”循环）。
  - Spreadsheet 的“公式缓存/渲染检查”在不同环境中表现差异大，容易产生隐性错误。
- ZYR 的核心是**repo-first + 可审计**。因此我们把平台技能映射为：
  1) **可复用模板**（open-source 依赖优先）
  2) **对齐差异**（明确哪些点属于平台假设、哪些点必须在 ZYR 中显式声明）

---

## 1) 审计对象清单（全量）
### 1.1 文件枚举（按路径）
- `docs/`
  - `docs/skill.md`
  - `docs/render_docx.py`
- `pdfs/`
  - `pdfs/skill.md`
- `spreadsheets/`
  - `spreadsheets/skill.md`
  - `spreadsheets/spreadsheet.md`
  - `spreadsheets/artifact_tool_spreadsheets_api.md`
  - `spreadsheets/artifact_tool_spreadsheet_formulas.md`
  - `spreadsheets/examples/**.py`（已在上一份审计中覆盖；见 §6）

### 1.2 完整性校验（sha256 快照）
> 目的：未来若平台更新，可直接对比差异。

```text
# sha256sum (relative to /home/oai/skills)
aa90e7455a45ffb1051cda0db3bc5a39fe402e93f178197e471f84fc864bbe01  ./docs/render_docx.py
3371beed114ef5a2c103367d5102c8b36ca19896e5499c266a9dea50c6bea637  ./docs/skill.md
76af35f8932f3cda08a5438605f87789670bd90d720f67cf0aa7af9ddad4e7f4  ./pdfs/skill.md
b5299c87e4dc0a2e0c077eec369a4998cd890a69b32fbb28572c73c272c4b228  ./spreadsheets/artifact_tool_spreadsheet_formulas.md
a99e138a3ecdd2d43ff637367a4a9ddf58cc123ed55de4d19d02f606c2daf6f4  ./spreadsheets/artifact_tool_spreadsheets_api.md
f9f4af1b0a0e753687e1ae101436821f0d6a4f03694ce3075fe59818601a7dab  ./spreadsheets/examples/create_basic_spreadsheet.py
7f0428c3cf395ff95a727faa616709847c1d9495f2f59f830ef5c188f8e96c69  ./spreadsheets/examples/create_spreadsheet_with_styling.py
9431a3594a80df040b493e2ac0616dbef4c5b0d8bcb76d9797268a24c29b31b8  ./spreadsheets/examples/features/change_existing_charts.py
3c36e6d30e7214f4ee24778847982e4bdbbfa783db53e59f2ef573c41f485ac0  ./spreadsheets/examples/features/cite_cells.py
85ec32424db765ed103d1355dd4fad394c207e6b54b0ac26c5305d64cc9307f9  ./spreadsheets/examples/features/create_area_chart.py
2664599a7859c1bb0ff28d318c404fb0c02cb5db596378a90f39ec97a2d22421  ./spreadsheets/examples/features/create_bar_chart.py
7d0da34038f2a6e58d48a8cb68efb9b7b1d6bd3736d8a5fe4e10010527bdbe37  ./spreadsheets/examples/features/create_doughnut_chart.py
9144a9f45fffe6fd4e28b1546587c430cd301d96277adcff88508c5b6d527ecd  ./spreadsheets/examples/features/create_line_chart.py
ad854287aac4647196141b28b87a594ff5f30393097955ebeb341ace7054f3ef  ./spreadsheets/examples/features/create_pie_chart.py
07a8e02a990c9b0e42395f155840ecbf9b82f27d010037f8105fa9a5f9505916  ./spreadsheets/examples/features/create_tables.py
43fcc0f89ef9b31f0fb9f45cd3019273446720754f7e6c903079bdbe7f018b00  ./spreadsheets/examples/features/set_cell_borders.py
c53f0d45b0112c8e252f0857ee0c7fa108c0adaa3334f714b8616e9f35a50990  ./spreadsheets/examples/features/set_cell_fills.py
c35b8d4af394589a7a738486af13bf1cb7f4fe26bc397bc41e8e57b3ea0f196a  ./spreadsheets/examples/features/set_cell_width_height.py
69cc7d58ebe5fc83179760275194c132792a26d10d12c28c7187a9dc5c7dab96  ./spreadsheets/examples/features/set_conditional_formatting.py
4f2c3ee5de77e5bda20db60438ed66e268b8c154654933779504f01c89fc1a74  ./spreadsheets/examples/features/set_font_styles.py
ff4be68b2b2048bc29612b29ab10e1e6ddec6bc1aecf6f02805620fb229d3565  ./spreadsheets/examples/features/set_merge_cells.py
9d13a14599e280be6e24409273c4cd278bc564c75c9d0b7ff8ae9564ebcf35cd  ./spreadsheets/examples/features/set_number_formats.py
5c9aab970b4403e3ad93fd5070670234acbd8bf645b1492ccdc2f3e1ee2e9518  ./spreadsheets/examples/features/set_text_alignment.py
2d107a03be0227fdbb364843cc7f9a6a68139e17257d51b26505bc82bcfa6300  ./spreadsheets/examples/features/set_wrap_text_styles.py
a2139b360086a0a94e7f5b3c5dc67ff99dc02602d397ea9aa575e2f01e2adc54  ./spreadsheets/examples/read_existing_spreadsheet.py
970760cf3d819e140d4f863798a717f53b7e36d5ebac85feb0b95229f11d1fcc  ./spreadsheets/examples/styling_spreadsheet.py
cef2ed8d3e50f618914f7d68c98c2158461f00e83ad836e1033cf236e48131ed  ./spreadsheets/skill.md
e953dc28faf645ba2972c590d2cb7d7585e1112cf48c7d5b741292093ccd982f  ./spreadsheets/spreadsheet.md
```


---

## 2) 对齐评估 rubric（ZYR 视角）
与上一份 spreadsheets 示例审计一致，额外补充 2 个维度：

- **ZYR-V (Visual QA discipline):** 是否强制“渲染→逐页图片肉眼验收”的闭环。
- **ZYR-S (Sandbox coupling risk):** 是否假设了环境内置组件/工具，导致迁移不可用。

评级：**PASS / PARTIAL / GAP**。

---

## 3) 可复用模板库（repo-native）

### T-DOCX-1 — DOCX 编辑闭环：`python-docx` → PDF → PNG → 逐页验收
**目的：**把平台 docs skill 的核心优势（视觉验收闭环）迁移到 ZYR。

**模板（命令行闭环）：**
```bash
# 0) 约定：所有中间产物输出到 results/ 或 artifacts/，避免污染根目录
OUTDIR=artifacts/docx_render
mkdir -p "$OUTDIR"

# 1) DOCX -> PDF（LibreOffice headless；必须隔离 UserInstallation）
soffice -env:UserInstallation=file:///tmp/lo_profile_$$ \
  --headless --convert-to pdf --outdir "$OUTDIR" input.docx

# 2) PDF -> PNG（逐页）
pdftoppm -png "$OUTDIR/input.pdf" "$OUTDIR/input"

# 3) 人工验收：打开 PNG（100% zoom）逐页检查
ls -1 "$OUTDIR" | head
```

**ZYR 对齐点：**
- ZYR-V：强 PASS（把“视觉验收”提升到强制闭环）。
- ZYR-R：PARTIAL（依赖系统可执行 `soffice` 与 `pdftoppm`；需在 repropack/environment 里显式声明）。

### T-PDF-1 — PDF 生成闭环：`reportlab` → PNG → 逐页验收
**目的：**把平台 pdf skill 的核心优势（reportlab + 渲染验收）迁移到 ZYR。

**模板：**
```bash
python tools/how_to_use/gen_ZIP-your-Research_HowToUse_v1_3_2.py
pdftoppm -png docs/how_to_use/ZIP-your-Research_How_to_Use_v1.3.2.pdf artifacts/pdf_render/how_to_use
```

**ZYR 对齐点：**
- ZYR-V：PASS。
- ZYR-R：PASS（reportlab 已在 ZYR 工具链里出现；但仍建议在环境捕获里声明）。

### T-XLSX-1 — XLSX 构建：openpyxl 生成 + viewer 校验（公式/图表）
**目的：**避免把“环境内置重算/渲染能力”当作用户可用依赖。

**模板（原则）：**
- 生成：用 openpyxl 写值、写公式、写样式。
- 校验：
  - **公式结果**：用 Excel/LibreOffice 打开并保存（让计算引擎写入缓存），或在你的工具链中提供一个“可重算”的步骤（若可用）。
  - **图表/CF**：必须 viewer 里目视确认（openpyxl 的写入不等于渲染一致）。

---

## 4) 审计表（逐文件）：功能点 → 模板 → 对齐差异

| 类别 | 平台文件 | 功能点摘要 | 模板映射 | 对齐评级 | 主要差异/风险 | ZYR 集成建议（最小改动） |
|---|---|---|---|---|---|---|
| DOCX | `docs/skill.md` | 提出“DOCX→PDF→PNG→逐页验收”闭环；强调 `soffice -env:UserInstallation=...` 防止超时 | T-DOCX-1 | **PARTIAL** | 平台默认存在 `soffice/pdftoppm`；ZYR 没有显式写入环境捕获 | 新增 `docs/how_to_use/PLATFORM_SKILLS_INTEGRATION_v1.4.md`（见 §7）；在 repropack 中把 LO/pdftoppm 列为必需工具 |
| DOCX | `docs/render_docx.py` | 脚本化渲染：优先解析 DOCX 纸张尺寸 → 估算 DPI → rasterize PNG；失败则 DOCX→PDF→PNG | T-DOCX-1 | **GAP** | 脚本本身依赖平台上下文（内部渲染链）；迁移后可能不可运行 | 在 ZYR 中只保留“闭环流程”，不把该脚本当必需依赖；若要产品化，再单独做一份 repo-native 渲染工具 |
| PDF | `pdfs/skill.md` | 提倡 reportlab 生成；每次更新后 `pdftoppm` 渲染验收；禁止某些 unicode dash | T-PDF-1 | **PASS** | 与 ZYR 现有 how-to-use PDF 生成方式一致 | 在 integration doc 里把“PDF->PNG 逐页验收”写成强制 QA |
| XLSX | `spreadsheets/skill.md` | 公式必须用公式；禁动态数组函数；强调“重算 + 渲染检查”；提出样式与数字格式规范 | T-XLSX-1 +（上一份审计的 T1–T14） | **PARTIAL** | 平台假设存在额外的“重算/渲染能力”；但用户环境可能没有 | ZYR 文档里把“公式缓存/重算”标为 **环境能力可选**，默认走 viewer 校验；禁止把平台能力写进用户代码 |
| XLSX | `spreadsheets/spreadsheet.md` | 描述一个“SpreadsheetArtifact”对象模型（读取/渲染/导出/重算） | T-XLSX-1 | **GAP** | 强绑定平台内部库；直接迁移会造成依赖幻觉 | 只抽取“操作顺序”和“验收口径”，不抽取 API 细节 |
| XLSX | `artifact_tool_spreadsheets_api.md` | 内部库 API 参考（类/方法/字段） | N/A | **GAP** | 属于环境内部参考，迁移会产生“看得见却用不了”的假象 | 不 vendor；只在审计中记录“存在该类文档”，并把 ZYR 的对外接口固定为 openpyxl/pandas |
| XLSX | `artifact_tool_spreadsheet_formulas.md` | 内部计算引擎支持的 Excel 函数白名单 | N/A | **PARTIAL** | 可作为“兼容性提示”，但不同 viewer 引擎差异仍在 | 在 ZYR spreadsheet workflow 中新增“函数兼容性提示”小节：不承诺所有函数可重算 |

---

## 5) 关键缺口（查漏补缺结果）
### 5.1 ZYR 当前缺少“DOCX 交付闭环”显式写法
- ZYR 已覆盖 PDF 生成（reportlab），但 **DOCX 的 render→inspect 过程未显式文档化**。
- 平台 docs skill 的最大价值就是：强制视觉验收，避免“文本抽取看不见表格/图/排版”问题。

### 5.2 Spreadsheet 的“重算/渲染”在迁移中必须降级为可选能力
- 平台 skill 强调“必须重算并缓存公式结果”。这在某些环境可实现，但**不能假设对用户可用**。
- 因此：ZYR 的对外、可移植模板必须以 **openpyxl 生成 + viewer 验收**为基线。

### 5.3 示例脚本存在“样例文件缺失”的可复现性问题
- 见上一份审计：部分脚本引用 `sample_xlsx/*.xlsx` 但目录不存在。
- 这类例子只能作为“特性展示”，不能作为可运行基线。

---

## 6) 与上一份 spreadsheets 示例审计的关系
- 已存在：`docs/audits/AUDIT_platform_spreadsheets_examples_vs_ZYR_v1.3.2_addendum_20260222.md`
- 本文新增覆盖：
  - DOCX/PDF 两类 skill
  - spreadsheet 的“对象模型文档/函数白名单/API 参考”
  - 与 ZYR 的集成策略（不引入环境耦合）

---

## 7) 最小集成落地（本次 v1.4.0 实际在 repo 中做了什么）
本次 release 会新增一份**短小、可复制粘贴**的集成指南：
- `docs/how_to_use/PLATFORM_SKILLS_INTEGRATION_v1.4.md`

它将：
- 把 DOCX/PDF/XLSX 的“渲染验收闭环”写成可执行流程
- 明确：平台能力 ≠ 用户能力；对外模板默认 open-source 工具链

---

## 8) Decision record (append-only)
- 我们完成了 `/home/oai/skills` 的全量清单化审计，并把“可移植模板 + 对齐差异”落到 repo 文档。
- 我们显式拒绝把平台内部 API 文档作为 ZYR 的“依赖”，只将其转化为**验收口径与兼容性提示**。
