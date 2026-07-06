# Protocol-Legitimacy Table Plan

Date: 2026-06-21

## Checklist

- [x] Add failing test for adherence-vs-legitimacy export.
- [x] Verify the test fails before implementation.
- [x] Implement export function.
- [x] Add CLI command.
- [x] Run export on the prompt-protocol matrix artifacts.
- [x] Update live runbook to include the protocol-legitimacy table step.
- [x] Run full pytest before final reporting.

## Commands

```text
pytest tests/test_mvp.py::test_eair_protocol_legitimacy_export_joins_adherence_and_warrant_quality -q
pytest tests/test_mvp.py -k "protocol_legitimacy or prompt_adherence or reportable or artifact_summary" -q
python -m formaltrust_platform eair-export-protocol-legitimacy-table --adherence outputs/eair_prompt_protocol_matrix_dry_run/prompt_adherence/prompt_adherence_audit.json --summary outputs/eair_prompt_protocol_matrix_dry_run/summary/artifact_summary.json --output-dir outputs/eair_prompt_protocol_matrix_dry_run/protocol_legitimacy
pytest -q
```

## Final Verification

```text
92 passed
protocol_table_exists=True
protocol_csv_exists=True
protocol_md_exists=True
artifact_type=eair_protocol_legitimacy_table
table_rows=9
hijack_adherence=1.0
hijack_quality=0.0
hijack_gap=1.0
runbook_command_count=9
runbook_has_protocol_table=True
```
