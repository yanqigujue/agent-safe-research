# Iteration 184: Statistical Robustness

## Goal

Add confidence intervals around current fixture-level point estimates so the paper can report uncertainty honestly.

## Hypothesis

Wilson intervals can make perfect fixture rates such as 16/16 or 10/10 reportable without pretending they are production population guarantees.

## Implementation

- Added `formaltrust_platform/experiments/power_ops_statistical_robustness.py`.
- Added focused TDD test:
  - `test_power_ops_statistical_robustness_reports_wilson_intervals`
- Generated artifacts:
  - `docs/power_ops_statistical_robustness_2026-07-02.md`
  - `docs/power_ops_statistical_robustness_2026-07-02.json`

## Readback

| Metric | Count | Wilson 95% CI |
|---|---:|---|
| normal authorized-field preservation | 16/16 | [0.8064, 1.0000] |
| CapGuard confusion block | 10/10 | [0.7225, 1.0000] |
| CapGuard false allow | 0/10 | [0.0000, 0.2775] |
| boundary-scope-only false allow | 10/10 | [0.7225, 1.0000] |
| strict-block false block | 10/10 | [0.7225, 1.0000] |

## Verification

```powershell
pytest tests/test_power_ops_action_invariance.py::test_power_ops_statistical_robustness_reports_wilson_intervals -q
```

Result:

```text
1 passed
```

## Keep / Revise / Reject

Keep. This creates a more honest reporting layer for the current point estimates. The next iteration should convert the main results into paper-ready figures and tables with explicit source JSON bindings.
