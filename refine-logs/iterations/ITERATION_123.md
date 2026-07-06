# Iteration 123 - Paper Kernel and Figure/Table Package

## Goal

Turn the accumulated power-ops action-invariance artifacts into paper-ready narrative, figures, and result tables.

## What Changed

- Added `docs/power_ops_action_invariance_paper_kernel_2026-07-02.md`.
- Added `docs/power_ops_action_invariance_figure_table_package_2026-07-02.md`.
- Added figure specs:
  - `figures/specs/power_ops_action_invariance_architecture.json`
  - `figures/specs/power_ops_action_invariance_repair_frame.json`
  - `figures/specs/power_ops_action_invariance_result_ladder.json`
- Rendered SVG figures:
  - `figures/power_ops_action_invariance_architecture.svg`
  - `figures/power_ops_action_invariance_repair_frame.svg`
  - `figures/power_ops_action_invariance_result_ladder.svg`
- Updated `README_POWER_OPS_ACTION_INVARIANCE.md`.
- Updated `figures/README.md`.
- Updated `task_plan.md`, `findings.md`, and `progress.md` with the continuous iteration backlog.

## Figure Package

| Figure | Purpose |
|---|---|
| Architecture | Explains `Cap(x)`, `Need(s,f)`, CapGuard coverage check, and fieldwise repair. |
| Repair frame | Explains the action-invariance invariant: preserve authorized fields and remove or review invalid fields. |
| Evidence ladder | Prevents claim inflation by separating L1-L4 artifact evidence from missing L5 production evidence. |

## Paper Kernel

The paper kernel now frames the work as:

```text
field-level action invariance under strict LLM-agent supervision
```

The safe claim is narrow:

- current artifact supports curated, trace, span/OTLP, AgentDojo-style bridge, and semi-real trace fixtures;
- current artifact does not support production safety or real operator workload reduction claims.

## Verification

- FigureSpec validation passed for all three new specs.
- SVG rendering passed for all three new figures after setting `PYTHONIOENCODING=utf-8`.

## Issue Log

| Issue | Resolution |
|---|---|
| Windows GBK console could not print the renderer's checkmark during validation. | Re-ran renderer with `$env:PYTHONIOENCODING='utf-8'`. |

## Next Iteration

Start the large-sample power-ops expansion:

```text
expanded JSONL suite + dataset audit + expanded validation YAML + expanded results
```
