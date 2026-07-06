# Iteration 059: Reportable Live Matrix Runbook

Date: 2026-06-21

## Motivation

Iteration 058 made the live prompt-protocol matrix preflight-aware. This iteration turns the live matrix into a reportable execution handoff by generating both human-readable and machine-readable runbook artifacts.

## Implemented

- `eair-write-live-runbook` now writes a JSON sidecar next to the Markdown runbook.
- The runbook payload includes:
  - scenario count;
  - prompt variants;
  - planned transcript count;
  - nine named commands from preflight through prompt adherence, protocol-legitimacy export, and paper-table export;
  - required artifacts, including `reportable_warrant_leaderboard.json`.
- Generated:
  - `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.md`
  - `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json`

## Verification

Red check:

```text
pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
1 failed
```

Green checks so far:

```text
pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
1 passed

pytest tests/test_mvp.py -k "live_runbook or reportable or live_config_checker or live_run_doctor or live_workflow_status" -q
14 passed, 19 deselected

pytest -q
91 passed
```

Runbook generation:

```text
python -m formaltrust_platform eair-write-live-runbook --config examples/eair_prompt_protocol_matrix_live_template.yaml --output outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.md
```

Readback:

```text
artifact_type=eair_live_runbook
scenario_count=3
prompt_variant_count=3
planned_transcript_count=9
command_count=9
has_prompt_adherence_command=True
has_protocol_legitimacy_command=True
required_has_leaderboard=True
claim_boundary=Runbook only records the planned live-provider workflow; it is not live-model evidence.
json_exists=True
md_exists=True
has_reportability=True
has_export=True
```

## Interpretation

The live prompt-matrix now has a reproducible, reportability-aware execution contract. It still does not support live-model behavior claims until provider transcripts are actually collected and the replay, coverage, reportability, and export gates pass.
