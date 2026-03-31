# Audit: Platform Spreadsheet Example Scripts → Reusable Templates → Alignment vs ZIP-your-Research (v1.3.2)

**Audit date:** 2026-02-22 (America/Los_Angeles)  
**Scope:** platform runtime examples at `zyr_runtime_skills/spreadsheets/examples/**/*.py`  
**Deliverable in this repo:** this audit file (template-first, repo-native).  

---

## 0) Why this audit exists
The platform runtime includes spreadsheet example scripts under `zyr_runtime_skills/spreadsheets/…`. Those scripts are **not** part of ZIP-your-Research. In a repo-first workflow, any “knowledge” that lives only in the runtime environment is **fragile** and breaks lossless migration.

This audit converts the examples into:
1) a **feature map** (what each example demonstrates),
2) a set of **reusable, repo-native templates** (portable blueprints),
3) a **protocol alignment diff** vs ZIP-your-Research principles.

---

## 1) Alignment rubric (ZIP-your-Research lens)
We evaluate each example against ZIP-your-Research invariants:

- **ZYR-T (Truthfulness / checkability):** deterministic behavior, explicit checks, minimal ambiguity.
- **ZYR-R (Repo-first reproducibility):** runnable with repo-declared dependencies and repo-contained inputs.
- **ZYR-P (Path hygiene):** avoid hard-coded machine paths; prefer explicit `--input/--output` and repo-relative outputs.
- **ZYR-D (Dependency disclosure):** dependencies must be explicit; environment-only dependencies must not become hidden “core”.
- **ZYR-C (Citation discipline):** if web-sourced facts enter a spreadsheet, include explicit source URLs/comments.

**Rating:**
- **PASS** = aligned by default
- **PARTIAL** = aligned intent, needs small refactor
- **GAP** = conflicts with repo-first portability or violates invariants

---

## 2) Reusable template library (repo-native blueprints)
Templates below are expressed in **openpyxl-first** terms (portable).

> Note: openpyxl typically does **not** evaluate Excel formulas. Formula results are computed when opening in Excel/LibreOffice. For correctness workflows, treat formula-caching as a separate, explicit step.

### T1 — Create workbook + sheets + write values + formulas
```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "Overview"
ws2 = wb.create_sheet("Employees")

ws["A1"].value = "Description"
ws["A2"].value = "Awesome Company Report"

ws2.append(["Title", "Name", "Address", "Score"])
ws2.append(["Engineer", "Vicky", "90 50th Street", 98])
ws2.append(["Manager", "Alex", "500 Market Street", 92])
ws2.append(["Designer", "Jordan", "200 Pine Street", 88])

ws2["A6"].value = "Total Score"
ws2["D6"].value = "=SUM(D2:D4)"

wb.save("report.xlsx")
```

### T2 — Style registry (header/highlight) + apply to ranges
```python
from openpyxl.styles import Font, PatternFill, Alignment

header_font = Font(bold=True)
header_fill = PatternFill("solid", fgColor="B7E1CD")
header_align = Alignment(horizontal="center", vertical="center")

for cell in ws2[1]:
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = header_align
```

### T3 — Column width / row height
```python
ws2.column_dimensions["C"].width = 13.16
ws2.row_dimensions[2].height = 35.25
```

### T4 — Merge cells + write top-left value
```python
ws2.merge_cells("C7:D7")
ws2["C7"].value = "Winner"
```

### T5 — Borders
```python
from openpyxl.styles import Border, Side
thin = Side(style="thin")
box = Border(left=thin, right=thin, top=thin, bottom=thin)
ws2["B9"].border = box
```

### T6 — Fills (solid + pattern)
```python
from openpyxl.styles import PatternFill
solid = PatternFill("solid", fgColor="F2CCFF")
ws2["A2"].fill = solid
```

### T7 — Font styles (capability note)
```python
from openpyxl.styles import Font
ws2["A5"].font = Font(bold=True, color="FF0000")
```

### T8 — Number formats
```python
ws2["B4"].number_format = "0.00"
ws2["B6"].number_format = "#,##0.00;[Red](#,##0.00)"
ws2["B22"].number_format = "00000"  # zip code
```

### T9 — Alignment + wrap
```python
from openpyxl.styles import Alignment
ws2["B7"].alignment = Alignment(horizontal="center", vertical="top", wrap_text=True)
```

### T10 — Conditional formatting (example)
```python
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import PatternFill

fill = PatternFill("solid", fgColor="CCE5FF")
rule = CellIsRule(operator='greaterThan', formula=['10'], fill=fill)
ws2.conditional_formatting.add("A2:C5", rule)
```

### T11 — Tables
```python
from openpyxl.worksheet.table import Table, TableStyleInfo

tab = Table(displayName="ScoresTable", ref="A1:C5")
style = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
tab.tableStyleInfo = style
ws2.add_table(tab)
```

### T12 — Charts
```python
from openpyxl.chart import LineChart, Reference

chart = LineChart()
chart.title = "Game Scores"
values = Reference(ws2, min_col=2, min_row=1, max_col=3, max_row=5)
chart.add_data(values, titles_from_data=True)
labels = Reference(ws2, min_col=1, min_row=2, max_row=5)
chart.set_categories(labels)
ws2.add_chart(chart, "E2")
```

### T13 — Load existing xlsx + inspect
```python
from openpyxl import load_workbook
wb = load_workbook("in.xlsx")
ws = wb.active
v = ws["B7"].value
style = ws["B7"]._style
wb.save("out.xlsx")
```

### T14 — Citation discipline (repo-native)
If spreadsheet rows encode web-sourced facts, add:
- a **Source URL** column, or
- a cell comment on the input cells.

