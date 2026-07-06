# Iteration 147: Evidence-Bound Method Outline

## Status

complete

## Goal

Generate an evidence-bound §3 method-section outline from the formal model, paper outline, and paper-ready claim ledger.

## TDD

Added `test_power_ops_evidence_bound_method_outline_uses_formal_model_and_ready_claims`.

Observed red:

```text
ModuleNotFoundError: No module named 'formaltrust_platform.experiments.power_ops_evidence_bound_method_outline'
```

Implemented `formaltrust_platform/experiments/power_ops_evidence_bound_method_outline.py`.

## Artifacts

- `formaltrust_platform/experiments/power_ops_evidence_bound_method_outline.py`
- `docs/power_ops_action_invariance_evidence_bound_method_outline_2026-07-02.md`
- `docs/power_ops_action_invariance_evidence_bound_method_outline_2026-07-02.json`
- Updated `README_POWER_OPS_ACTION_INVARIANCE.md`
- Updated `PAPER_PLAN.md`
- Updated `tests/test_power_ops_action_invariance.py`

## Result

```text
method_outline_status=ready
paper_section=§3 Formal Model and CapGuard
method_slots=6
forbidden_claim_hits=0
```

Slots:

- formal_objects
- coverage_rule
- minimal_witness_decision
- repair_invariance
- implementation_binding
- claim_boundary

## Verification

```text
pytest tests/test_power_ops_action_invariance.py::test_power_ops_evidence_bound_method_outline_uses_formal_model_and_ready_claims -q
1 passed
```

Final verification after Iteration 148:

```text
pytest tests/test_power_ops_action_invariance.py -q
43 passed

pytest -q
243 passed
```

## Keep / Revise / Reject

keep

## Next

The method outline is a new writing artifact, so paper readiness must scan it by default.
