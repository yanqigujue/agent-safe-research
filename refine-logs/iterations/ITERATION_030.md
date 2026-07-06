# ITERATION_030: Standalone Replay CLI and Live Template

Date: 2026-06-20

## Hypothesis

EAIR-Bench should evaluate externally collected transcripts without requiring Python code. A standalone replay command makes the benchmark usable for real model outputs captured outside the sampler.

## Design Change

Added CLI command:

```text
formaltrust eair-replay --transcripts transcripts.jsonl --output-dir replay_dir
python -m formaltrust_platform eair-replay --transcripts transcripts.jsonl --output-dir replay_dir
```

The command runs:

```text
transcript JSONL/JSON -> structured action parser -> EAIR gate -> evaluator -> replay artifacts
```

Added live-provider sampler template:

```text
examples/eair_sampler_live_template.yaml
```

It uses `api_key_env` rather than an inline API key.

## Tests

Added TDD tests:

- `test_eair_replay_cli_evaluates_existing_transcript_jsonl`
- `test_live_sampler_template_uses_api_key_env_not_inline_secret`

Observed failures before implementation:

- CLI reported `No such command 'eair-replay'`.
- `examples/eair_sampler_live_template.yaml` did not exist.

## Experiment

Ran standalone replay:

```text
python -m formaltrust_platform eair-replay \
  --transcripts examples/data/eair_structured_action_transcripts.jsonl \
  --output-dir outputs/eair_replay_cli_pilot
```

Replay summary:

| metric | value |
|---|---:|
| transcripts | 4 |
| parse errors | 1 |
| candidate unsafe | 2 |
| final unsafe | 0 |
| gate allow | 2 |
| gate replace | 2 |

## Supported Claim

EAIR-Bench now has an auditable standalone replay workflow for externally collected model transcripts.

## Claim Boundary

The replay CLI evaluates saved transcripts. It does not sample a live model by itself.

## Next Iteration

Add a concise live-run checklist documenting: set env var, run sampler config, inspect transcript JSONL, run replay, cite replay artifacts.
