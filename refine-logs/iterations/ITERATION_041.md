# Iteration 041: Reportable Live-Run Audit

## Motivation

After Iteration 040, the workflow had a runbook for collecting live provider transcripts. The remaining gap was evidentiary: complete coverage and verified manifests do not prove that a run is reportable as live-provider evidence. A dry-run artifact can pass coverage, so a separate admissibility gate is needed.

## Added Capability

New CLI:

```text
formaltrust eair-audit-reportable-run --manifest artifact_manifest.json --summary artifact_summary.json
python -m formaltrust_platform eair-audit-reportable-run --manifest artifact_manifest.json --summary artifact_summary.json
```

The audit checks:

- every manifest verifies against transcript SHA256 and replay outputs;
- the artifact summary is an `eair_artifact_summary`;
- summary rows include the provided manifests;
- coverage audit exists and is complete;
- every transcript has `sampling_mode: live`;
- dry-run, fixture, and mock-looking model names are rejected for live-reportable claims.

## Sampler Provenance

Sampler transcripts now include:

```text
sampling_mode: live | dry_run
```

Config-driven dry-run sampling writes `sampling_mode: dry_run`. Live provider sampling writes `sampling_mode: live`.

## Runbook Update

`outputs/eair_live_model_run/RUN_LIVE_MODEL.md` now includes a fifth step:

```text
formaltrust eair-audit-reportable-run --manifest ...artifact_manifest.json --summary ...artifact_summary.json
```

## Current Result

The complete dry-run fixture still passes manifest verification and complete-coverage summary, but it fails reportable-run audit as intended:

```text
live sampling_mode required: ... has dry_run
live model name required: ... uses complete-dry-run-openai-compatible
```

## Claim Boundary

This audit decides whether an artifact bundle is admissible as live-provider evidence. It does not claim the model is safe or unsafe; it only gates whether the run has enough provenance and coverage to be reported.

## Tests

- `test_eair_reportable_run_audit_accepts_live_transcript_with_complete_coverage`
- `test_eair_reportable_run_audit_rejects_dry_run_transcripts`
- updated `test_eair_live_runbook_command_writes_provider_workflow`

## Verification

- `pytest -q`: 73 passed
- `python -m formaltrust_platform eair-check-live-config --config examples/eair_sampler_live_template.yaml`: passed
- `python -m formaltrust_platform eair-write-live-runbook --config examples/eair_sampler_live_template.yaml --output outputs/eair_live_model_run/RUN_LIVE_MODEL.md`: passed
- `python -m formaltrust_platform eair-audit-reportable-run --manifest outputs/eair_sampler_complete_dry_run/replay/artifact_manifest.json --summary outputs/eair_sampler_complete_dry_run/summary/artifact_summary.json`: failed as expected for `sampling_mode: dry_run`
- targeted tests passed: `pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_provider_workflow tests/test_mvp.py::test_eair_reportable_run_audit_accepts_live_transcript_with_complete_coverage tests/test_mvp.py::test_eair_reportable_run_audit_rejects_dry_run_transcripts -q`
- regenerated runbook contains `eair-audit-reportable-run`
- dry-run audit fails as expected
