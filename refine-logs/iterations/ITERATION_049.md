# Iteration 049: Action-Warrant Transcript Replay

## Motivation

`warrantguard_full` made proof-carrying actions visible in the deterministic baseline table, but transcript replay still evaluated bare action JSON. The next step is to let model outputs carry their own warrants.

## Change

Structured transcript replay now accepts:

- legacy bare action JSON;
- top-level `(action, warrant)` JSON.

When a model-supplied warrant is present, replay verifies it with `verify_action_warrant`. A failed warrant blocks or replaces the action before final evaluation.

## Implementation

Modified:

- `formaltrust_platform/experiments/eair_bench.py`
- `tests/test_eair_bench.py`
- `examples/data/eair_structured_action_transcripts.jsonl`
- `outputs/eair_transcript_replay_pilot/*`

Added:

- `warrant_from_mapping`
- `warrant_to_dict`
- `action_warrant_from_mapping`
- `action_warrant_from_model_output`

## TDD Trace

Red tests:

```text
pytest tests/test_eair_bench.py::test_structured_action_transcript_replay_verifies_model_supplied_warrants -q
FAILED: KeyError: 'warrant_present_count'

pytest tests/test_eair_bench.py::test_openai_compatible_sampler_writes_replayable_transcript_jsonl -q
FAILED: assert '"warrant"' in prompt
```

Green tests:

```text
pytest tests/test_eair_bench.py::test_structured_action_transcript_replay_verifies_model_supplied_warrants -q
1 passed

pytest tests/test_eair_bench.py::test_openai_compatible_sampler_writes_replayable_transcript_jsonl -q
1 passed
```

## Fixture Replay Readback

```text
total_transcripts=6
warrant_present_count=2
warrant_failed_count=1
gate_counts={'allow': 3, 'replace': 2, 'block': 1}
```

The failing warrant fixture records:

```text
decision_warrant_insufficient
```

## Final Verification

```text
pytest -q
83 passed
```

Artifact readback:

```text
total_transcripts=6
warrant_present_count=2
warrant_failed_count=1
gate_counts={"allow":3,"replace":2,"block":1}
decision_warrant_insufficient
```

Deterministic pilot remains readable:

```text
bench_total_results=270
bench_warrant_failure_rate=0.6
bench_mean_warrant_error_count=0.8667
```

## Claim Boundary

Supported:

- Replay can evaluate model-supplied warrants when present.
- The sampler now asks for proof-carrying action output.

Not yet supported:

- A live model consistently emits valid warrants.
- Warrant quality generalizes beyond the fixture rows.
