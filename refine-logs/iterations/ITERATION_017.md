# Iteration 017: Case Selector Robustness Sweep

Date: 2026-06-17

## Goal

Make the case-level robustness sweep scale from hand-written case lists to benchmark slices while preserving the FormalTrust node contract.

## Implementation

- Extended built-in node `evaluate.eair_case_robustness_sweep`.
- Added optional config `case_selector`.
- Made explicit `cases` optional, with explicit `cases` still taking priority.
- Selector filters are resolved against `build_benchmark()`:
  - `case_ids`
  - `conditions`
  - `case_types`
  - `limit`
- Added metric `case_robustness_sweep_selector`.
- Added JSON payload field `selector`.

## TDD Check

Added `test_case_robustness_sweep_can_select_cases_from_benchmark`.

Red failure:

- Graph assembly rejected `case_selector` as unknown.
- Graph assembly still required explicit `cases`.

Green behavior:

- Selector over `approval`/`policy` case types and two conditions resolves to:
  - `approval_bypass::clean_sufficient_evidence`
  - `policy_update::legitimate_evidence_update`
- Shared `selected_topk` run with `retrieval.top_k=2` produces 2 rows.
- Pass rate: `1.0`.
- Outcome counts: `{"allowed_supported_action": 2}`.

## Interface Notes

- The node still reads `FormalTrustState` and config only.
- The node still returns only top-level state patch fields: `evaluation`, `metrics`, and `artifacts`.
- No `FormalTrustState` schema changes were needed.
