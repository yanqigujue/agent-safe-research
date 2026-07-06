# Reportable Child Table Row Integrity Plan

## Acceptance Criteria

- Add a red CLI test where the protocol source hash matches but `reportable_protocol_legitimacy_table.json.rows` differs from the main export.
- Extend `audit_reportable_eair_export` to compare child rows against the main export payload.
- Record `expected_row_count`, `actual_row_count`, and `rows_match_export` for each child artifact.
- Regenerate the existing reportable export integrity audit fixture.
- Verify focused and full tests pass.

## Verification Commands

```powershell
pytest tests/test_mvp.py::test_eair_audit_reportable_export_detects_child_table_row_mismatch -q
pytest tests/test_mvp.py::test_eair_audit_reportable_export_detects_protocol_source_hash_mismatch tests/test_mvp.py::test_eair_audit_reportable_export_detects_child_table_row_mismatch -q
python -m formaltrust_platform eair-audit-reportable-export --export outputs/eair_warrant_reportable_export/reportable_results_export.json --output-dir outputs/eair_warrant_reportable_export/integrity
pytest tests/test_mvp.py -k "reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence or live_runbook" -q
pytest -q
```
