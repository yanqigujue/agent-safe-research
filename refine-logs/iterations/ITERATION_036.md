# Iteration 036: Expected-Condition Coverage Audit

## Motivation

The model-condition matrix shows per-cell outcomes, but it does not by itself prove that every model was evaluated on every planned condition. A model-backed experiment needs a coverage gate before any performance claim.

## Added Capability

`formaltrust eair-summarize-artifacts` now accepts repeatable expected condition keys:

```text
--expected-condition case_id::condition
```

The summary JSON includes:

```text
coverage
```

and the command writes:

```text
outputs/eair_artifact_summary/artifact_summary_coverage.csv
outputs/eair_artifact_summary/artifact_summary_coverage.md
```

Coverage tracks:

- expected conditions
- observed conditions
- unexpected conditions
- per-model covered conditions
- per-model missing conditions
- per-model coverage rate
- complete / incomplete status

## Current Result

Expected conditions:

```text
approval_bypass::clean_sufficient_evidence
approval_bypass::risk_report_downgrade_no_tool
parameter_setting::parameter_level_hijack
policy_update::legitimate_evidence_update
```

Coverage audit:

| model | coverage rate | missing conditions |
|---|---:|---|
| cli-dry-run-openai-compatible | 0.5000 | approval_bypass::clean_sufficient_evidence; parameter_setting::parameter_level_hijack |
| replay-fixture | 1.0000 | none |

## Claim Boundary

Coverage audit verifies whether replay artifacts cover planned model-condition cells. It is not a safety score and does not prove live-model behavior unless the underlying transcripts are provider-generated and verified.

## Tests

- `test_eair_artifact_summary_reports_expected_condition_coverage`

## Verification

- `pytest -q`: 66 passed
- `python -m formaltrust_platform eair-summarize-artifacts --manifest outputs/eair_replay_cli_pilot/artifact_manifest.json --manifest outputs/eair_sampler_cli_dry_run/replay/artifact_manifest.json --expected-condition approval_bypass::clean_sufficient_evidence --expected-condition approval_bypass::risk_report_downgrade_no_tool --expected-condition parameter_setting::parameter_level_hijack --expected-condition policy_update::legitimate_evidence_update --output-dir outputs/eair_artifact_summary`: passed
- `artifact_summary_coverage.csv` exists
- `artifact_summary_coverage.md` exists
- JSON readback confirms:
  - `complete=false`
  - `cli-dry-run-openai-compatible` coverage rate `0.5`
  - missing conditions: `approval_bypass::clean_sufficient_evidence`, `parameter_setting::parameter_level_hijack`
  - `replay-fixture` coverage rate `1.0`
