# Iteration 045: Live Workflow Status Checkpoint

## Motivation

The live run doctor reports the immediate runtime blocker, but after the pipeline grows to multiple steps it is useful to have a single checkpoint artifact that tells whether the whole live-provider workflow is ready, blocked, or complete.

## Added Capability

New CLI:

```text
formaltrust eair-live-workflow-status --config examples/eair_sampler_live_template.yaml --output-dir outputs/eair_live_model_run/workflow_status
python -m formaltrust_platform eair-live-workflow-status --config examples/eair_sampler_live_template.yaml --output-dir outputs/eair_live_model_run/workflow_status
```

The status command checks:

- live preflight doctor status;
- transcript JSONL presence;
- replay `artifact_manifest.json` presence;
- coverage summary presence and completeness;
- reportability audit presence and `reportable=true`;
- paper-table export presence.

It writes:

```text
live_workflow_status.json
live_workflow_status.md
```

## Current Result

Generated artifacts:

```text
outputs/eair_live_model_run/workflow_status/live_workflow_status.json
outputs/eair_live_model_run/workflow_status/live_workflow_status.md
```

Current state:

- `overall_status=blocked`
- `blocked_stage=live_preflight`
- `api_key_env=OPENAI_API_KEY`
- `api_key_env_present=false`
- `secret_value_recorded=false`

## Claim Boundary

Workflow status is an operational checkpoint. It does not query a provider and does not support model-behavior claims.

## Tests

- `test_eair_live_workflow_status_reports_preflight_blocker`
- `test_eair_live_workflow_status_passes_complete_live_bundle`

## Verification

- targeted tests passed: `pytest tests/test_mvp.py::test_eair_live_workflow_status_reports_preflight_blocker tests/test_mvp.py::test_eair_live_workflow_status_passes_complete_live_bundle -q`
- current workflow status command blocks as expected at `live_preflight`
- status JSON/Markdown were generated and read back
- `pytest -q` passed: 79 passed
- `python -m formaltrust_platform eair-check-live-config --config examples/eair_sampler_live_template.yaml` passed
- `python -m formaltrust_platform eair-write-live-runbook --config examples/eair_sampler_live_template.yaml --output outputs/eair_live_model_run/RUN_LIVE_MODEL.md` passed
- workflow status artifact readback confirms `overall_status=blocked`, `blocked_stage=live_preflight`, `api_key_env=OPENAI_API_KEY`, `api_key_env_present=false`, and `secret_value_recorded=false`
