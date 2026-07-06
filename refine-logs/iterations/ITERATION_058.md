# Iteration 058: Live Prompt-Matrix Readiness

Date: 2026-06-21

## Motivation

Iteration 057 produced a deterministic prompt-protocol matrix. Before using a live provider, the preflight path should know the planned matrix scale and carry that metadata through readiness, doctor, and workflow-status artifacts.

## Implemented

- Live config readiness now reports:
  - `scenario_count`
  - `prompt_variants`
  - `prompt_variant_count`
  - `planned_transcript_count`
- `eair-check-live-config` prints the matrix counts.
- Live doctor JSON/Markdown carries the matrix counts.
- Live workflow status JSON carries the matrix counts.
- Added `examples/eair_prompt_protocol_matrix_live_template.yaml`.
- Generated:
  - `outputs/eair_prompt_protocol_matrix_live/live_preflight/`
  - `outputs/eair_prompt_protocol_matrix_live/workflow_status/`

## Verification

Red check:

```text
pytest tests/test_mvp.py::test_eair_live_config_checker_reports_prompt_protocol_matrix_plan -q
1 failed
```

Green checks so far:

```text
pytest tests/test_mvp.py::test_eair_live_config_checker_reports_prompt_protocol_matrix_plan -q
1 passed

pytest tests/test_mvp.py -k "live_config_checker or live_run_doctor or live_workflow_status" -q
7 passed, 25 deselected

pytest -q
89 passed
```

Template checker:

```text
python -m formaltrust_platform eair-check-live-config --config examples/eair_prompt_protocol_matrix_live_template.yaml
Live config ready
scenario_count: 3
prompt_variants: 3
planned_transcripts: 9
```

Current environment blocker:

```text
python -m formaltrust_platform eair-doctor-live-run --config examples/eair_prompt_protocol_matrix_live_template.yaml --output-dir outputs/eair_prompt_protocol_matrix_live/live_preflight
Live run doctor failed:
- environment variable 'OPENAI_API_KEY' is not set
```

Readback:

```text
ready=False
api_key_env=OPENAI_API_KEY
api_key_env_present=False
secret_value_recorded=False
scenario_count=3
prompt_variant_count=3
planned_transcript_count=9
prompt_variants=legacy_action_only,proof_carrying,proof_carrying_strict
workflow_status=blocked
blocked_stage=live_preflight
doctor_exists=True
status_exists=True
```

## Interpretation

The live prompt-matrix experiment is structurally ready, but the current shell cannot run it because `OPENAI_API_KEY` is missing. This is a correct blocker and does not support any live-model performance claim.
