# Iteration 121 - Semi-Real Power Trace Replay

## Goal

Move from curated metadata and bridge tasks toward semi-real power-operation span traces.

## What Changed

- Added `examples/data/power_ops_action_invariance_semireal_trace_cases.json`.
- Added `examples/power_ops_action_invariance_semireal_trace_validation.yaml`.
- Added `test_power_ops_semireal_trace_yaml_runs_with_severity_weighting`.
- Generated `docs/power_ops_action_invariance_semireal_trace_results_2026-07-02.md/json`.
- Added `docs/power_ops_action_invariance_semireal_trace_2026-07-02.md`.
- Updated `README_POWER_OPS_ACTION_INVARIANCE.md`.

## Results

| Metric | Value |
|---|---:|
| total_cases | 2 |
| passed_cases | 2 |
| gate counts | block=1, abstain=1 |
| authorized_final_field_preservation_rate | 1.000 |
| unauthorized_final_field_removal_rate | 1.000 |
| whole_action_block_rate | 0.000 |
| repair_frame_validity_rate | 1.000 |
| auto_executable_fields | 4 |
| partial_human_review_fields | 2 |
| auto_executable_severity | 6.000 |
| partial_human_review_severity | 10.000 |

## Interpretation

The new cases encode SCADA alarms, operator requests, incident snapshots, publish approvals, action spans, authority-use spans, and counter-authority spans. They remain curated, but their shape is closer to what an operations trace exporter could produce.

## Boundary

This is not a production trace export. It is a semi-real replay fixture that exercises the same interface expected from real traces.

## Next Iteration

Create a claim ledger for the action-invariance direction: which claims are backed by code/tests/results, which are only narrative, and which remain forbidden.
