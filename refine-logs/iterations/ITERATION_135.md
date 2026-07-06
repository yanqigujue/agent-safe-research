# Iteration 135 - Numeric Audit With Table Binding

## Goal

Let the numeric claim audit consume the table-row evidence binding so README table numbers can be marked as supported by row-level artifacts.

## What Changed

- Updated `formaltrust_platform/experiments/power_ops_numeric_claim_audit.py`.
- Added `table_binding_paths` to `build_numeric_claim_audit`.
- Added CLI flag:
  - `--table-binding`
- Regenerated:
  - `docs/power_ops_action_invariance_numeric_claim_audit_2026-07-02.md`
  - `docs/power_ops_action_invariance_numeric_claim_audit_2026-07-02.json`
- Added test:
  - `test_power_ops_numeric_claim_audit_uses_table_binding_for_readme_tables`
- Updated:
  - `README_POWER_OPS_ACTION_INVARIANCE.md`
  - `task_plan.md`
  - `findings.md`
  - `progress.md`

## Audit Readback

| Item | Value |
|---|---:|
| table bindings | 1 |
| supported numeric mentions | 22 |
| supported_by_table_binding mentions | 184 |
| needs_evidence mentions | 43 |

## Before / After

| State | needs_evidence |
|---|---:|
| numeric audit without table binding | 218 |
| numeric audit with table binding | 43 |

## TDD Record

| Test | Red Signal | Green Result |
|---|---|---|
| `test_power_ops_numeric_claim_audit_uses_table_binding_for_readme_tables` | `build_numeric_claim_audit()` did not accept `table_binding_paths` | passed |

## Verification

| Check | Result |
|---|---|
| focused numeric audit table-binding test | 1 passed |
| `pytest tests/test_power_ops_action_invariance.py -q` | 31 passed |
| JSON parse / numeric audit with table binding check | passed |
| `pytest -q` | 231 passed |

## Keep / Revise / Reject

Keep. The numeric audit now separates directly supported metric readbacks, table-row supported values, and still-unresolved numeric mentions.

## Boundary

The remaining 43 `needs_evidence` mentions are not automatically wrong. They need classification before deciding whether to add evidence, rewrite text, or extend the parser.

## Next Iteration

Default next step:

```text
residual needs-evidence triage
```

The next round should classify the remaining mentions as context-only, needs-new-evidence, rewrite, or parser-extension candidates.
