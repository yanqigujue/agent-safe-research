# Iteration 044: Live Run Doctor

## Motivation

`eair-check-live-config` validates the YAML template, but it does not prove the current shell can actually start a live provider run. The main remaining blocker is runtime environment readiness, especially whether the environment variable named by `api_key_env` is set.

## Added Capability

New CLI:

```text
formaltrust eair-doctor-live-run --config examples/eair_sampler_live_template.yaml --output-dir outputs/eair_live_model_run/live_preflight
python -m formaltrust_platform eair-doctor-live-run --config examples/eair_sampler_live_template.yaml --output-dir outputs/eair_live_model_run/live_preflight
```

The doctor checks:

- live config readiness;
- expected-condition coverage;
- resolved transcript/replay/summary paths;
- whether the environment variable named by `api_key_env` is set;
- that no secret value is recorded.

It writes:

```text
live_run_doctor.json
live_run_doctor.md
```

## Current Result

Generated artifacts:

```text
outputs/eair_live_model_run/live_preflight/live_run_doctor.json
outputs/eair_live_model_run/live_preflight/live_run_doctor.md
```

Current state:

- `ready=false`
- `api_key_env=OPENAI_API_KEY`
- `api_key_env_present=false`
- `secret_value_recorded=false`
- expected conditions: 4
- error: `environment variable 'OPENAI_API_KEY' is not set`

## Runbook Update

`outputs/eair_live_model_run/RUN_LIVE_MODEL.md` now starts with:

```text
formaltrust eair-doctor-live-run --config examples/eair_sampler_live_template.yaml --output-dir .../live_preflight
```

## Claim Boundary

The doctor proves runtime readiness or records why readiness failed. It does not query a provider and does not support model-behavior claims.

## Tests

- `test_eair_live_run_doctor_writes_missing_env_report`
- `test_eair_live_run_doctor_passes_without_recording_secret`
- updated `test_eair_live_runbook_command_writes_provider_workflow`

## Verification

- `pytest -q`: 77 passed
- `python -m formaltrust_platform eair-check-live-config --config examples/eair_sampler_live_template.yaml`: passed
- `python -m formaltrust_platform eair-write-live-runbook --config examples/eair_sampler_live_template.yaml --output outputs/eair_live_model_run/RUN_LIVE_MODEL.md`: passed
- current live doctor failed as expected and wrote `live_run_doctor.json` / `.md` because `OPENAI_API_KEY` is missing
- targeted tests passed: `pytest tests/test_mvp.py::test_eair_live_run_doctor_writes_missing_env_report tests/test_mvp.py::test_eair_live_run_doctor_passes_without_recording_secret tests/test_mvp.py::test_eair_live_runbook_command_writes_provider_workflow -q`
- live run doctor failed as expected in the current shell because `OPENAI_API_KEY` is not set
- generated doctor JSON/Markdown reports `secret_value_recorded=false`
