# Iteration 067: Reportable Protocol Source Hash

## Goal

Record source integrity metadata for reportable protocol-legitimacy exports.

## Implemented

- Added `protocol_legitimacy_sha256` to `reportable_results_export.json`.
- Added the same hash to `reportable_protocol_legitimacy_table.json`.
- Added the same hash to `reportable_protocol_legitimacy_by_prompt_variant.json`.
- Reused the existing `_sha256_file` helper.

## Red-Green

Red check:

```text
pytest tests/test_mvp.py::test_eair_export_reportable_results_includes_warrant_taxonomy_columns -q
failed because protocol_legitimacy_sha256 was missing
```

Green check:

```text
pytest tests/test_mvp.py::test_eair_export_reportable_results_includes_warrant_taxonomy_columns -q
1 passed
```

## Readback

```text
expected_sha256=317d7ef211ab083cf91b85a12c9ba537f99d753a4ea29ad0eee850b0939fb6f4
export_sha256=317d7ef211ab083cf91b85a12c9ba537f99d753a4ea29ad0eee850b0939fb6f4
table_sha256=317d7ef211ab083cf91b85a12c9ba537f99d753a4ea29ad0eee850b0939fb6f4
aggregate_sha256=317d7ef211ab083cf91b85a12c9ba537f99d753a4ea29ad0eee850b0939fb6f4
all_match=True
```

## Boundary

This proves source-file identity for the export. It does not prove live-provider behavior.

## Verification

```text
pytest tests/test_mvp.py::test_eair_export_reportable_results_includes_warrant_taxonomy_columns -q
1 passed

pytest tests/test_mvp.py::test_eair_export_reportable_results_rejects_protocol_internal_inconsistency tests/test_mvp.py::test_eair_export_reportable_results_rejects_protocol_metric_mismatch tests/test_mvp.py::test_eair_export_reportable_results_rejects_mismatched_protocol_legitimacy_rows tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
4 passed

pytest tests/test_mvp.py -k "reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence or live_runbook" -q
12 passed, 26 deselected

pytest -q
95 passed
```

Final readback:

```text
all_match=True
expected_sha256=317d7ef211ab083cf91b85a12c9ba537f99d753a4ea29ad0eee850b0939fb6f4
export_sha256=317d7ef211ab083cf91b85a12c9ba537f99d753a4ea29ad0eee850b0939fb6f4
table_sha256=317d7ef211ab083cf91b85a12c9ba537f99d753a4ea29ad0eee850b0939fb6f4
aggregate_sha256=317d7ef211ab083cf91b85a12c9ba537f99d753a4ea29ad0eee850b0939fb6f4
```
