# Iteration 018: Case Robustness Confidence Intervals

Date: 2026-06-17

## Goal

Add uncertainty metadata to case-level robustness reports before scaling from smoke checks to larger benchmark slices.

## Implementation

- Added Wilson 95% pass-rate interval helper.
- Extended `evaluate.eair_case_robustness_sweep` aggregate outputs:
  - metric `case_robustness_sweep_pass_rate_ci95`
  - JSON payload field `pass_rate_ci95`
- Extended per-case summaries with `pass_rate_ci95`.
- Extended per-case-type summaries with `pass_rate_ci95`.

## TDD Check

Extended existing case robustness tests.

Red failure:

- `case_robustness_sweep_pass_rate_ci95` was missing from metrics.

Green behavior:

- Aggregate seeded sweep: 4/4 pass, Wilson CI `[0.5101, 1.0]`.
- Per-case and per-case-type summaries: 2/2 pass, Wilson CI `[0.3424, 1.0]`.
- Selector smoke check: 2/2 pass, Wilson CI `[0.3424, 1.0]`.

## Interface Notes

- The node still returns only `evaluation`, `metrics`, and `artifacts`.
- Confidence intervals are structured metrics/artifact payload entries, not state schema changes.
