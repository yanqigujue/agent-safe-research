# Iteration 136 - Residual Needs-Evidence Triage

## Goal

Classify the remaining `needs_evidence` numeric mentions after numeric audit consumed table-row evidence binding.

## What Changed

- Added `formaltrust_platform/experiments/power_ops_residual_numeric_triage.py`.
- Generated:
  - `docs/power_ops_action_invariance_residual_numeric_triage_2026-07-02.md`
  - `docs/power_ops_action_invariance_residual_numeric_triage_2026-07-02.json`
- Added test:
  - `test_power_ops_residual_numeric_triage_classifies_remaining_mentions`
- Updated:
  - `README_POWER_OPS_ACTION_INVARIANCE.md`
  - `task_plan.md`
  - `findings.md`
  - `progress.md`

## Triage Readback

| Category | Count |
|---|---:|
| context_only | 25 |
| parser_extension | 17 |
| rewrite_needed | 1 |

## Key Finding

The one `rewrite_needed` item is the README lead-in for the Current Result table. It still says the table is "On the 10-case curated power-ops suite", but the table now mixes many result suites and import fixtures.

## TDD Record

| Test | Red Signal | Green Result |
|---|---|---|
| `test_power_ops_residual_numeric_triage_classifies_remaining_mentions` | missing `power_ops_residual_numeric_triage` module | passed |

## Verification

| Check | Result |
|---|---|
| focused residual triage test | 1 passed |
| `pytest tests/test_power_ops_action_invariance.py -q` | 32 passed |
| JSON parse / triage consistency check | passed |
| `pytest -q` | 232 passed |

## Keep / Revise / Reject

Keep. The audit now distinguishes non-claim context numbers from parser gaps and text that should be rewritten.

## Boundary

The triage is rule-based. It identifies next actions but does not itself rewrite README or extend numeric audit parser rules.

## Next Iteration

Default next step:

```text
lead-in rewrite and parser refinement
```

The next round should rewrite the over-broad Current Result table lead-in, rerun the audits, and check that `rewrite_needed` drops to zero.
