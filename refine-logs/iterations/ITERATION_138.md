# Iteration 138 - Parser-Extension Cleanup

## Goal

Reduce residual numeric-audit `parser_extension` items by adding narrow artifact-backed parser rules for baseline lead-ins, baseline comparative sentences, and result-readback snippets.

## What Changed

- Updated `formaltrust_platform/experiments/power_ops_numeric_claim_audit.py`.
- Added `supported_by_context_rule` numeric mention status.
- Added context rules for:
  - baseline-grid `10-case` lead-in;
  - baseline comparative `fieldwise_repair` values;
  - expanded `18-case` result phrase;
  - performance-profile `suite_count=3` and `baseline_count=4` readbacks.
- Updated `formaltrust_platform/experiments/power_ops_residual_numeric_triage.py`.
- Classified structural list and future-work numbers as `context_only`.
- Regenerated:
  - `docs/power_ops_action_invariance_numeric_claim_audit_2026-07-02.md`
  - `docs/power_ops_action_invariance_numeric_claim_audit_2026-07-02.json`
  - `docs/power_ops_action_invariance_residual_numeric_triage_2026-07-02.md`
  - `docs/power_ops_action_invariance_residual_numeric_triage_2026-07-02.json`
- Added/updated test:
  - `test_power_ops_parser_extension_cleanup_supports_known_result_contexts`
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
| needs_evidence mentions | 42 |

## Residual Triage Readback

| Category | Count |
|---|---:|
| context_only | 42 |
| parser_extension | 0 |
| rewrite_needed | 0 |

## TDD Record

| Test | Red Signal | Green Result |
|---|---|---|
| `test_power_ops_parser_extension_cleanup_supports_known_result_contexts` | missing `supported_by_context_rule_numeric_claim_count` | passed |
| same test, tightened | remaining baseline/list parser-extension items | passed |

## Verification

| Check | Result |
|---|---|
| focused parser-extension cleanup test | 1 passed |
| `pytest tests/test_power_ops_action_invariance.py -q` | 34 passed |
| `pytest -q` | 234 passed |

## Keep / Revise / Reject

Keep. The audit now distinguishes artifact-backed context numbers from structural context-only numbers without globally marking unresolved numbers as supported.

## Boundary

`supported_by_context_rule` is intentionally narrow. It is not a general natural-language fact checker; it only binds known writing contexts to known generated artifacts.

## Next Iteration

Default next step:

```text
context-only exclusion from numeric claim count
```

The next round should stop counting list, round, and section numbers as unsupported numeric claims while preserving real unsupported result claims.
