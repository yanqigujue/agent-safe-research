# Iteration 139 - Context-Only Exclusion From Numeric Claim Count

## Goal

Stop counting structural numbers, such as iteration rows and list indices, as unsupported numeric claims while preserving the failure path for real unsupported result numbers.

## What Changed

- Updated `formaltrust_platform/experiments/power_ops_numeric_claim_audit.py`.
- Added `ignored_context_number` numeric mention status.
- Added `ignored_context_number_count` to the JSON and Markdown audit summaries.
- Kept `unsupported_numeric_claim_count` limited to true `needs_evidence` mentions.
- Preserved supported-result precedence:
  - `supported`
  - `supported_by_table_binding`
  - `supported_by_context_rule`
  - `ignored_context_number`
  - `needs_evidence`
- Regenerated:
  - `docs/power_ops_action_invariance_numeric_claim_audit_2026-07-02.md`
  - `docs/power_ops_action_invariance_numeric_claim_audit_2026-07-02.json`
  - `docs/power_ops_action_invariance_residual_numeric_triage_2026-07-02.md`
  - `docs/power_ops_action_invariance_residual_numeric_triage_2026-07-02.json`
- Added/updated test:
  - `test_power_ops_numeric_claim_audit_excludes_context_only_numbers`
- Updated:
  - `README_POWER_OPS_ACTION_INVARIANCE.md`
  - `task_plan.md`
  - `findings.md`
  - `progress.md`

## Numeric Audit Readback

| Item | Count |
|---|---:|
| supported numeric mentions | 22 |
| supported_by_table_binding mentions | 184 |
| supported_by_context_rule mentions | 11 |
| ignored_context_number | 50 |
| unsupported_numeric_claim_count | 0 |

## Residual Triage Readback

| Item | Count |
|---|---:|
| total_needs_evidence_mentions | 0 |

## TDD Record

| Test | Red Signal | Green Result |
|---|---|---|
| `test_power_ops_numeric_claim_audit_excludes_context_only_numbers` | missing `ignored_context_number_count` | passed |
| same test, tightened | `source_type_coverage=1.000` was incorrectly ignored near "Next Experiments" | passed |

## Verification

| Check | Result |
|---|---|
| focused context-only exclusion test | 1 passed |
| `pytest tests/test_power_ops_action_invariance.py -q` | 35 passed |
| `pytest -q` | 235 passed |

## Keep / Revise / Reject

Keep. The audit no longer reports structural writing numbers as unsupported claims, and the synthetic unsupported result number remains `needs_evidence`.

## Boundary

`ignored_context_number` is not evidence support. It only says the number is outside the result-claim audit scope.

## Next Iteration

Default next step:

```text
paper-claim readiness gate
```

The next round should combine numeric audit, table evidence binding, residual triage, and forbidden-claim scan into a single pass/fail evidence-readiness artifact.
