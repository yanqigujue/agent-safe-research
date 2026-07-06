# Iteration 161: Evidence-Bound Limitations Prose

## Status

complete

## Goal

Convert the §6 limitations outline into bounded prose while preserving excluded-claim binding, future-work actions, and source refs.

## TDD

Added `test_power_ops_evidence_bound_limitations_prose_keeps_excluded_claim_binding`.

Observed red:

```text
ModuleNotFoundError: No module named 'formaltrust_platform.experiments.power_ops_evidence_bound_limitations_prose'
```

## Implementation

- Added `formaltrust_platform/experiments/power_ops_evidence_bound_limitations_prose.py`.
- Generated:
  - `docs/power_ops_action_invariance_evidence_bound_limitations_prose_2026-07-02.md`
  - `docs/power_ops_action_invariance_evidence_bound_limitations_prose_2026-07-02.json`
- Markdown reports excluded-claim binding counts rather than copying forbidden phrases into paper prose.

## Readback

```text
limitations_prose: ready, paragraphs=6, forbidden_hits=0
```

## Verification

```text
pytest tests/test_power_ops_action_invariance.py::test_power_ops_evidence_bound_limitations_prose_keeps_excluded_claim_binding -q
1 passed
```

## Keep / Revise / Reject

keep

## Next

Iteration 162 should add the limitations-prose JSON artifact to the default paper-readiness forbidden-claim scan.
