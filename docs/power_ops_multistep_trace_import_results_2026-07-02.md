# Power-Ops Trace Import Summary

## Inputs

| Item | Value |
|---|---:|
| Suite ID | `power_ops_multistep_trace_import` |
| Run ID | `20260702-034305-799343-power-ops-multistep-trace-import-validation` |
| Total cases | 1 |
| Passed cases | 1 |
| Failed cases | 0 |

## Import Boundary Coverage

| Boundary | Cases |
|---|---:|
| multi_step_trace | 1 |

## Source Type Coverage

| Metric | Value |
|---|---:|
| coverage_rate | 1.000 |
| missing_source_types | none |

| Source type | Events |
|---|---:|
| memory | 1 |
| prior_step_output | 1 |
| tool_metadata | 1 |
| user_approval | 1 |

## Import Diagnostics

| Metric | Value |
|---|---:|
| invalid_trace_cases | 0 |
| missing_source_cases | 0 |
| duplicate_approval_cases | 0 |
| expired_epoch_cases | 0 |
| missing_candidate_action_cases | 0 |

## Adapter Diagnostics

| Metric | Value |
|---|---:|
| cases_with_invalid_trace_schema | 0 |
| invalid_events | 0 |
| unknown_events | 0 |

| Invalid reason | Count |
|---|---:|

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
| `multistep-memory-tool-prior-approval-keep-fields-block-switching` | multi_step_trace | `block` | `fieldwise_repaired` | 0 | 0 | 0 | 0 |
