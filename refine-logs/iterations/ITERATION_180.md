# Iteration 180 - Normal-Behavior Stress Test

## Goal

Measure whether strict field-level supervision preserves normal behavior when all action fields are already authorized.

## What Changed

- Added `examples/data/power_ops_normal_behavior_stress_fixture.json` with 4 fully authorized power-operation traces.
- Added `examples/power_ops_normal_behavior_stress_validation.yaml`.
- Added `formaltrust_platform/experiments/power_ops_normal_behavior_stress.py`.
- Generated:
  - `docs/power_ops_normal_behavior_stress_results_2026-07-02.md/json`
  - `docs/power_ops_normal_behavior_stress_runtime_report_2026-07-02.md/json`
- Updated README, PAPER_PLAN, table evidence binding, numeric audit, residual triage, paper readiness, claim ledger readiness, and derived paper artifacts.

## Readback

| Artifact | Result |
|---|---|
| Benchmark cases | total_cases=4, passed_cases=4 |
| Fully authorized cases | 4 |
| Authorized fields | 16 |
| Preserved authorized fields | 16 |
| False-block fields | 0 |
| False intervention field rate | 0.000 |
| Whole-action intervention rate | 0.000 |
| Final-action mutation cases | 0 |
| Mean repair overhead fields | 0.000 |
| Table evidence binding | fully_supported_row_count=20, unsupported_row_count=0 |
| Numeric audit | unsupported_numeric_claim_count=0 |
| Claim readiness | PASS |

## Verification

| Command | Result |
|---|---|
| `pytest tests/test_power_ops_action_invariance.py::test_power_ops_normal_behavior_stress_preserves_fully_authorized_actions -q` | failed first on missing module, then passed |
| focused Iteration 71 regression | 5 passed |
| `pytest tests/test_power_ops_action_invariance.py -q` | 69 passed |
| `pytest -q` | 269 passed |

## Boundary

This is fixture-level evidence. It supports the claim that the current strict-supervision path does not over-intervene on these curated fully authorized traces. It does not claim production telemetry, real operator workload reduction, wall-clock latency, or official benchmark superiority.

## Next

Iteration 181 should implement a trace-derived authority-confusion generator: start from legal trace rows, mutate required roles while preserving fields and scopes, and verify that CapGuard blocks role-confusion rows without blocking the original legal rows.
