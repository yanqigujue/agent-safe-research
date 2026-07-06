# Iteration 042: Persisted Reportability Audit Artifacts

## Motivation

Iteration 041 introduced the reportable live-run audit, but the audit result only lived in CLI output. For a paper artifact, pass/fail status and reasons must be archived as files, including failure cases.

## Added Capability

`eair-audit-reportable-run` now accepts:

```text
--output-dir reportability_dir
```

When provided, the command writes:

```text
reportable_run_audit.json
reportable_run_audit.md
```

The audit files are written for both pass and fail outcomes. Failure still exits nonzero, but the reasons are preserved.

## Runbook Update

The live runbook now records:

```text
formaltrust eair-audit-reportable-run --manifest ...artifact_manifest.json --summary ...artifact_summary.json --output-dir .../reportability
```

## Current Dry-Run Artifact

Generated files:

```text
outputs/eair_sampler_complete_dry_run/reportability/reportable_run_audit.json
outputs/eair_sampler_complete_dry_run/reportability/reportable_run_audit.md
```

Current result:

- `coverage_complete`: true
- `reportable`: false
- `sampling_modes`: `{"dry_run": 4}`
- rejection reason: live `sampling_mode` is required and dry-run model names are not reportable as live-provider evidence.

## Claim Boundary

Persisted reportability audits prove artifact admissibility or rejection reasons. They do not prove model safety.

## Tests

- updated `test_eair_reportable_run_audit_accepts_live_transcript_with_complete_coverage`
- updated `test_eair_reportable_run_audit_rejects_dry_run_transcripts`
- updated `test_eair_live_runbook_command_writes_provider_workflow`

## Verification

- `pytest -q`: 73 passed
- `python -m formaltrust_platform eair-check-live-config --config examples/eair_sampler_live_template.yaml`: passed
- `python -m formaltrust_platform eair-write-live-runbook --config examples/eair_sampler_live_template.yaml --output outputs/eair_live_model_run/RUN_LIVE_MODEL.md`: passed
- dry-run reportability command failed as expected while writing `reportable_run_audit.json` and `.md`
- targeted tests passed: `pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_provider_workflow tests/test_mvp.py::test_eair_reportable_run_audit_accepts_live_transcript_with_complete_coverage tests/test_mvp.py::test_eair_reportable_run_audit_rejects_dry_run_transcripts -q`
- regenerated live runbook includes `--output-dir .../reportability`
- dry-run reportability audit writes JSON/Markdown failure artifacts
