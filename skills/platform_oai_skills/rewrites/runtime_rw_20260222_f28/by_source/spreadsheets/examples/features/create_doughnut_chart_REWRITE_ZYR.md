# Rewrite (portable): spreadsheets/examples/features/create_doughnut_chart.py

**Source (platform runtime):** `/home/oai/skills/spreadsheets/examples/features/create_doughnut_chart.py`
**Snapshot:** sha256 `7d0da34038f2a6e58d48a8cb68efb9b7b1d6bd3736d8a5fe4e10010527bdbe37` · 1735 bytes · mtime(UTC) `2025-12-10 20:38:37`
**Rewrite date:** 2026-02-22

## Intent and scope
Demonstration script showing `create_doughnut_chart.py` behavior in the platform spreadsheet artifact library.

## What the platform script does
- Seeds a small data table and adds a doughnut chart over a target cell range.
- Adds series with categories and values ranges, then renders the workbook to images.

## Portable template (ZYR)
Use openpyxl charts:

```python
from openpyxl.chart import DoughnutChart, Reference

# Assume ws has data in A1:C5 (headers in row 1).
chart = DoughnutChart()
chart.title = "Example"

data = Reference(ws, min_col=2, min_row=1, max_col=3, max_row=5)
cats = Reference(ws, min_col=1, min_row=2, max_row=5)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)

ws.add_chart(chart, "E2")
```

## ZYR alignment notes

| Topic | Status | Notes |
|---|---|---|
| Chart creation | PASS | openpyxl chart objects are portable. |
| Chart rendering to images | PARTIAL | Rendering requires external tooling; validate in Excel/LibreOffice. |
| Platform chart proto types | GAP | Do not bind to platform-specific proto imports. |

## QA checklist

- [ ] Open in Excel/LibreOffice and verify chart series, labels, and placement.
- [ ] Check that axis labels and legend are readable at normal zoom.
