# Iteration 137 - Lead-In Rewrite And Parser Refinement

## Goal

Remove the only `rewrite_needed` item found by residual numeric triage: the over-broad README lead-in for the Current Result table.

## What Changed

- Updated `README_POWER_OPS_ACTION_INVARIANCE.md`.
- Replaced the Current Result lead-in:
  - from: "On the 10-case curated power-ops suite"
  - to: "Rows below combine the current curated-suite summaries, trace replays, bridge fixtures, expanded cases, skill cases, and trace-import summaries"
- Regenerated:
  - `docs/power_ops_action_invariance_numeric_claim_audit_2026-07-02.md`
  - `docs/power_ops_action_invariance_numeric_claim_audit_2026-07-02.json`
  - `docs/power_ops_action_invariance_residual_numeric_triage_2026-07-02.md`
  - `docs/power_ops_action_invariance_residual_numeric_triage_2026-07-02.json`
- Added/updated test:
  - `test_power_ops_current_result_lead_in_no_longer_triggers_rewrite_triage`
- Updated:
  - `task_plan.md`
  - `findings.md`
  - `progress.md`

## Triage Readback

| Category | Count |
|---|---:|
| context_only | 32 |
| parser_extension | 17 |
| rewrite_needed | 0 |

## TDD Record

| Test | Red Signal | Green Result |
|---|---|---|
| `test_power_ops_current_result_lead_in_no_longer_triggers_rewrite_triage` | rewrite_needed was 1 | passed |

## Verification

| Check | Result |
|---|---|
| focused lead-in rewrite test | 1 passed |
| `pytest tests/test_power_ops_action_invariance.py -q` | 33 passed |
| `pytest -q` | 233 passed |

## Keep / Revise / Reject

Keep. The README no longer misstates the scope of the Current Result table.

## Boundary

The remaining residual numeric mentions are parser-extension or context-only cases. The next iteration should add targeted parser rules rather than globally marking them as supported.

## Next Iteration

Default next step:

```text
parser-extension cleanup
```

The next round should support baseline lead-in counts, baseline comparative sentence values, and result-readback snippets.
