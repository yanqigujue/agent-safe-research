# Iteration 066: Protocol Row Internal Consistency

## Goal

Block protocol-legitimacy rows whose prompt-adherence arithmetic is internally inconsistent, even if the row belongs to the summary and selected summary metrics match.

## Implemented

- Added `_protocol_legitimacy_internal_consistency_errors`.
- Checked prompt adherence totals, compliant/noncompliant counts, prompt adherence rate, and adherence-legitimacy gap.
- Integrated the checks into reportable protocol export before metric consistency checks.

## Red-Green

Red check:

```text
pytest tests/test_mvp.py::test_eair_export_reportable_results_rejects_protocol_internal_inconsistency -q
failed because internally inconsistent prompt_adherence_rate was accepted
```

Green check:

```text
pytest tests/test_mvp.py::test_eair_export_reportable_results_rejects_protocol_internal_inconsistency -q
1 passed
```

## Readback

```text
protocol_row=provider-live-warrant-model/default/policy_update::near_duplicate_single_source_policy_support
prompt_adherence_total=1
prompt_adherence_rate=1.0
adherence_legitimacy_gap=1.0
warrant_quality_score=0.0
```

## Boundary

This validates arithmetic self-consistency. It does not prove prompt-adherence labels are semantically correct.

## Verification

```text
pytest tests/test_mvp.py::test_eair_export_reportable_results_rejects_protocol_internal_inconsistency -q
1 passed

pytest tests/test_mvp.py::test_eair_export_reportable_results_includes_warrant_taxonomy_columns tests/test_mvp.py::test_eair_export_reportable_results_rejects_protocol_metric_mismatch tests/test_mvp.py::test_eair_export_reportable_results_rejects_mismatched_protocol_legitimacy_rows tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
4 passed

pytest tests/test_mvp.py -k "reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence or live_runbook" -q
12 passed, 26 deselected

pytest -q
95 passed
```

Final readback:

```text
export_artifact_type=eair_reportable_results_export
reportable=True
protocol_row=provider-live-warrant-model/default/policy_update::near_duplicate_single_source_policy_support
prompt_adherence_total=1
prompt_adherence_rate=1.0
adherence_legitimacy_gap=1.0
warrant_quality_score=0.0
reportable_protocol_table_exists=True
```
