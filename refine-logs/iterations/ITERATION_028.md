# ITERATION_028: OpenAI-Compatible Sampler Dry Run

Date: 2026-06-20

## Hypothesis

The live-model step should be split into two auditable stages:

```text
sample model outputs -> write transcript JSONL -> replay transcript JSONL through EAIR
```

This prevents live API sampling from being confused with deterministic gate/evaluator results.

## Design Change

Added:

```text
sample_openai_compatible_action_transcripts
```

The sampler:

- builds an action-planning prompt from EAIR-Bench query, policy, and retrieved evidence;
- calls an OpenAI-compatible `/chat/completions` endpoint;
- supports an injectable `transport` for tests and dry runs;
- writes replay-compatible transcript JSONL;
- stores the prompt and raw response in each transcript row;
- leaves all safety evaluation to the transcript replay layer.

## Tests

Added TDD test:

```text
test_openai_compatible_sampler_writes_replayable_transcript_jsonl
```

Observed failure before implementation: `sample_openai_compatible_action_transcripts` did not exist.

## Dry-Run Experiment

Ran sampler with a fake OpenAI-compatible transport:

```text
outputs/eair_live_sampler_dry_run/sampled_transcripts.jsonl
outputs/eair_live_sampler_dry_run/replay/
```

Sampling summary:

| metric | value |
|---|---:|
| sampled transcripts | 2 |
| model | `dry-run-openai-compatible` |

Replay summary:

| metric | value |
|---|---:|
| total transcripts | 2 |
| parse errors | 0 |
| candidate unsafe | 1 |
| final unsafe | 0 |
| gate allow | 1 |
| gate replace | 1 |

## Supported Claim

EAIR-Bench now has a live-model-ready sampling interface that writes replayable transcripts before evaluation. This supports a clean experimental protocol for future real-model runs.

## Claim Boundary

This dry run uses fake transport, not a live model call. It proves request construction, transcript writing, and replay compatibility; it does not measure any provider/model behavior.

## Next Iteration

Add a CLI or config-file runner for live sampling so real model experiments can be launched without editing Python code, while preserving the sampler -> transcript JSONL -> replay protocol.
