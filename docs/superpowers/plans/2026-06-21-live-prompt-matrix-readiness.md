# Live Prompt-Matrix Readiness Plan

Date: 2026-06-21

## Checklist

- [x] Add a failing test for prompt-variant-aware live readiness.
- [x] Verify the test fails before implementation.
- [x] Add matrix scale fields to live config readiness.
- [x] Add matrix scale fields to live doctor JSON/Markdown.
- [x] Add matrix scale fields to live workflow status JSON.
- [x] Print scenario, prompt-variant, and planned transcript counts from `eair-check-live-config`.
- [x] Add live prompt-protocol matrix template.
- [x] Run static live config checker on the template.
- [x] Run doctor/workflow status and record the missing-key blocker.
- [x] Run full pytest before final reporting.

## Commands

```text
pytest tests/test_mvp.py::test_eair_live_config_checker_reports_prompt_protocol_matrix_plan -q
pytest tests/test_mvp.py -k "live_config_checker or live_run_doctor or live_workflow_status" -q
python -m formaltrust_platform eair-check-live-config --config examples/eair_prompt_protocol_matrix_live_template.yaml
python -m formaltrust_platform eair-doctor-live-run --config examples/eair_prompt_protocol_matrix_live_template.yaml --output-dir outputs/eair_prompt_protocol_matrix_live/live_preflight
python -m formaltrust_platform eair-live-workflow-status --config examples/eair_prompt_protocol_matrix_live_template.yaml --output-dir outputs/eair_prompt_protocol_matrix_live/workflow_status
pytest -q
```

## Final Verification

```text
89 passed
doctor_exists=True
status_exists=True
doctor_ready=False
doctor_secret_value_recorded=False
doctor_planned_transcript_count=9
status_overall=blocked
status_blocked_stage=live_preflight
status_planned_transcript_count=9
```
