# Iteration 054: WarrantGuard Leaderboard

## Motivation

Iteration 053 introduced `warrant_quality_score`, but the metric still lived as a column inside several tables. For multi-model and multi-prompt experiments, the paper needs a directly sortable leaderboard.

## Design

The leaderboard ranks model-condition rows by:

```text
1. warrant_quality_score descending
2. warrant_present_rate descending
3. warrant_valid_rate descending
4. warrant_failure_rate ascending
5. total_transcripts descending
6. model ascending
7. condition ascending
```

Each row contains:

```text
rank, model, condition, total_transcripts,
warrant_quality_score,
warrant_present_rate, warrant_valid_rate, warrant_failure_rate,
warrant_present_count, warrant_failed_count,
warrant_error_category_counts_json
```

## TDD

Focused RED command:

```text
pytest tests/test_mvp.py::test_eair_artifact_summary_aggregates_warrant_taxonomy tests/test_mvp.py::test_eair_export_reportable_results_includes_warrant_taxonomy_columns -q
```

Expected failure:

```text
KeyError: 'warrant_leaderboard'
```

Focused GREEN result:

```text
2 passed
```

Related check:

```text
pytest tests/test_mvp.py -k "artifact_summary or reportable_results or reportable_run_audit" -q
9 passed, 19 deselected
```

## Generated Artifacts

Artifact summary:

```text
outputs/eair_warrant_artifact_summary/artifact_summary_warrant_leaderboard.json
outputs/eair_warrant_artifact_summary/artifact_summary_warrant_leaderboard.csv
outputs/eair_warrant_artifact_summary/artifact_summary_warrant_leaderboard.md
```

Reportable export:

```text
outputs/eair_warrant_reportable_export/reportable_warrant_leaderboard.json
outputs/eair_warrant_reportable_export/reportable_warrant_leaderboard.csv
outputs/eair_warrant_reportable_export/reportable_warrant_leaderboard.md
```

## Readback

```text
artifact_top_rank=1
artifact_top_model=warrant-fixture
artifact_top_condition=approval_bypass::clean_sufficient_evidence
artifact_top_quality=1.0
reportable_top_rank=1
reportable_top_quality=0.0
```

## Claim Boundary

The leaderboard is a reporting artifact over already-generated summary rows. It does not alter verifier behavior and does not constitute a live-provider result unless the upstream transcripts are live and pass reportability audit.
