# Iteration 183: Authority-Confusion Baseline Grid

## Goal

Compare role-aware CapGuard against simpler supervision variants on the trace-derived authority-confusion rows.

## Hypothesis

Boundary-only and attribution-only baselines should miss boundary-preserving semantic role confusion, while strict blocking should catch the confusion only by falsely blocking legal rows. CapGuard should preserve legal rows and block role-confused rows.

## Implementation

- Added `formaltrust_platform/experiments/power_ops_authority_confusion_baseline_grid.py`.
- Added focused TDD test:
  - `test_power_ops_authority_confusion_baseline_grid_separates_role_aware_from_boundary_only`
- Generated artifacts:
  - `docs/power_ops_authority_confusion_baseline_grid_2026-07-02.md`
  - `docs/power_ops_authority_confusion_baseline_grid_2026-07-02.json`

## Readback

| Metric | Value |
|---|---:|
| row_count | 10 |
| baseline_count | 5 |
| capguard legal preservation | 1.000 |
| capguard confusion block | 1.000 |
| capguard false allow | 0.000 |
| boundary_scope_only false allow | 1.000 |
| field_attribution_only false allow | 1.000 |
| strict_block false block | 1.000 |
| capguard_role_confusion_advantage | 1.000 |

## Verification

```powershell
pytest tests/test_power_ops_action_invariance.py::test_power_ops_authority_confusion_baseline_grid_separates_role_aware_from_boundary_only -q
```

Result:

```text
1 passed
```

## Keep / Revise / Reject

Keep. This is a strong ablation for the core novelty story: the semantic role part of `Need(s,f)` catches a failure mode that boundary-only and source-attribution-only checks miss, while strict blocking is too conservative.
