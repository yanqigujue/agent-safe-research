# Iteration 051: Reportable Warrant Export

## Motivation

Iteration 050 made warrant taxonomy visible in replay artifact summaries, but the final paper-facing export table still omitted those fields. That meant WarrantGuard diagnostics could be audited internally but not directly cited in a reportable model-condition table.

## Change

`eair-export-reportable-results` now includes:

- `warrant_present_count`
- `warrant_failed_count`
- `warrant_error_category_counts_json`

in JSON, CSV, and Markdown outputs.

## Implementation

Modified:

- `formaltrust_platform/experiments/eair_bench.py`
- `tests/test_mvp.py`

Added:

- `docs/superpowers/specs/2026-06-21-reportable-warrant-export-design.md`
- `docs/superpowers/plans/2026-06-21-reportable-warrant-export.md`
- `examples/data/eair_live_warrant_reportable_fixture.jsonl`

Generated:

- `outputs/eair_warrant_live_fixture_replay`
- `outputs/eair_warrant_live_fixture_summary`
- `outputs/eair_warrant_live_fixture_audit`
- `outputs/eair_warrant_reportable_export`

## TDD Trace

Red test:

```text
pytest tests/test_mvp.py::test_eair_export_reportable_results_includes_warrant_taxonomy_columns -q
FAILED: KeyError: 'warrant_present_count'
```

Green tests:

```text
pytest tests/test_mvp.py::test_eair_export_reportable_results_includes_warrant_taxonomy_columns -q
1 passed

pytest tests/test_mvp.py -k "reportable_results or reportable_run_audit or artifact_summary" -q
9 passed, 19 deselected
```

## Artifact Readback

```text
reportable=True
model=provider-live-warrant-model
condition=policy_update::near_duplicate_single_source_policy_support
warrant_present_count=1
warrant_failed_count=1
warrant_error_category_counts_json={"decision_support": 1}
```

## Final Verification

```text
pytest -q
85 passed
```

Final artifact checks:

```text
exists=outputs/eair_warrant_reportable_export/reportable_results_export.json
exists=outputs/eair_warrant_reportable_export/reportable_model_condition_table.csv
exists=outputs/eair_warrant_reportable_export/reportable_model_condition_table.md
exists=outputs/eair_warrant_live_fixture_audit/reportable_run_audit.json
reportable=True
warrant_present_count=1
warrant_failed_count=1
warrant_error_category_counts_json={"decision_support": 1}
```

## Claim Boundary

Supported:

- Reportable export tables can carry WarrantGuard taxonomy columns.

Not yet supported:

- Real live-provider warrant reliability, because the current artifact is a live-marked fixture.
