# Iteration 125 - Action-Invariance Metamorphic Tests

## Goal

Move beyond hand-written expanded cases by generating deterministic authority-confusion mutations and checking whether fieldwise repair preserves authorized fields.

## What Changed

- Added `formaltrust_platform/experiments/power_ops_action_invariance_metamorphic.py`.
- Added `examples/data/power_ops_action_invariance_metamorphic_cases.jsonl`.
- Added `examples/power_ops_action_invariance_metamorphic_validation.yaml`.
- Added tests:
  - `test_power_ops_metamorphic_generator_covers_required_mutations`
  - `test_power_ops_metamorphic_suite_runs_and_preserves_authorized_fields`
- Added reports:
  - `docs/power_ops_action_invariance_metamorphic_runtime_report_2026-07-02.md`
  - `docs/power_ops_action_invariance_metamorphic_runtime_report_2026-07-02.json`
  - `docs/power_ops_action_invariance_metamorphic_tests_2026-07-02.md`
  - `docs/power_ops_action_invariance_metamorphic_tests_2026-07-02.json`
- Updated README, paper kernel, figure/table package, claim ledger, task plan, findings, and progress.

## TDD

The new focused tests first failed because the metamorphic module did not exist:

```text
ModuleNotFoundError: formaltrust_platform.experiments.power_ops_action_invariance_metamorphic
```

After adding the module and artifacts:

```text
2 passed
```

## Mutation Coverage

| Mutation | Expected unsafe-field behavior |
|---|---|
| role_mismatch | block |
| scope_mismatch | block |
| counter_authority | abstain |
| expired_approval | block |

## Runtime Result

| Suite | Cases | Passed | Whole-action block | Preservation | Unsafe removal | Repair validity |
|---|---:|---:|---:|---:|---:|---:|
| metamorphic | 4 | 4 | 0.000 | 1.000 | 1.000 | 1.000 |

## Keep / Revise / Reject

Keep. The result directly supports the action-invariance property under systematic authority-confusion mutations.

## Next Iteration

Start skill-driven agent security:

```text
skill manifest -> Cap(x), action field -> Need(s,f), verify formatting/summary skills cannot become risk or dispatch authority
```
