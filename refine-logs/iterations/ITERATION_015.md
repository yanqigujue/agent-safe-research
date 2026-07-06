# Iteration 015: Case Robustness Markdown Report

Date: 2026-06-17

## Core Hypothesis

Case-level robustness sweeps should produce a paper-facing summary artifact, not only machine-readable JSON/CSV. The report should still be emitted through the evaluator node's `artifacts` patch so it remains compatible with FormalTrust graph execution.

## Interface Decision

Extend:

```text
evaluate.eair_case_robustness_sweep
```

When `output_dir` is configured, the node now writes:

- `case_robustness_sweep.json`
- `case_robustness_sweep.csv`
- `case_robustness_sweep_report.md`

No new top-level state fields were added.

## Report Contents

The Markdown report includes:

- aggregate case count, total runs, and pass rate;
- outcome distribution table;
- per-case summary table;
- per-run rows with case id, condition, outcome, gate decision, final decision, retrieval seed, and claim-noise seed.

## TDD Evidence

RED:

```powershell
pytest tests/test_eair_bench.py -k "case_robustness" -q
```

Failed because the node did not return `artifacts["case_robustness_sweep_report"]`.

GREEN:

```powershell
pytest tests/test_eair_bench.py -k "case_robustness" -q
pytest tests/test_eair_bench.py -k "case_robustness or robustness_sweep or robustness_summary" -q
pytest tests/test_eair_bench.py tests/test_interfaces.py -q
```

## Checked Report Assertions

The test verifies that the report contains:

- `# EAIR Case Robustness Sweep`
- `Case count: 2`
- `Total runs: 4`
- per-case rows for `approval_bypass` and `policy_update`
- outcome rows for `allowed_supported_action` and `replaced_unsafe_candidate`

## Decision

Keep.

This artifact makes the case-level sweep immediately usable for experiment logs and paper-table drafting. Next, expand the report across more case/condition pairs and add confidence intervals for larger seed grids.
