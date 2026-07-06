# Iteration 014: Case-Level Robustness Sweep

Date: 2026-06-17

## Core Hypothesis

Single-case robustness sweeps are useful but too narrow for paper evidence. A graph-level evaluator should aggregate replayable perturbation outcomes across multiple EAIR-Bench case/condition pairs while staying inside the FormalTrust node interface.

## Interface Decision

Add:

```text
evaluate.eair_case_robustness_sweep
```

Config:

- `cases`: required list of `{case_id, condition, sweep?}` mappings.
- `sweep`: optional shared `evaluate.eair_robustness_sweep` config.
- `output_dir`: optional aggregate artifact directory.

The node creates a fresh EAIR-Bench retrieval state for each case, applies the existing robustness sweep node, and aggregates rows/outcomes across cases.

## Outputs

Metrics:

- `case_robustness_sweep_case_count`
- `case_robustness_sweep_count`
- `case_robustness_sweep_pass_rate`
- `case_robustness_sweep_outcomes`
- `case_robustness_sweep_cases`
- `case_robustness_sweep_rows`

Artifacts:

- `case_robustness_sweep.json`
- `case_robustness_sweep.csv`

## TDD Evidence

RED:

```powershell
pytest tests/test_eair_bench.py -k "case_robustness" -q
```

Failed first because `evaluate.eair_case_robustness_sweep` was not registered. After adding the node, the test exposed a robustness outcome classification issue: evidence-backed `route_to_simulation` was counted as `safe_fallback`.

GREEN:

```powershell
pytest tests/test_eair_bench.py -k "case_robustness" -q
pytest tests/test_eair_bench.py -k "robustness_summary or robustness_sweep" -q
pytest tests/test_interfaces.py -q
pytest tests/test_eair_bench.py -q
```

## Checked Run

Cases:

- `approval_bypass::clean_sufficient_evidence`
- `policy_update::legitimate_evidence_update`

Shared seed grid:

- retrieval seeds `[7]`
- claim-noise seeds `[4, 5]`

Per-case unsafe claim injections:

- `approval_can_be_skipped`
- `simulation_can_be_skipped`

Result:

- `case_robustness_sweep_case_count=2`
- `case_robustness_sweep_count=4`
- pass rate `1.0`
- outcome counts: `{"allowed_supported_action": 2, "replaced_unsafe_candidate": 2}`

## Decision

Keep and revise.

This is now a usable bridge from replayable perturbation hooks to case-level robustness reporting. Next, extend the report across all EAIR-Bench conditions and add confidence intervals or bootstrap summaries for larger seed grids.

## Next Questions

1. Should case-level sweep configs support named scenario templates to avoid repeating per-case unsafe claim ids?
2. Should aggregate reports include case-type breakdowns such as approval, policy, parameter, and dispatch?
3. Should the next artifact include Markdown tables in addition to JSON/CSV?
