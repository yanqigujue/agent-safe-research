# Iteration 064: Protocol-Legitimacy Alignment Gate

## Goal

Prevent reportable paper export from mixing a reportable summary with protocol-legitimacy rows from another model, prompt variant, or condition.

## Implemented

- Added `_protocol_legitimacy_summary_alignment_errors`.
- If `by_model_prompt_condition` exists, protocol rows must match `(model, prompt_variant, condition)`.
- Otherwise protocol rows must match `(model, condition)`.
- On mismatch, `eair-export-reportable-results` writes `reportable_results_export_blocked.json/md` and exits.

## Red-Green

Red check:

```text
pytest tests/test_mvp.py::test_eair_export_reportable_results_rejects_mismatched_protocol_legitimacy_rows -q
failed because mismatched protocol rows were accepted
```

Green check:

```text
pytest tests/test_mvp.py::test_eair_export_reportable_results_rejects_mismatched_protocol_legitimacy_rows -q
1 passed
```

## Readback

```text
protocol_legitimacy_row_count=1
protocol_rows=[('provider-live-warrant-model', 'default', 'policy_update::near_duplicate_single_source_policy_support')]
```

## Boundary

This validates artifact alignment only. It does not replace WarrantGuard's warrant-quality checks.

## Verification

```text
pytest tests/test_mvp.py::test_eair_export_reportable_results_rejects_mismatched_protocol_legitimacy_rows -q
1 passed

pytest tests/test_mvp.py::test_eair_export_reportable_results_rejects_mismatched_protocol_legitimacy_rows tests/test_mvp.py::test_eair_export_reportable_results_includes_warrant_taxonomy_columns tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
3 passed

pytest tests/test_mvp.py -k "reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence or live_runbook" -q
10 passed, 26 deselected

pytest -q
93 passed
```

Final readback:

```text
export_artifact_type=eair_reportable_results_export
reportable=True
protocol_rows=[('provider-live-warrant-model', 'default', 'policy_update::near_duplicate_single_source_policy_support')]
reportable_protocol_table_exists=True
```
