# Iteration 124 - Large-Sample Power-Ops Expansion

## Goal

Expand the curated power-ops action-invariance suite beyond the original 10 cases and add a dataset audit path.

## What Changed

- Added `formaltrust_platform/experiments/power_ops_action_invariance_dataset_audit.py`.
- Added `examples/data/power_ops_action_invariance_expanded_cases.jsonl`.
- Added `examples/power_ops_action_invariance_expanded_validation.yaml`.
- Added tests:
  - `test_power_ops_expanded_dataset_audit_reports_coverage`
  - `test_power_ops_expanded_fieldwise_repair_yaml_runs_through_afw_runtime_graph`
- Added reports:
  - `docs/power_ops_action_invariance_expanded_dataset_audit_2026-07-02.md`
  - `docs/power_ops_action_invariance_expanded_dataset_audit_2026-07-02.json`
  - `docs/power_ops_action_invariance_expanded_runtime_report_2026-07-02.md`
  - `docs/power_ops_action_invariance_expanded_runtime_report_2026-07-02.json`
  - `docs/power_ops_action_invariance_expanded_results_2026-07-02.md`
  - `docs/power_ops_action_invariance_expanded_results_2026-07-02.json`
- Updated README, paper kernel, figure/table package, claim ledger, task plan, findings, and progress.

## TDD

The new focused tests first failed because the dataset audit module did not exist:

```text
ModuleNotFoundError: formaltrust_platform.experiments.power_ops_action_invariance_dataset_audit
```

After adding the module, expanded dataset, and YAML:

```text
2 passed
```

## Expanded Dataset

| Metric | Value |
|---|---:|
| total cases | 18 |
| oracle coverage rate | 1.000 |
| authorized fields | 18 |
| unauthorized fields | 18 |
| block decisions | 14 |
| abstain decisions | 4 |
| source types | 6 |
| critical severity labels | 6 |

## Runtime Result

| Suite | Cases | Passed | Whole-action block | Executable repair | Repair validity |
|---|---:|---:|---:|---:|---:|
| expanded-fieldwise | 18 | 18 | 0.000 | 1.000 | 1.000 |

## Keep / Revise / Reject

Keep. The larger curated suite preserves the current fieldwise-repair claim and gives the next iteration a better base for systematic mutation.

## Next Iteration

Build action-invariance metamorphic tests:

```text
base valid action -> mutate invalid authority role/scope/counter/time -> verify authorized fields remain unchanged
```
