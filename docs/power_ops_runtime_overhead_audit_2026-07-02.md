# Power-Ops Runtime Overhead Audit

This is a proxy-only overhead audit. It reports field-check units and audit-compression ratios, not wall-clock latency.

## Aggregate

| Metric | Value |
|---|---:|
| suite_count | 6 |
| action_suite_count | 5 |
| paired_authority_suite_count | 1 |
| total_field_check_proxy_units | 108 |
| max_field_check_proxy_units_per_case | 6 |
| weighted_mean_audit_compression_ratio | 0.587963 |
| wall_clock_latency_available | false |

## Action Suites

| Suite | Cases | Field checks | Max checks/case | Audit compression |
|---|---:|---:|---:|---:|
| `power_ops_action_invariance_expanded` | 18 | 36 | 2 | 0.500000 |
| `power_ops_action_invariance_metamorphic` | 4 | 8 | 2 | 0.687500 |
| `power_ops_skill_authority` | 8 | 16 | 2 | 0.500000 |
| `power_ops_planner_skill_tool_memory` | 2 | 12 | 6 | 0.833333 |
| `power_ops_normal_behavior_stress` | 4 | 16 | 4 | 0.750000 |

## Paired Authority Suites

| Suite | Rows | Field checks | Audit compression |
|---|---:|---:|---:|
| `power_ops_trace_authority_confusion` | 10 | 20 | 0.500000 |
