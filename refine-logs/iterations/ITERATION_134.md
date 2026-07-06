# Iteration 134 - Table Row Evidence Binding

## Goal

Bind the main README result-table rows to result artifacts so table numbers can be audited row by row rather than treated as loose prose numbers.

## What Changed

- Added `formaltrust_platform/experiments/power_ops_table_evidence_binding.py`.
- Generated:
  - `docs/power_ops_action_invariance_table_evidence_binding_2026-07-02.md`
  - `docs/power_ops_action_invariance_table_evidence_binding_2026-07-02.json`
- Added test:
  - `test_power_ops_table_evidence_binding_maps_result_rows_to_artifacts`
- Updated:
  - `README_POWER_OPS_ACTION_INVARIANCE.md`
  - `task_plan.md`
  - `findings.md`
  - `progress.md`

## Binding Readback

| Item | Value |
|---|---:|
| tables | 3 |
| evidence files | 13 |
| fully supported rows | 18 |
| unsupported rows | 0 |

## Covered Tables

| Table | Rows | Status |
|---|---:|---|
| Current Result | 11 | fully supported |
| Baseline Grid | 4 | fully supported |
| Performance Profile | 3 | fully supported |

## TDD Record

| Test | Red Signal | Green Result |
|---|---|---|
| `test_power_ops_table_evidence_binding_maps_result_rows_to_artifacts` | missing `power_ops_table_evidence_binding` module | passed |

## Verification

| Check | Result |
|---|---|
| focused table binding test | 1 passed |
| `pytest tests/test_power_ops_action_invariance.py -q` | 30 passed |
| JSON parse / binding consistency check | passed |
| `pytest -q` | 230 passed |

## Keep / Revise / Reject

Keep. The table binding artifact proves that all README main-result rows currently agree with their source JSON artifacts.

## Boundary

The numeric audit has not yet consumed this binding artifact, so table numbers may still appear as `needs_evidence` there. The next iteration should connect the two.

## Next Iteration

Default next step:

```text
numeric audit with table binding
```

The next round should mark README table numbers as `supported_by_table_binding` when their contexts match a fully supported row.
