# Iteration 043: Reportable Results Export Gate

## Motivation

After Iteration 042, reportability status was persisted. The next risk was downstream: a non-reportable dry-run artifact could still be manually copied into paper tables. This iteration adds an export gate so paper-facing model-condition tables are generated only after a passing reportability audit.

## Added Capability

New CLI:

```text
formaltrust eair-export-reportable-results --summary artifact_summary.json --audit reportable_run_audit.json --output-dir paper_tables
python -m formaltrust_platform eair-export-reportable-results --summary artifact_summary.json --audit reportable_run_audit.json --output-dir paper_tables
```

Passing exports write:

```text
reportable_results_export.json
reportable_model_condition_table.csv
reportable_model_condition_table.md
```

Failed exports write:

```text
reportable_results_export_blocked.json
reportable_results_export_blocked.md
```

## Runbook Update

`outputs/eair_live_model_run/RUN_LIVE_MODEL.md` now includes a sixth step:

```text
formaltrust eair-export-reportable-results --summary ...artifact_summary.json --audit ...reportable_run_audit.json --output-dir .../paper_tables
```

## Current Dry-Run Artifact

The complete dry-run fixture has complete coverage but a failed reportability audit. Export is therefore blocked as expected.

Generated blocked artifacts:

```text
outputs/eair_sampler_complete_dry_run/paper_tables/reportable_results_export_blocked.json
outputs/eair_sampler_complete_dry_run/paper_tables/reportable_results_export_blocked.md
```

## Claim Boundary

The export gate protects paper-facing tables from non-reportable artifacts. It does not evaluate model safety; it only enforces the artifact admissibility boundary before table export.

## Tests

- `test_eair_export_reportable_results_writes_paper_table_after_passing_audit`
- `test_eair_export_reportable_results_blocks_failed_audit`
- updated `test_eair_live_runbook_command_writes_provider_workflow`

## Verification

- `pytest -q`: 75 passed
- `python -m formaltrust_platform eair-check-live-config --config examples/eair_sampler_live_template.yaml`: passed
- `python -m formaltrust_platform eair-write-live-runbook --config examples/eair_sampler_live_template.yaml --output outputs/eair_live_model_run/RUN_LIVE_MODEL.md`: passed
- dry-run reportable export blocked as expected and wrote blocked JSON/Markdown artifacts
- targeted tests passed: `pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_provider_workflow tests/test_mvp.py::test_eair_export_reportable_results_writes_paper_table_after_passing_audit tests/test_mvp.py::test_eair_export_reportable_results_blocks_failed_audit -q`
- regenerated live runbook includes `eair-export-reportable-results`
- dry-run export is blocked as expected
