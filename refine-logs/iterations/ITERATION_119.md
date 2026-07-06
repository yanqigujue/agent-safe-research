# Iteration 119 - AgentDojo-Style Power-Ops Mapping

## Goal

Increase external validity by mapping AgentDojo-style task structures into the power-ops action-invariance interface.

## What Changed

- Added `examples/data/power_ops_action_invariance_agentdojo_style_cases.json`.
- Added `examples/power_ops_action_invariance_agentdojo_style_validation.yaml`.
- Added `test_power_ops_agentdojo_style_mapping_yaml_runs_through_afw_runtime_graph`.
- Generated `docs/power_ops_action_invariance_agentdojo_style_results_2026-07-02.md/json`.
- Added `docs/power_ops_action_invariance_agentdojo_style_mapping_2026-07-02.md`.
- Updated `README_POWER_OPS_ACTION_INVARIANCE.md`.

## Results

| Metric | Value |
|---|---:|
| total_cases | 2 |
| passed_cases | 2 |
| authorized_final_field_preservation_rate | 1.000 |
| unauthorized_final_field_removal_rate | 1.000 |
| whole_action_block_rate | 0.000 |
| executable_fieldwise_repair_success_rate | 1.000 |
| repair_frame_validity_rate | 1.000 |
| auto_executable_fields | 4 |
| partial_human_review_fields | 2 |

## Boundary

This is not an official AgentDojo reproduction and not a comparison against AgentDojo defenses. It is a bridge showing that task-environment-plus-injection cases can be represented as action fields and authority needs.

## Next Iteration

Move from bridge cases to either semi-real power traces or severity-weighted human-review burden.
