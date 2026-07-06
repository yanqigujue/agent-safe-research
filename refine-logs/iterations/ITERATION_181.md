# Iteration 181: Trace-Derived Authority Confusion

## Goal

Generate authority-confusion cases from otherwise legal power-agent traces, instead of relying only on hand-written adversarial rows.

## Hypothesis

If a row preserves field, operation, attributed source, and all boundary scopes but mutates only the semantic role requirement, a boundary-only checker will allow it while CapGuard will block it.

## Implementation

- Added `formaltrust_platform/experiments/power_ops_trace_authority_confusion.py`.
- Added focused TDD test:
  - `test_power_ops_trace_authority_confusion_generator_mutates_roles_only`
- Generated artifacts:
  - `examples/data/power_ops_trace_authority_confusion_rows.json`
  - `docs/power_ops_trace_authority_confusion_results_2026-07-02.md`
  - `docs/power_ops_trace_authority_confusion_results_2026-07-02.json`

## Readback

| Metric | Value |
|---|---:|
| source_case_count | 2 |
| generated_row_count | 10 |
| authority_confusion_row_count | 10 |
| boundary_preserved_row_count | 10 |
| mutated_required_role_only_count | 10 |
| capguard_legal_preservation_rate | 1.000 |
| capguard_confusion_block_rate | 1.000 |
| capguard_false_allow_rate | 0.000 |
| boundary_scope_only_false_allow_rate | 1.000 |

## Verification

```powershell
pytest tests/test_power_ops_action_invariance.py::test_power_ops_trace_authority_confusion_generator_mutates_roles_only -q
```

Result:

```text
1 passed
```

## Keep / Revise / Reject

Keep. This iteration strengthens the innovation claim by turning boundary-preserving role mismatch into a trace-derived test-generation mechanism. The next iteration should quantify overhead and audit compression so the method does not look like a safety-only system that ignores agent performance.
