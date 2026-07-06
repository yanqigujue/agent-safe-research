# Reportable Protocol-Legitimacy Export Plan

## Acceptance Criteria

- Add a failing test for `--protocol-legitimacy`.
- Add the optional CLI argument.
- Validate that the supplied artifact has `artifact_type=eair_protocol_legitimacy_table`.
- Write reportable condition-level and prompt-aggregate protocol artifacts only after reportability passes.
- Add the protocol argument to the live prompt-matrix runbook paper export command.
- Include final reportable protocol artifacts in the runbook required artifact list.
- Regenerate fixture outputs and docs.

## Verification Commands

```powershell
pytest tests/test_mvp.py::test_eair_export_reportable_results_includes_warrant_taxonomy_columns -q
pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
pytest tests/test_mvp.py -k "reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence or live_runbook" -q
python -m formaltrust_platform eair-export-reportable-results --summary outputs/eair_warrant_live_fixture_summary/artifact_summary.json --audit outputs/eair_warrant_live_fixture_audit/reportable_run_audit.json --protocol-legitimacy outputs/eair_warrant_live_fixture_protocol_legitimacy/protocol_legitimacy_table.json --output-dir outputs/eair_warrant_reportable_export
pytest -q
```
