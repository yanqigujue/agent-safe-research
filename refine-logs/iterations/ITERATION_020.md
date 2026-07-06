# Iteration 020: Case Robustness Coverage Gate

Date: 2026-06-17

## Goal

Prevent small robustness smoke checks from being interpreted as broad multi-case-type evidence when the graph declares stricter coverage requirements.

## Implementation

- Extended built-in evaluator node `evaluate.eair_case_robustness_sweep`.
- Added optional config `coverage`.
- Supported coverage fields:
  - `min_cases`
  - `min_case_types`
  - `required_case_types`
- Added metric `case_robustness_sweep_coverage`.
- Added JSON payload field `coverage`.
- Added a Markdown report `Coverage` section.
- If action evaluation passes but coverage fails, the node returns:
  - `evaluation.passed=False`
  - `evaluation.label="case_robustness_sweep_coverage_failure"`
  - action-evaluation and coverage reasons in `evaluation.reasons`

## TDD Check

Added `test_case_robustness_sweep_coverage_gate_fails_undercovered_slices`.

Red failure:

- Graph assembly rejected `coverage` as an unknown config field.

Green behavior:

- Selector over approval/policy samples produces 2 cases and 2 case types.
- Action-evaluator pass rate remains `1.0`.
- Coverage requirement asks for 3 cases, 3 case types, and `parameter`.
- Node records missing `parameter`, returns no runtime errors, and fails evaluation with coverage reasons.
- JSON and Markdown artifacts expose the same coverage details.

## Interface Notes

- The node still reads `FormalTrustState` and config only.
- The node still returns only `evaluation`, `metrics`, and `artifacts`.
- No state schema changes were needed.
