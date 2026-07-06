# Reportable Protocol Source Hash Plan

## Acceptance Criteria

- Add a red test requiring `protocol_legitimacy_sha256`.
- Use the existing `_sha256_file` helper.
- Propagate the hash to the main export and reportable protocol artifacts.
- Regenerate fixture outputs.
- Verify all recorded hashes match the source protocol file.

## Verification Commands

```powershell
pytest tests/test_mvp.py::test_eair_export_reportable_results_includes_warrant_taxonomy_columns -q
pytest tests/test_mvp.py::test_eair_export_reportable_results_rejects_protocol_internal_inconsistency tests/test_mvp.py::test_eair_export_reportable_results_rejects_protocol_metric_mismatch tests/test_mvp.py::test_eair_export_reportable_results_rejects_mismatched_protocol_legitimacy_rows tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
python -m formaltrust_platform eair-export-reportable-results --summary outputs/eair_warrant_live_fixture_summary/artifact_summary.json --audit outputs/eair_warrant_live_fixture_audit/reportable_run_audit.json --protocol-legitimacy outputs/eair_warrant_live_fixture_protocol_legitimacy/protocol_legitimacy_table.json --output-dir outputs/eair_warrant_reportable_export
pytest -q
```
