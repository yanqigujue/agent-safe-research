# Iteration 053: Warrant Quality Score

## Motivation

Iterations 050-052 made WarrantGuard diagnostics visible as counts, taxonomy, and rates. The next missing piece was a single scalar score that can rank model-condition pairs by proof-carrying action quality.

## Design

```text
warrant_quality_score = valid_warrant_count / total_transcripts
valid_warrant_count = max(0, warrant_present_count - warrant_failed_count)
```

The score is equivalent to `warrant_present_rate * warrant_valid_rate` before rounding, but it is computed directly from counts.

## TDD

Focused RED command:

```text
pytest tests/test_eair_bench.py::test_structured_action_transcript_replay_verifies_model_supplied_warrants tests/test_mvp.py::test_eair_artifact_summary_aggregates_warrant_taxonomy tests/test_mvp.py::test_eair_export_reportable_results_includes_warrant_taxonomy_columns -q
```

Expected failure:

```text
KeyError: 'warrant_quality_score'
```

Focused GREEN result:

```text
3 passed
```

Related checks:

```text
pytest tests/test_eair_bench.py -k "warrant or structured_action_transcript" -q
5 passed, 40 deselected

pytest tests/test_mvp.py -k "artifact_summary or reportable_results or reportable_run_audit" -q
9 passed, 19 deselected
```

## Generated Artifacts

```text
outputs/eair_transcript_replay_pilot
outputs/eair_warrant_artifact_summary
outputs/eair_warrant_live_fixture_replay
outputs/eair_warrant_live_fixture_summary
outputs/eair_warrant_live_fixture_audit
outputs/eair_warrant_reportable_export
```

## Readback

```text
replay_warrant_quality_score=0.1667
replay_warrant_present_rate=0.3333
replay_warrant_valid_rate=0.5

summary_warrant_quality_score=0.1667
summary_warrant_present_rate=0.3333
summary_warrant_valid_rate=0.5

export_warrant_quality_score=0.0
export_warrant_present_rate=1.0
export_warrant_valid_rate=0.0
```

## Claim Boundary

The score is currently supported for deterministic replay fixtures and live-marked reportable fixtures. It prepares the comparison axis for real provider experiments but is not itself a live-provider result.
