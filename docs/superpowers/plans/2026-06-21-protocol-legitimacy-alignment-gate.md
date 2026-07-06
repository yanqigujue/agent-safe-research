# Protocol-Legitimacy Alignment Gate Plan

## Acceptance Criteria

- Add a red test with a reportable summary and a mismatched protocol-legitimacy row.
- The export must fail with `protocol_legitimacy row not present in summary`.
- The blocked export JSON must record `protocol_legitimacy_path`.
- No reportable protocol artifacts should be written on mismatch.
- Existing successful reportable protocol exports must still pass.

## Verification Commands

```powershell
pytest tests/test_mvp.py::test_eair_export_reportable_results_rejects_mismatched_protocol_legitimacy_rows -q
pytest tests/test_mvp.py::test_eair_export_reportable_results_rejects_mismatched_protocol_legitimacy_rows tests/test_mvp.py::test_eair_export_reportable_results_includes_warrant_taxonomy_columns tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
python -m formaltrust_platform eair-export-reportable-results --summary outputs/eair_warrant_live_fixture_summary/artifact_summary.json --audit outputs/eair_warrant_live_fixture_audit/reportable_run_audit.json --protocol-legitimacy outputs/eair_warrant_live_fixture_protocol_legitimacy/protocol_legitimacy_table.json --output-dir outputs/eair_warrant_reportable_export
pytest -q
```
