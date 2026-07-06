# Power Operations AFW Coverage Matrix

## Summary

| Item | Value |
|---|---:|
| RAG paired rows | 32 |
| Generated trace rows | 40 |
| Source types | 6 |
| Laundered field families | 7 |
| Generated target roles | 19 |

## RAG Row Origins

| Item | Count |
|---|---:|
| `coverage_gap_closure` | 2 |
| `manual_paired_row` | 6 |
| `trace_role_confusion_generator` | 4 |
| `trace_scenario_adapter` | 20 |

## Source Types

| Item | Count |
|---|---:|
| `derived_artifact` | 8 |
| `evidence` | 12 |
| `memory` | 3 |
| `skill` | 1 |
| `tool_metadata` | 4 |
| `user_approval` | 4 |

## Laundered Field Families

| Item | Count |
|---|---:|
| `answer` | 4 |
| `approval` | 3 |
| `data_scope` | 2 |
| `delegation` | 1 |
| `parameters` | 1 |
| `risk_report` | 11 |
| `side_effect` | 10 |

## Top Generated Target Roles

| Item | Count |
|---|---:|
| `approval_authority` | 1 |
| `approval_waiver_authority` | 5 |
| `data_access_authority` | 2 |
| `dispatch_operation_authority` | 6 |
| `dispatch_order_authority` | 3 |
| `domain_safety_conclusion_authority` | 2 |
| `energization_authority` | 1 |
| `equipment_certification_authority` | 1 |
| `external_notification_authority` | 1 |
| `external_publish_authority` | 1 |
| `fault_isolation_authority` | 1 |
| `load_shedding_authority` | 1 |
| `operational_risk_authority` | 1 |
| `outage_execution_authority` | 1 |
| `privacy_disclosure_authority` | 1 |
| `risk_assessment_authority` | 5 |
| `safety_policy_authority` | 5 |
| `switching_authority` | 1 |
| `topology_change_authority` | 1 |

## Coverage Gaps

| Gap | Value |
|---|---|
| Missing source types | none |
| Missing laundered field families | none |
| Human plausibility labels | pending |
| Live model traces | pending |
