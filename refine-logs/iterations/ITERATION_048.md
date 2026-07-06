# Iteration 048: WarrantGuard Full Baseline

## Motivation

Iteration 047 introduced `ActionWarrant` and `verify_action_warrant`, but the deterministic EAIR-Bench table still compared bare-action baselines. That left WarrantGuard as a method abstraction rather than an experimental condition.

## Change

This iteration adds `warrantguard_full`.

The baseline:

1. proposes a candidate `AgentAction`;
2. builds an `ActionWarrant`;
3. verifies the warrant;
4. blocks or replaces the action when the warrant fails;
5. otherwise applies the existing EAIR-Full verifier.

## Implementation

Modified:

- `formaltrust_platform/experiments/eair_bench.py`
- `tests/test_eair_bench.py`

Added:

- `docs/superpowers/specs/2026-06-21-warrantguard-full-baseline-design.md`
- `docs/superpowers/plans/2026-06-21-warrantguard-full-baseline.md`

New result fields:

- `warrant_passed`
- `warrant_error_count`
- `warrant_warning_count`
- `warrant_errors`
- `warrant_warnings`

New aggregate fields:

- `warrant_failure_rate`
- `mean_warrant_error_count`

## TDD Trace

Red test:

```text
pytest tests/test_eair_bench.py::test_warrantguard_full_baseline_records_warrant_diagnostics -q
FAILED: ValueError: Unknown baselines: ['warrantguard_full']
```

Green tests:

```text
pytest tests/test_eair_bench.py::test_warrantguard_full_baseline_records_warrant_diagnostics -q
1 passed

pytest tests/test_eair_bench.py::test_report_summarizes_closest_neighbor_baselines -q
1 passed

pytest tests/test_eair_bench.py -k "warrantguard or report_summarizes or summary_covers" -q
5 passed, 39 deselected
```

## Pilot Readback

Command:

```text
run_experiment(build_benchmark(), BASELINES, output_dir=Path("outputs/eair_bench_pilot"))
```

Result:

```text
results=270
baselines=18
warrantguard_full=True
```

`outputs/eair_bench_pilot/summary.json` reports:

```text
warrant_failure_rate=0.6
mean_warrant_error_count=0.8667
unsafe_decision_rate=0.0
clean_utility_retention=1.0
```

## Final Verification

```text
pytest -q
82 passed
```

Artifact readback:

```text
exists=outputs/eair_bench_pilot/summary.json
exists=outputs/eair_bench_pilot/baseline_summary.csv
exists=outputs/eair_bench_pilot/case_results.json
exists=outputs/eair_bench_pilot/report.md
total_results=270
warrant_failure_rate=0.6
mean_warrant_error_count=0.8667
unsafe_decision_rate=0.0
clean_utility_retention=1.0
```

## Claim Boundary

Supported:

- WarrantGuard can be evaluated as a deterministic EAIR-Bench baseline.
- The pilot can report proof-carrying action failures separately from generic unsupported-action or unsafe-action rates.

Not yet supported:

- Live LLMs can reliably emit valid warrants.
- WarrantGuard outperforms official prior systems.

## Next Step

Extend structured action replay from bare `AgentAction` JSON to `(action, warrant)` JSON.
