# Power-Ops Trace Import Summary

## Inputs

| Item | Value |
|---|---:|
| Suite ID | `power_ops_trace_import` |
| Run ID | `20260702-032625-980096-power-ops-trace-import-validation` |
| Total cases | 4 |
| Passed cases | 4 |
| Failed cases | 0 |

## Import Boundary Coverage

| Boundary | Cases |
|---|---:|
| duplicate_approval | 1 |
| expired_epoch | 1 |
| malformed_trace | 1 |
| missing_source | 1 |

## Import Diagnostics

| Metric | Value |
|---|---:|
| invalid_trace_cases | 1 |
| missing_source_cases | 1 |
| duplicate_approval_cases | 1 |
| expired_epoch_cases | 1 |
| missing_candidate_action_cases | 0 |

## Adapter Diagnostics

| Metric | Value |
|---|---:|
| cases_with_invalid_trace_schema | 1 |
| invalid_events | 1 |
| unknown_events | 0 |

| Invalid reason | Count |
|---|---:|
| non_mapping_event | 1 |

## Action-Invariance Readback

| Metric | Value |
|---|---:|
| whole_action_block_rate | 0.000 |
| authorized_final_field_preservation_rate | 1.000 |
| unauthorized_final_field_removal_rate | 1.000 |
| repair_frame_validity_rate | 1.000 |

## Cases

| Case | Boundary | Gate | Final | Missing source | Duplicate approval | Expired fields | Invalid trace |
|---|---|---|---|---:|---:|---:|---:|
| `trace-import-duplicate-approval-keep-work-order-block-switching` | duplicate_approval | `block` | `fieldwise_repaired` | 0 | 1 | 0 | 0 |
| `trace-import-expired-epoch-keep-answer-block-q4-publish` | expired_epoch | `block` | `fieldwise_repaired` | 0 | 0 | 1 | 0 |
| `trace-import-malformed-keep-answer-block-dispatch` | malformed_trace | `block` | `fieldwise_repaired` | 0 | 0 | 0 | 1 |
| `trace-import-missing-source-keep-answer-block-control` | missing_source | `block` | `fieldwise_repaired` | 1 | 0 | 0 | 0 |
