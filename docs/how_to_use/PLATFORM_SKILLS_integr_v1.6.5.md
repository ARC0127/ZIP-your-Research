# Platform Artifact Workflows for ZYR v1.6.5

This guide maps platform artifact requests to the ZYR engine-binding discipline.

## DOCX / Word

```text
document request
→ writing_engine
→ proof_engine first if logic or claims are being constructed
→ S640 for writing/logic gate
→ document tooling
→ final file + revision report
```

## PDF

```text
PDF reading / revision / audit
→ writing_engine or proof_engine depending on task
→ cite extracted evidence when reporting claims
→ final report or regenerated PDF when requested
```

## Spreadsheets

```text
spreadsheet task
→ coding_engine or experiment workflow
→ preserve formulas / sheets / units
→ validate calculations
→ final spreadsheet + validation notes
```

## Figures

```text
figure request
→ figure_engine
→ inspect ext/src/figures/
→ preserve source-generation and structured data-loading logic
→ export requested format when suitable
```
