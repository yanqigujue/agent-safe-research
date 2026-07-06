# Iteration 120 - Severity-Weighted Review Burden

## Goal

Separate field-count review burden from risk-weighted review burden.

## What Changed

- Added severity-weighted review metrics to `formaltrust_platform/experiments/power_ops_action_invariance.py`.
- Added `test_action_invariance_summary_reports_severity_weighted_review_burden`.
- Updated the AgentDojo-style mapping test to assert severity totals.
- Added `field_severity` annotations to `examples/data/power_ops_action_invariance_agentdojo_style_cases.json`.
- Regenerated action-invariance reports.
- Added `docs/power_ops_action_invariance_severity_weighted_review_2026-07-02.md`.
- Updated `README_POWER_OPS_ACTION_INVARIANCE.md`.

## New Metrics

| Metric | Meaning |
|---|---|
| `human_review_severity_counts.partial_human_review_severity` | Total severity weight routed to human review. |
| `human_review_severity_counts.auto_executable_severity` | Total severity weight preserved for automatic execution. |
| `mean_partial_human_review_severity` | Average review severity per case. |
| `auto_executable_severity_ratio` | Auto-executable severity divided by auto plus review severity. |

## Results

| suite | auto fields | review fields | auto severity | review severity | auto severity ratio |
|---|---:|---:|---:|---:|---:|
| agentdojo-style | 4 | 2 | 6.000 | 10.000 | 0.375 |

## Interpretation

The bridge suite has only two review fields, but those fields carry most of the severity weight. This better matches power-operation safety intuition: a single breaker-opening or external-disclosure field can dominate review burden.

## Boundary

The current severity weights are engineering defaults, not expert-calibrated field risks. A deployment claim still needs domain severity calibration and real review-time data.

## Next Iteration

Add semi-real power trace cases with severity labels, preferably using span/OTLP structure.
