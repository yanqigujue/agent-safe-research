# Iteration 065: Protocol Metric Consistency Gate

## Goal

Prevent same-key but metric-tampered protocol-legitimacy rows from entering reportable paper export.

## Implemented

- Extended `_protocol_legitimacy_summary_alignment_errors`.
- Added `_protocol_legitimacy_metric_mismatch_errors`.
- Compared selected transcript counts, WarrantGuard rates, quality scores, and JSON count fields against the matching summary metrics.

## Red-Green

Red check:

```text
pytest tests/test_mvp.py::test_eair_export_reportable_results_rejects_protocol_metric_mismatch -q
failed because same-key metric-tampered rows were accepted
```

Green check:

```text
pytest tests/test_mvp.py::test_eair_export_reportable_results_rejects_protocol_metric_mismatch -q
1 passed
```

## Readback

```text
protocol_row=provider-live-warrant-model/default/policy_update::near_duplicate_single_source_policy_support
warrant_quality_score=0.0
warrant_error_category_counts_json={"decision_support": 1}
```

## Boundary

This validates exported metric consistency with the summary artifact. It does not recompute metrics from raw transcripts.

## Verification

```text
pytest tests/test_mvp.py::test_eair_export_reportable_results_rejects_protocol_metric_mismatch -q
1 passed

pytest tests/test_mvp.py::test_eair_export_reportable_results_includes_warrant_taxonomy_columns tests/test_mvp.py::test_eair_export_reportable_results_rejects_mismatched_protocol_legitimacy_rows tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
3 passed

pytest tests/test_mvp.py -k "reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence or live_runbook" -q
11 passed, 26 deselected

pytest -q
94 passed
```

Final readback:

```text
export_artifact_type=eair_reportable_results_export
reportable=True
protocol_row=provider-live-warrant-model/default/policy_update::near_duplicate_single_source_policy_support
warrant_quality_score=0.0
reportable_protocol_table_exists=True
```
