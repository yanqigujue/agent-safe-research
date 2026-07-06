# Reportable Live Matrix Runbook Plan

Date: 2026-06-21

## Checklist

- [x] Add failing test for a prompt-matrix runbook JSON sidecar.
- [x] Verify the test fails before implementation.
- [x] Add structured runbook payload generation.
- [x] Write JSON sidecar next to the Markdown runbook.
- [x] Include prompt matrix scale and prompt variant names.
- [x] Include reportability audit and paper-table export commands.
- [x] Include required reportable WarrantGuard artifacts.
- [x] Generate live prompt-matrix runbook artifacts.
- [x] Run full pytest before final reporting.

## Commands

```text
pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
pytest tests/test_mvp.py -k "live_runbook or reportable or live_config_checker or live_run_doctor or live_workflow_status" -q
python -m formaltrust_platform eair-write-live-runbook --config examples/eair_prompt_protocol_matrix_live_template.yaml --output outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.md
pytest -q
```

## Final Verification

```text
91 passed
json_exists=True
md_exists=True
artifact_type=eair_live_runbook
planned_transcript_count=9
command_count=9
has_prompt_adherence_command=True
has_protocol_legitimacy_command=True
has_reportability=True
has_export=True
has_required_leaderboard=True
```
