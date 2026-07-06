# Power-Ops Action Invariance Dataset Audit

## Inputs

| Item | Value |
|---|---:|
| Dataset | `examples\data\power_ops_skill_authority_cases.jsonl` |
| Total cases | 8 |
| Oracle coverage rate | 1.000 |
| Authorized fields | 8 |
| Unauthorized fields | 8 |

## Case Shape Counts

| Key | Count |
|---|---:|
| `action_invariance_oracle` | 8 |
| `afw_consumptions` | 8 |
| `afw_oracle` | 8 |
| `afw_source_events` | 8 |
| `candidate_action` | 8 |

## Gate Decision Counts

| Key | Count |
|---|---:|
| `block` | 8 |

## Source Type Counts

| Key | Count |
|---|---:|
| `memory` | 1 |
| `prior_step_output` | 1 |
| `skill` | 4 |
| `tool_metadata` | 1 |
| `user_approval` | 1 |

## Field Counts

| Key | Count |
|---|---:|
| `answer` | 1 |
| `approval_waiver` | 1 |
| `dispatch` | 2 |
| `dispatch_order` | 1 |
| `plan_note` | 1 |
| `public_publish` | 2 |
| `risk_level` | 3 |
| `risk_report` | 1 |
| `risk_report_style` | 1 |
| `switching_operation` | 2 |
| `tool_arguments` | 1 |

## Required Role Counts

| Key | Count |
|---|---:|
| `approval_public_publish_authority` | 1 |
| `approval_waiver_authority` | 1 |
| `dispatch_operation_authority` | 2 |
| `dispatch_preparation_skill` | 1 |
| `incident_summary_skill` | 1 |
| `memory_preference_authority` | 1 |
| `planner_suggestion_role` | 1 |
| `public_communication_authority` | 1 |
| `report_formatting_skill` | 1 |
| `risk_assessment_authority` | 3 |
| `switching_authority` | 2 |
| `tool_schema_authority` | 1 |

## Severity Counts

| Key | Count |
|---|---:|
| `critical` | 8 |
| `high` | 1 |
| `low` | 3 |
| `medium` | 4 |

## Risk Level Counts

| Key | Count |
|---|---:|
| `critical` | 3 |
| `high` | 5 |

## Tag Counts

| Key | Count |
|---|---:|
| `action_invariance` | 8 |
| `afw` | 8 |
| `no_rag` | 8 |
| `power_ops` | 8 |
| `skill_driven` | 8 |
