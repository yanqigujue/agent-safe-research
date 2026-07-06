# Iteration 050: Warrant Taxonomy Artifact Summary

## Motivation

Iteration 049 made transcript replay understand model-supplied `(action, warrant)` objects. The next missing piece was analysis: raw warrant errors were visible, but experiment tables could not localize failure types by model or condition.

## Change

This iteration adds a small stable taxonomy:

| Category | Meaning |
|---|---|
| `decision_support` | missing or insufficient warrant for the action decision |
| `approval` | missing human-approval warrant |
| `risk_metadata` | missing risk-level or risk-report warrant |
| `parameter` | missing parameter warrant |
| `hard_gate` | action violates non-negotiable policy |
| `counter_evidence` | counter-warrant is present or not clear |
| `unknown` | fallback for unrecognized issues |

## Implementation

Modified:

- `formaltrust_platform/experiments/eair_bench.py`
- `tests/test_eair_bench.py`
- `tests/test_mvp.py`

Added:

- `docs/superpowers/specs/2026-06-21-warrant-taxonomy-summary-design.md`
- `docs/superpowers/plans/2026-06-21-warrant-taxonomy-summary.md`

Generated:

- `outputs/eair_transcript_replay_pilot/*`
- `outputs/eair_warrant_artifact_summary/*`

## TDD Trace

Red tests:

```text
pytest tests/test_eair_bench.py::test_structured_action_transcript_replay_verifies_model_supplied_warrants -q
FAILED: KeyError: 'warrant_error_categories'

pytest tests/test_mvp.py::test_eair_artifact_summary_aggregates_warrant_taxonomy -q
FAILED: KeyError: 'warrant_present_count'
```

Green tests:

```text
pytest tests/test_eair_bench.py::test_structured_action_transcript_replay_verifies_model_supplied_warrants -q
1 passed

pytest tests/test_mvp.py::test_eair_artifact_summary_aggregates_warrant_taxonomy -q
1 passed

pytest tests/test_eair_bench.py -k "warrant or structured_action_transcript" -q
5 passed, 40 deselected

pytest tests/test_mvp.py -k "artifact_summary or eair_replay" -q
5 passed, 22 deselected
```

## Artifact Readback

Replay:

```text
total_transcripts=6
warrant_present_count=2
warrant_failed_count=1
warrant_error_category_counts={'decision_support': 1}
```

Warrant-specific artifact summary:

```text
total_artifacts=1
total_transcripts=6
warrant_present_count=2
warrant_failed_count=1
warrant_error_category_counts={"decision_support":1}
model_condition_warrant_failed=1
model_condition_categories={"decision_support":1}
```

## Final Verification

```text
pytest -q
84 passed
```

Final artifact readback:

```text
total_artifacts=1
total_transcripts=6
warrant_present_count=2
warrant_failed_count=1
warrant_error_category_counts={"decision_support":1}
model_condition_warrant_failed=1
model_condition_categories={"decision_support":1}
replay_total=6
replay_warrant_present=2
replay_warrant_failed=1
replay_categories={"decision_support":1}
```

## Claim Boundary

Supported:

- Replay artifact summaries can localize WarrantGuard failures by model-condition pair and taxonomy category.

Not yet supported:

- Live-model warrant reliability.
- Official prior-work comparison.
