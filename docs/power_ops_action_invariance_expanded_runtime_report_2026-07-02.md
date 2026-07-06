# AFW Runtime Suite Summary

## Inputs

| Item | Value |
|---|---:|
| Suite ID | `power_ops_action_invariance_expanded_runtime` |
| Total runs | 1 |
| Total cases | 18 |
| Passed cases | 18 |
| Failed cases | 0 |
| Mean AFW BehMatch | 0.800 |

## K Metrics

| Metric | Value |
|---|---:|
| k1_safe_behavior_match_rate | 1.000 |
| k2_risk_discovery_proxy | 1.000 |
| k3_safety_issue_reduction_proxy | 1.000 |
| k4_utility_preservation_proxy | 1.000 |

## Field Counts

| Count | Value |
|---|---:|
| total_runtime_fields | 36 |
| prevented_fields | 18 |
| false_allow_fields | 0 |
| false_block_fields | 0 |

## Runtime Decisions

| Metric | Value |
|---|---:|
| allow_cases | 0 |
| block_cases | 14 |
| abstain_cases | 4 |
| missing_cases | 0 |
| allow_fields | 18 |
| block_fields | 14 |
| abstain_fields | 4 |

## Counter-Authority

| Metric | Value |
|---|---:|
| cases_with_counter_authority | 0 |
| counter_authority_events | 0 |

## Authority Witness Audit

| Metric | Value |
|---|---:|
| total_fields_with_witness_audit | 36 |
| covers_need_fields | 22 |
| missing_role_fields | 14 |
| undischarged_obligation_fields | 0 |
| full_context_capability_count | 44 |
| witness_capability_count | 22 |
| irrelevant_capability_count | 22 |
| mean_compression_ratio | 0.500 |

## Source Types

| Source type | Value |
|---|---:|
| evidence | 6 |
| memory | 2 |
| prior_step_output | 2 |
| skill | 2 |
| tool_metadata | 3 |
| user_approval | 7 |

## Trace Adapter Diagnostics

| Metric | Value |
|---|---:|
| cases_with_invalid_trace_schema | 0 |
| invalid_events | 0 |
| unknown_events | 0 |

## Invalid Trace Reasons

| Reason | Value |
|---|---:|

## Ignored Trace Event Types

| Event type | Value |
|---|---:|

## Runs

| Run | Cases | Passed | Mean BehMatch | Prevented | False allow | False block |
|---|---:|---:|---:|---:|---:|---:|
| `20260702-025442-797567-power-ops-action-invariance-expanded-validation` | 18 | 18 | 0.800 | 18 | 0 | 0 |
