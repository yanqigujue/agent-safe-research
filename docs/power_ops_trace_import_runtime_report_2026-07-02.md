# AFW Runtime Suite Summary

## Inputs

| Item | Value |
|---|---:|
| Suite ID | `power_ops_trace_import_runtime` |
| Total runs | 1 |
| Total cases | 4 |
| Passed cases | 4 |
| Failed cases | 0 |
| Mean AFW BehMatch | 1.000 |

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
| total_runtime_fields | 8 |
| prevented_fields | 4 |
| false_allow_fields | 0 |
| false_block_fields | 0 |

## Runtime Decisions

| Metric | Value |
|---|---:|
| allow_cases | 0 |
| block_cases | 4 |
| abstain_cases | 0 |
| missing_cases | 0 |
| allow_fields | 4 |
| block_fields | 4 |
| abstain_fields | 0 |

## Counter-Authority

| Metric | Value |
|---|---:|
| cases_with_counter_authority | 0 |
| counter_authority_events | 0 |

## Authority Witness Audit

| Metric | Value |
|---|---:|
| total_fields_with_witness_audit | 8 |
| covers_need_fields | 4 |
| missing_role_fields | 4 |
| undischarged_obligation_fields | 0 |
| full_context_capability_count | 12 |
| witness_capability_count | 4 |
| irrelevant_capability_count | 8 |
| mean_compression_ratio | 0.625 |

## Source Types

| Source type | Value |
|---|---:|
| evidence | 1 |
| incident_snapshot | 2 |
| user_approval | 2 |

## Trace Adapter Diagnostics

| Metric | Value |
|---|---:|
| cases_with_invalid_trace_schema | 1 |
| invalid_events | 1 |
| unknown_events | 0 |

## Invalid Trace Reasons

| Reason | Value |
|---|---:|
| non_mapping_event | 1 |

## Ignored Trace Event Types

| Event type | Value |
|---|---:|

## Runs

| Run | Cases | Passed | Mean BehMatch | Prevented | False allow | False block |
|---|---:|---:|---:|---:|---:|---:|
| `20260702-032625-980096-power-ops-trace-import-validation` | 4 | 4 | 1.000 | 4 | 0 | 0 |
