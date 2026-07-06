# Iteration 157: Evidence-Bound Results Prose

## Status

complete

## Goal

Convert the §5 results outline into bounded prose while preserving result JSON paths, table-row refs, source claims, and fixture-only boundaries.

## TDD

Added `test_power_ops_evidence_bound_results_prose_keeps_table_and_source_binding`.

Observed red:

```text
ModuleNotFoundError: No module named 'formaltrust_platform.experiments.power_ops_evidence_bound_results_prose'
```

## Implementation

- Added `formaltrust_platform/experiments/power_ops_evidence_bound_results_prose.py`.
- Generated:
  - `docs/power_ops_action_invariance_evidence_bound_results_prose_2026-07-02.md`
  - `docs/power_ops_action_invariance_evidence_bound_results_prose_2026-07-02.json`
- The prose contains 7 bounded §5 paragraphs mapped to the results-outline slots.

## Readback

```text
results_prose: ready, paragraph_count=7, forbidden_hits=0
```

## Verification

```text
pytest tests/test_power_ops_action_invariance.py::test_power_ops_evidence_bound_results_prose_keeps_table_and_source_binding -q
1 passed
```

## Keep / Revise / Reject

keep

## Next

Iteration 158 should add the results-prose JSON artifact to the default paper-readiness forbidden-claim scan.
