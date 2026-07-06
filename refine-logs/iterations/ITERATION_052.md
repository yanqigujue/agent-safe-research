# Iteration 052: Warrant Rate Metrics

## Motivation

Raw warrant counts are useful for audits, but model comparisons need rates. A model that never emits warrants and a model that emits invalid warrants should be distinguishable.

## Change

Added:

- `warrant_present_rate`
- `warrant_failure_rate`
- `warrant_valid_rate`

Definitions:

```text
warrant_present_rate = warrant_present_count / total_transcripts
warrant_failure_rate = warrant_failed_count / warrant_present_count
warrant_valid_rate = (warrant_present_count - warrant_failed_count) / warrant_present_count
```

If no warrant is present, failure and valid rates are `0.0`.

## Implementation

Modified:

- `formaltrust_platform/experiments/eair_bench.py`
- `tests/test_eair_bench.py`
- `tests/test_mvp.py`

Generated:

- `outputs/eair_transcript_replay_pilot/*`
- `outputs/eair_warrant_artifact_summary/*`
- `outputs/eair_warrant_reportable_export/*`

## TDD Trace

Red tests:

```text
pytest tests/test_eair_bench.py::test_structured_action_transcript_replay_verifies_model_supplied_warrants tests/test_mvp.py::test_eair_artifact_summary_aggregates_warrant_taxonomy tests/test_mvp.py::test_eair_export_reportable_results_includes_warrant_taxonomy_columns -q
FAILED: KeyError: 'warrant_present_rate'
```

Green tests:

```text
pytest tests/test_eair_bench.py::test_structured_action_transcript_replay_verifies_model_supplied_warrants tests/test_mvp.py::test_eair_artifact_summary_aggregates_warrant_taxonomy tests/test_mvp.py::test_eair_export_reportable_results_includes_warrant_taxonomy_columns -q
3 passed

pytest tests/test_eair_bench.py -k "warrant or structured_action_transcript" -q
5 passed, 40 deselected

pytest tests/test_mvp.py -k "artifact_summary or reportable_results or reportable_run_audit" -q
9 passed, 19 deselected
```

## Artifact Readback

```text
replay_total=6
replay_warrant_present_rate=0.3333
replay_warrant_failure_rate=0.5
replay_warrant_valid_rate=0.5

summary_total=6
summary_warrant_present_rate=0.3333
summary_warrant_failure_rate=0.5
summary_warrant_valid_rate=0.5
model_condition_failure_rate=1.0
model_condition_valid_rate=0.0

export_warrant_present_rate=1.0
export_warrant_failure_rate=1.0
export_warrant_valid_rate=0.0
```

## Final Verification

```text
pytest -q
85 passed
```

Final artifact readback:

```text
replay_warrant_present_rate=0.3333
replay_warrant_failure_rate=0.5
replay_warrant_valid_rate=0.5
summary_warrant_present_rate=0.3333
summary_warrant_failure_rate=0.5
summary_warrant_valid_rate=0.5
model_condition_failure_rate=1.0
model_condition_valid_rate=0.0
export_warrant_present_rate=1.0
export_warrant_failure_rate=1.0
export_warrant_valid_rate=0.0
```

## Claim Boundary

Supported:

- Replay, artifact summary, and reportable export tables can carry comparable warrant rates.

Not yet supported:

- Real live-provider warrant reliability.
