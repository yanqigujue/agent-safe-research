# Iteration 118 - Human Review Burden Metrics

## Goal

Make "partial human review instead of whole-action collapse" measurable.

## What Changed

- Added human-review burden metrics to `formaltrust_platform/experiments/power_ops_action_invariance.py`.
- Added `test_action_invariance_summary_reports_human_review_burden`.
- Regenerated strict, fieldwise-repair, trace-repair, and span/OTLP repair reports.
- Added `docs/power_ops_action_invariance_human_review_burden_2026-07-02.md`.
- Updated `README_POWER_OPS_ACTION_INVARIANCE.md`.

## New Metrics

| Metric | Meaning |
|---|---|
| `mean_partial_human_review_fields` | Average number of fields per case routed to local human review. |
| `auto_executable_field_ratio` | Auto-executable fields divided by auto-executable plus partial-review fields. |
| `human_review_field_counts.partial_human_review_fields` | Total fields routed to local human review. |
| `human_review_field_counts.auto_executable_fields` | Total fields preserved for automatic execution. |

## Results

| suite | partial_human_review_fields | auto_executable_fields | mean_partial_human_review_fields | auto_executable_field_ratio |
|---|---:|---:|---:|---:|
| strict-block | 0 | 0 | 0.000 | 1.000 |
| fieldwise-repair | 10 | 10 | 1.000 | 0.500 |
| trace-repair | 2 | 2 | 1.000 | 0.500 |
| span-otlp-repair | 2 | 2 | 1.000 | 0.500 |

## Interpretation

Strict-block has no field-local review surface; it sends the whole action to human approval. Fieldwise repair creates a local review frame: in the current mixed cases, one field stays executable and one field goes to human review.

## Verification

| Command | Result |
|---|---|
| `pytest tests/test_power_ops_action_invariance.py::test_action_invariance_summary_reports_human_review_burden -q` | 1 passed |
| `pytest tests/test_afw_bench.py tests/test_interfaces.py tests/test_power_ops_action_invariance.py -q` | 99 passed |
| `pytest -q` | 213 passed |

## Keep / Revise / Reject

Keep. This metric directly supports the action-invariance framing, but it is still a field-count proxy. A future production claim needs real operator workload or review-time data.

## Next Iteration

Add external validity:

1. Real or semi-real power-agent trace logs.
2. AgentDojo-style task mapping.
3. Severity-weighted human-review burden.
