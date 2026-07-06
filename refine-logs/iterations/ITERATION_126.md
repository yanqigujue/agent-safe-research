# Iteration 126 - Skill-Driven Agent Security

## Goal

Extend the action-invariance direction beyond RAG by testing whether no-RAG skill manifests can be lifted into field-level capabilities without allowing skill authority escalation.

## What Changed

- Added `examples/data/power_ops_skill_authority_cases.jsonl`.
- Added `examples/power_ops_skill_authority_validation.yaml`.
- Added `docs/power_ops_skill_authority_model_2026-07-02.md`.
- Added reports:
  - `docs/power_ops_skill_authority_dataset_audit_2026-07-02.md`
  - `docs/power_ops_skill_authority_dataset_audit_2026-07-02.json`
  - `docs/power_ops_skill_authority_runtime_report_2026-07-02.md`
  - `docs/power_ops_skill_authority_runtime_report_2026-07-02.json`
  - `docs/power_ops_skill_authority_results_2026-07-02.md`
  - `docs/power_ops_skill_authority_results_2026-07-02.json`
- Added tests:
  - `test_power_ops_skill_authority_dataset_audit_reports_no_rag_skill_sources`
  - `test_power_ops_skill_authority_yaml_runs_through_afw_runtime_graph`
- Updated README, paper kernel, figure/table package, claim ledger, task plan, findings, and progress.

## Tested Skill Boundaries

| Skill | Authorized field | Blocked escalation |
|---|---|---|
| report-formatting skill | `risk_report` | `risk_level` |
| incident-summary skill | `answer` | `dispatch` |
| risk-assessment skill | `risk_level` | `switching_operation` |
| dispatch-prep skill | `dispatch_order` | `dispatch` |

## Runtime Result

| Suite | Cases | Passed | Source type | Whole-action block | Preservation | Unsafe removal | Repair validity |
|---|---:|---:|---|---:|---:|---:|---:|
| skill-authority | 4 | 4 | skill only | 0.000 | 1.000 | 1.000 | 1.000 |

## Keep / Revise / Reject

Keep. The result supports a narrow no-RAG skill-manifest authority claim, not a general skill-agent safety claim.

## Next Iteration

Start performance / over-conservatism evaluation:

```text
safety vs normal-action preservation + review burden + audit compression
```
