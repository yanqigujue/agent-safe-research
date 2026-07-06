# AFW Runtime Suite Summary

## Inputs

| Item | Value |
|---|---:|
| Suite ID | `afw_runtime_all_configs_suite` |
| Total runs | 10 |
| Total cases | 27 |
| Passed cases | 27 |
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
| total_runtime_fields | 25 |
| prevented_fields | 21 |
| false_allow_fields | 0 |
| false_block_fields | 0 |

## Runtime Decisions

| Metric | Value |
|---|---:|
| allow_cases | 4 |
| block_cases | 20 |
| abstain_cases | 3 |
| missing_cases | 0 |
| allow_fields | 4 |
| block_fields | 20 |
| abstain_fields | 1 |

## Counter-Authority

| Metric | Value |
|---|---:|
| cases_with_counter_authority | 1 |
| counter_authority_events | 1 |

## Authority Witness Audit

| Metric | Value |
|---|---:|
| total_fields_with_witness_audit | 25 |
| covers_need_fields | 6 |
| missing_role_fields | 19 |
| undischarged_obligation_fields | 1 |
| full_context_capability_count | 25 |
| witness_capability_count | 6 |
| irrelevant_capability_count | 19 |
| mean_compression_ratio | 0.760 |

## Source Types

| Source type | Value |
|---|---:|
| evidence | 8 |
| memory | 2 |
| prior_step_output | 2 |
| skill | 5 |
| tool_metadata | 2 |
| user_approval | 6 |

## Trace Adapter Diagnostics

| Metric | Value |
|---|---:|
| cases_with_invalid_trace_schema | 2 |
| invalid_events | 5 |
| unknown_events | 2 |

## Invalid Trace Reasons

| Reason | Value |
|---|---:|
| invalid_candidate_action | 1 |
| invalid_consumption_event | 1 |
| invalid_source_event | 1 |
| non_mapping_event | 2 |

## Ignored Trace Event Types

| Event type | Value |
|---|---:|
| <missing> | 1 |
| tool_call | 1 |

## Runs

| Run | Cases | Passed | Mean BehMatch | Prevented | False allow | False block |
|---|---:|---:|---:|---:|---:|---:|
| `20260701-092137-306200-afw-runtime-validation` | 8 | 8 | 1.000 | 7 | 0 | 0 |
| `20260701-092137-329788-afw-trace-adapter-runtime-validation` | 1 | 1 | 1.000 | 1 | 0 | 0 |
| `20260701-092137-338303-afw-trace-adapter-multisource-runtime-validation` | 6 | 6 | 1.000 | 6 | 0 | 0 |
| `20260701-092137-358271-afw-trace-adapter-malformed-runtime-validation` | 2 | 2 | 1.000 | 0 | 0 | 0 |
| `20260701-092137-369396-afw-trace-adapter-span-log-runtime-validation` | 2 | 2 | 1.000 | 2 | 0 | 0 |
| `20260701-092137-380075-afw-trace-adapter-otlp-runtime-validation` | 1 | 1 | 1.000 | 1 | 0 | 0 |
| `20260701-092137-389263-afw-trace-adapter-otlp-envelope-runtime-validation` | 1 | 1 | 1.000 | 1 | 0 | 0 |
| `20260701-092137-398444-afw-trace-adapter-obligation-runtime-validation` | 2 | 2 | 1.000 | 1 | 0 | 0 |
| `20260701-092137-409570-afw-trace-adapter-temporal-runtime-validation` | 2 | 2 | 1.000 | 1 | 0 | 0 |
| `20260701-092137-420058-afw-trace-adapter-counter-authority-runtime-validation` | 2 | 2 | 1.000 | 1 | 0 | 0 |
