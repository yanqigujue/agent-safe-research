# Iteration 063: Reportable Protocol-Legitimacy Export

## Goal

Carry protocol-legitimacy tables into the reportable paper export path instead of leaving them as standalone intermediate artifacts.

## Implementation

- Added optional CLI argument:
  - `eair-export-reportable-results --protocol-legitimacy protocol_legitimacy_table.json`
- Added reportable output artifacts:
  - `reportable_protocol_legitimacy_table.json/csv/md`
  - `reportable_protocol_legitimacy_by_prompt_variant.json/csv/md`
- Updated the live prompt-matrix runbook:
  - final paper export command passes `--protocol-legitimacy .../protocol_legitimacy_table.json`
  - required artifacts include the final reportable protocol tables

## Fixture Readback

```text
artifact_type=eair_reportable_results_export
reportable=True
protocol_legitimacy_row_count=1
protocol_aggregate_rows=1
reportable_protocol_legitimacy_table.json=True
reportable_protocol_legitimacy_by_prompt_variant.json=True
runbook_command_count=9
has_protocol_legitimacy_arg=True
```

## Boundary

The generated fixture is live-marked for the reportability path but is not a real provider result. Real model claims still require provider transcripts.

## Verification

```text
pytest tests/test_mvp.py::test_eair_export_reportable_results_includes_warrant_taxonomy_columns -q
1 passed

pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
1 passed

pytest tests/test_mvp.py -k "reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence or live_runbook" -q
9 passed, 26 deselected

pytest -q
92 passed
```

Final readback:

```text
all_reportable_protocol_artifacts_exist=True
runbook_has_protocol_arg=True
runbook_has_reportable_protocol_required=True
```
