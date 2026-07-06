# Iteration 127 - Performance / Over-Conservatism Evaluation

## Goal

Quantify whether strict supervision preserves normal authorized behavior rather than only reporting unsafe-field blocking.

## What Changed

- Added `formaltrust_platform/experiments/power_ops_action_invariance_perf.py`.
- Added `docs/power_ops_action_invariance_performance_2026-07-02.md`.
- Added `docs/power_ops_action_invariance_performance_2026-07-02.json`.
- Added test:
  - `test_power_ops_performance_profile_compares_safety_and_normal_behavior`
- Updated README, paper kernel, figure/table package, claim ledger, task plan, findings, and progress.

## Profile Dimensions

| Dimension | Meaning |
|---|---|
| normal preservation | authorized final-field preservation |
| safety removal | unauthorized final-field removal |
| whole-action block | whether strict intervention collapses the entire action |
| review fields/case | local human-review burden |
| latency proxy | runtime field checks, not wall-clock latency |
| audit compression | mean minimal-witness compression ratio |

## Baseline Takeaway

| Baseline | Normal preservation | Safety removal | Whole-action block | False allow |
|---|---:|---:|---:|---:|
| strict-block | 0.000 | 1.000 | 1.000 | 0.000 |
| provenance-only | 1.000 | 0.000 | 0.000 | 1.000 |
| fieldwise-repair | 1.000 | 1.000 | 0.000 | 0.000 |

## Keep / Revise / Reject

Keep. The profile directly answers the over-conservatism question at artifact level, while preserving the boundary that latency is only a field-check proxy.

## Next Iteration

Start realistic trace import path:

```text
trace import contract + fixture + malformed/missing/duplicate/expired behavior
```
