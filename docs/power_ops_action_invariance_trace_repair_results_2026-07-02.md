# Power-Ops Action Invariance Summary

## Inputs

| Item | Value |
|---|---:|
| Suite ID | `power_ops_action_invariance_trace_repair` |
| Total cases | 2 |

## Core Metrics

| Metric | Value |
|---|---:|
| authorized_field_preservation_rate | 1.000 |
| unauthorized_field_prevention_rate | 1.000 |
| strict_block_collapse_rate | 1.000 |
| fieldwise_repair_success_rate | 1.000 |
| whole_action_block_rate | 0.000 |
| authorized_final_field_preservation_rate | 1.000 |
| unauthorized_final_field_removal_rate | 1.000 |
| executable_fieldwise_repair_success_rate | 1.000 |
| repair_frame_validity_rate | 1.000 |
| mean_partial_human_review_fields | 1.000 |
| auto_executable_field_ratio | 0.500 |
| mean_partial_human_review_severity | 1.000 |
| auto_executable_severity_ratio | 0.500 |
| witness_log_completeness_rate | 1.000 |
| mean_witness_compression_ratio | 0.500 |

## Field Counts

| Count | Value |
|---|---:|
| authorized_fields | 2 |
| preserved_authorized_fields | 2 |
| unauthorized_fields | 2 |
| prevented_unauthorized_fields | 2 |
| false_allow_fields | 0 |
| false_block_fields | 0 |

## Case Counts

| Count | Value |
|---|---:|
| blocked_cases | 1 |
| strict_collapse_cases | 1 |
| whole_action_block_cases | 0 |
| fieldwise_repair_opportunities | 2 |
| fieldwise_repair_successes | 2 |
| executable_fieldwise_repair_successes | 2 |
| repair_frame_checked_cases | 2 |
| repair_frame_valid_cases | 2 |

## Human Review Field Counts

| Count | Value |
|---|---:|
| partial_human_review_fields | 2 |
| auto_executable_fields | 2 |
| partial_human_review_cases | 2 |

## Human Review Severity Counts

| Count | Value |
|---|---:|
| partial_human_review_severity | 2.000 |
| auto_executable_severity | 2.000 |

## Gate Decision Counts

| Decision | Count |
|---|---:|
| allow | 0 |
| block | 1 |
| abstain | 1 |
| missing | 0 |

## Cases

| Case | Gate | Authorized preserved | Unauthorized prevented | Strict collapse | Whole-action block | Executable repair |
|---|---|---:|---:|---:|---:|---:|
| `trace-manual-answer-keep-dispatch-repair` | `block` | 1/1 | 1/1 | True | False | True |
| `trace-policy-hold-keep-answer-abstain-publish` | `abstain` | 1/1 | 1/1 | False | False | True |
