# Iteration 016: Case-Type Robustness Aggregation

Date: 2026-06-17

## Core Hypothesis

Case-level robustness reports should support benchmark-category analysis. Individual case rows are useful for debugging, but paper tables and failure-mode discussions need grouped summaries by `case_type`.

## Interface Decision

Extend:

```text
evaluate.eair_case_robustness_sweep
```

without adding any new top-level `FormalTrustState` fields.

New/extended outputs:

- `case_robustness_sweep_rows[*].case_type`
- `case_robustness_sweep_cases[*].case_type`
- `case_robustness_sweep_case_types`
- JSON payload field `case_types`
- CSV column `case_type`
- Markdown section `## Case-Type Summary`

## TDD Evidence

RED:

```powershell
pytest tests/test_eair_bench.py -k "case_robustness" -q
```

Failed because rows did not include `case_type`.

GREEN:

```powershell
pytest tests/test_eair_bench.py -k "case_robustness" -q
pytest tests/test_eair_bench.py -k "case_robustness or robustness_sweep or robustness_summary" -q
pytest tests/test_eair_bench.py tests/test_interfaces.py -q
```

## Checked Summaries

The two-case seeded sweep now verifies:

- `approval_bypass::clean_sufficient_evidence` belongs to `approval`.
- `policy_update::legitimate_evidence_update` belongs to `policy`.
- each case type has `n=2`, pass rate `1.0`, and outcomes `{"allowed_supported_action": 1, "replaced_unsafe_candidate": 1}`.

## Decision

Keep.

This prepares case-level robustness reporting for all EAIR-Bench categories. The next iteration should expand from two cases to a reusable all-condition sweep config or add confidence interval summaries for larger seed grids.
