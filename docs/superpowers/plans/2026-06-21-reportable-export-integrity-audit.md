# Reportable Export Integrity Audit Plan

## Acceptance Criteria

- Add a failing CLI test for a replaced `protocol_legitimacy_table.json`.
- Implement `audit_reportable_eair_export`.
- Add `formaltrust eair-audit-reportable-export`.
- Write JSON/Markdown audit files before raising on integrity failure.
- Include the integrity audit in the live prompt-protocol runbook.
- Regenerate the live prompt-protocol runbook sidecar.
- Run the audit on the existing reportable fixture.

## Verification Commands

```powershell
pytest tests/test_mvp.py::test_eair_audit_reportable_export_detects_protocol_source_hash_mismatch -q
pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
python -m formaltrust_platform eair-write-live-runbook --config examples/eair_prompt_protocol_matrix_live_template.yaml --output outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.md
python -m formaltrust_platform eair-audit-reportable-export --export outputs/eair_warrant_reportable_export/reportable_results_export.json --output-dir outputs/eair_warrant_reportable_export/integrity
pytest tests/test_mvp.py -k "reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence or live_runbook" -q
pytest -q
```
