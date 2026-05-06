---
id: S622
name: matplotlib_publication_script_builder
category: figure_ops
triggers:
  - matplotlib script
  - plot script
  - generate figure code
  - grouped bar
  - heatmap
  - radar plot
  - trend plot
  - svg png pdf
  - 绘图代码
  - python画图
  - 生成svg
  - 生成png
---
# S622 Matplotlib Publication Script Builder

## Source integration
This skill integrates code idioms from all `figures4papers-main/figure_*/*.py` scripts and API conventions from `scientific-figure-making/references/api.md`.

## Purpose
Use for creating or repairing Matplotlib scripts for publication-quality figures.

## Required ZYR routing
1. If input data are not provided, ask only for the minimal missing data fields or use explicitly labeled mock data if the user requested a design prototype.
2. If the figure is based on experimental results, route through `S303`, `S305`, `S311`, and `S322` before final figure generation.
3. After code generation, run `S402_code_audit` and `S431_closed_loop_verification` when execution is possible.

## Implementation rules
- Use Matplotlib as the default backend.
- Prefer explicit functions: `apply_publication_style`, `finalize_figure`, `save_figure`.
- Use `matplotlib.use("Agg")` in unattended scripts.
- Preserve reproducibility: fixed data input, output paths, and deterministic layout.
- Export at least one editable/vector format (`.svg` or `.pdf`) and one preview format (`.png`) when requested.
- Avoid seaborn when the execution environment or system instruction prohibits it; implement equivalent heatmaps or styles in Matplotlib directly.
- Do not hard-code unsupported scientific claims into annotations.

## Minimal script skeleton
```python
from __future__ import annotations
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def apply_publication_style() -> None:
    plt.rcParams.update({
        "font.family": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
        "axes.spines.right": False,
        "axes.spines.top": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })


def main() -> None:
    apply_publication_style()
    fig, ax = plt.subplots(figsize=(6.0, 3.8), constrained_layout=True)
    # draw data here
    fig.savefig("figure.svg", bbox_inches="tight")
    fig.savefig("figure.png", dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    main()
```

## Output schema
- `SCRIPT`
- `RUN_COMMAND`
- `OUTPUT_FILES`
- `STYLE_CHECKS`
- `KNOWN_LIMITATIONS`
