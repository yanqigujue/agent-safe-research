# Iteration 037: Require Complete Coverage Gate

## Motivation

Coverage audit reports missing model-condition cells, but a formal experiment needs a gate that can fail the run before incomplete coverage is copied into paper tables.

## Added Capability

`formaltrust eair-summarize-artifacts` now supports:

```text
--require-complete-coverage
```

When coverage is incomplete:

- summary artifacts are still written;
- the CLI exits with an error;
- the error message names the model and missing conditions.

## Current Gate Check

Command shape:

```text
python -m formaltrust_platform eair-summarize-artifacts \
  --manifest outputs/eair_replay_cli_pilot/artifact_manifest.json \
  --manifest outputs/eair_sampler_cli_dry_run/replay/artifact_manifest.json \
  --expected-condition approval_bypass::clean_sufficient_evidence \
  --expected-condition approval_bypass::risk_report_downgrade_no_tool \
  --expected-condition parameter_setting::parameter_level_hijack \
  --expected-condition policy_update::legitimate_evidence_update \
  --require-complete-coverage \
  --output-dir outputs/eair_artifact_summary
```

Observed expected failure:

```text
coverage incomplete: cli-dry-run-openai-compatible: missing=['approval_bypass::clean_sufficient_evidence', 'parameter_setting::parameter_level_hijack']
```

The failure is correct because the dry-run sampler covers only two of four expected conditions.

## Claim Boundary

This is an experiment-validity gate. It prevents incomplete model-condition coverage from being reported as comparable model performance. It is not a safety score and does not prove live-model behavior.

## Tests

- `test_eair_artifact_summary_require_complete_coverage_fails_with_audit`

## Verification

- `pytest -q`: 67 passed
- normal summary command with expected conditions: passed
- summary command with `--require-complete-coverage`: failed as expected on current incomplete dry-run coverage
- failure message named `cli-dry-run-openai-compatible` and missing:
  - `approval_bypass::clean_sufficient_evidence`
  - `parameter_setting::parameter_level_hijack`
- coverage artifacts still existed after the expected failure
- JSON readback confirmed `complete=false` and `replay-fixture` coverage rate `1.0`