---

## 3) Audit table: each platform example → features → template mapping → protocol diff

**Legend (Template mapping):** the “Templates” column lists template IDs (T1–T14).

| # | Platform example script | What it demonstrates (feature points) | Templates | Alignment vs ZIP-your-Research | Gap notes / recommended repo-native adjustments |
|---:|---|---|---|---|---|
| 1 | `create_basic_spreadsheet.py` | Workbook + sheets; cell/range writes; SUM formula; (platform) recalc/render/export | T1 | **PARTIAL** | Repo-native: keep T1; treat formula caching as explicit workflow; add CLI `--out`. |
| 2 | `create_spreadsheet_with_styling.py` | Reusable header/highlight styles; row/col sizing; formulas; merge; conditional formatting | T1,T2,T3,T4,T10 | **PARTIAL** | Port styles/CF to openpyxl APIs; add `--out` and deterministic file naming. |
| 3 | `styling_spreadsheet.py` | Conditional formatting fill; borders; alignment; merge; formula on merged range | T1,T3,T4,T5,T9,T10 | **PARTIAL** | Openpyxl equivalents exist; add visual regression step (open in Excel) for final QA. |
| 4 | `read_existing_spreadsheet.py` | Load existing xlsx; summary/style inspection; save/export (platform) | T13 | **GAP** | References a sample file path that is not provided. Repo-native: accept `--input`; include a sample xlsx if keeping as demo. |
| 5 | `features/create_area_chart.py` | Area chart with categories/values | T1,T12 | **PARTIAL** | Port to openpyxl `AreaChart`; verify chart rendering in Excel. |
| 6 | `features/create_bar_chart.py` | Vertical + horizontal/stacked bar charts | T1,T12 | **PARTIAL** | Port to `BarChart`; confirm grouping/direction properties. |
| 7 | `features/create_line_chart.py` | Line chart, multiple series | T1,T12 | **PARTIAL** | Direct port via `LineChart`. |
| 8 | `features/create_pie_chart.py` | Pie chart + legend placement | T1,T12 | **PARTIAL** | Port via `PieChart`; legend behavior varies by viewer. |
| 9 | `features/create_doughnut_chart.py` | Doughnut chart + legend | T1,T12 | **PARTIAL** | Port via `DoughnutChart`; verify. |
|10 | `features/create_tables.py` | Excel table + style, row stripes; width/height | T1,T3,T11 | **PARTIAL** | Use openpyxl tables; ensure unique table name. |
|11 | `features/set_cell_borders.py` | Border variants (thin/thick/double/dashed/diagonal/colored) | T5 | **PARTIAL** | Diagonal borders may need extra QA; prefer an exported-xlsx visual check. |
|12 | `features/set_cell_fills.py` | Solid + pattern fills; style reuse; vertical align; italics | T6,T9,T7 | **PARTIAL** | Port by reusing style objects or NamedStyle; avoid relying on “style index increments”. |
|13 | `features/set_cell_width_height.py` | Bulk column widths; row heights; default row height | T3 | **PASS** | Straight mapping; only add CLI paths. |
|14 | `features/set_conditional_formatting.py` | Wide coverage of conditional formatting types; precedence; reusable styles | T10 | **PARTIAL** | Openpyxl supports many CF rules, but not always 1:1; document unsupported types explicitly. |
|15 | `features/set_font_styles.py` | Typeface/family; bold/italic/color/underline; sizes; rich-text-like demo | T7,T9 | **PARTIAL** | Rich text is limited in openpyxl; treat as best-effort and document constraints. |
|16 | `features/set_merge_cells.py` | Merge; write via range/top-left; formatting on merged cell | T4,T6 | **PASS** | Straight mapping. |
|17 | `features/set_number_formats.py` | Number/date/time/percent/fraction/scientific formats; zip/phone/currency | T8 | **PARTIAL** | Script includes explicit TODO holes → do not treat as complete reference until filled. |
|18 | `features/set_text_alignment.py` | Horizontal/vertical alignment; notes about unsupported indent/rotation | T9 | **PARTIAL** | Track unsupported alignment features as explicit limitations. |
|19 | `features/set_wrap_text_styles.py` | Wrap vs auto; long text spill behavior; visual setup | T9 | **PASS** | Port is straightforward; shrink-to-fit support varies. |
|20 | `features/cite_cells.py` | Cell/range-level citation metadata demo (platform-specific concept) | T14 | **GAP** | Repo-native: represent citations as URL columns or cell comments. |
|21 | `features/change_existing_charts.py` | Load xlsx; list charts; delete a chart | T13,T12 | **GAP** | References a sample file path that is not provided. Openpyxl chart deletion is not always robust; document behavior. |

---

## 4) Consolidated delta summary
### Biggest systematic mismatches
1) **Non-repo-contained inputs** referenced by some examples → breaks reproducibility (ZYR-R).
2) **Viewer-dependent features** (charts/CF) need an explicit QA step (ZYR-T + ZYR-R).
3) **Citation representation** should be explicit and portable (ZYR-C).

### Minimal additive fix plan (if ZIP-your-Research wants first-class spreadsheet support later)
- Add a dedicated spreadsheet skill that:
  - uses openpyxl as the public API,
  - defines formula-caching/QA steps explicitly,
  - includes at least one repo-contained sample xlsx,
  - codifies citation discipline.

---

## 5) Decision record (append-only)
- We audited the platform spreadsheet examples and captured their feature map + a portable template library in this repo.
- We identified weakest links for repo-first use: missing sample inputs, viewer-dependent behavior, and non-portable citation mechanisms.
