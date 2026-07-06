# Iteration 149: Evidence-Bound Method Prose

## Status

complete

## Goal

Convert the evidence-bound method outline into bounded §3 method prose while preserving formal-model references, paper-ready source claims, and explicit claim boundaries.

## TDD

Added `test_power_ops_evidence_bound_method_prose_keeps_formal_refs_and_claims`.

Observed red:

```text
ModuleNotFoundError: No module named 'formaltrust_platform.experiments.power_ops_evidence_bound_method_prose'
```

## Implementation

- Added `formaltrust_platform/experiments/power_ops_evidence_bound_method_prose.py`.
- Generated:
  - `docs/power_ops_action_invariance_evidence_bound_method_prose_2026-07-02.md`
  - `docs/power_ops_action_invariance_evidence_bound_method_prose_2026-07-02.json`
- The prose contains 6 paragraphs:
  - `formal_objects`
  - `coverage_rule`
  - `minimal_witness_decision`
  - `repair_invariance`
  - `implementation_binding`
  - `claim_boundary`

## Readback

```text
method_prose: ready, paragraph_count=6, forbidden_hits=0
```

## Verification

```text
pytest tests/test_power_ops_action_invariance.py::test_power_ops_evidence_bound_method_prose_keeps_formal_refs_and_claims -q
1 passed
```

## Keep / Revise / Reject

keep

## Next

Iteration 150 should add the method-prose JSON artifact to the default paper-readiness forbidden-claim scan.
