# Iteration 185: Paper Figure/Table Package

## Goal

Generate paper-ready, evidence-bound figures and tables from the current authority-confusion and statistical robustness artifacts.

## Hypothesis

The main result contrasts can be represented as reusable SVG figures and LaTeX tables without manually copying numbers, as long as every figure/table records its source JSON.

## Implementation

- Added `formaltrust_platform/experiments/power_ops_paper_figure_table_package.py`.
- Added focused TDD test:
  - `test_power_ops_paper_figure_table_package_binds_figures_to_source_json`
- Generated artifacts:
  - `docs/power_ops_paper_figure_table_package_2026-07-02.md`
  - `docs/power_ops_paper_figure_table_package_2026-07-02.json`
  - `figures/power_ops_authority_confusion_baseline_grid.svg`
  - `figures/power_ops_statistical_interval_ladder.svg`
  - `figures/power_ops_paper_tables.tex`

## Readback

| Artifact | Value |
|---|---:|
| figure_count | 2 |
| table_count | 2 |

Source bindings:

- `power_ops_authority_confusion_baseline_grid.svg` binds to `docs/power_ops_authority_confusion_baseline_grid_2026-07-02.json`.
- `power_ops_statistical_interval_ladder.svg` binds to `docs/power_ops_statistical_robustness_2026-07-02.json`.
- `power_ops_paper_tables.tex` contains both the authority-confusion baseline table and the Wilson interval table.

## Verification

```powershell
pytest tests/test_power_ops_action_invariance.py::test_power_ops_paper_figure_table_package_binds_figures_to_source_json -q
```

Result:

```text
1 passed
```

## Keep / Revise / Reject

Keep. The package gives the paper/report layer concrete figures and tables while preserving evidence bindings. A future polish pass can improve typography or convert SVG to PDF if the final venue requires PDF-only figures.
