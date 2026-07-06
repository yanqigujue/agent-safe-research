# ITERATION_029: Configurable EAIR Sampler CLI

Date: 2026-06-20

## Hypothesis

The live-model sampler should be runnable from a config file, not from ad hoc Python snippets. This makes real-model experiments easier to reproduce and keeps the protocol:

```text
config -> sampler -> transcript JSONL -> replay report
```

## Design Change

Added config runner:

```text
run_openai_compatible_sampling_config
```

Added CLI command:

```text
formaltrust eair-sample --config <sampler.yaml>
python -m formaltrust_platform eair-sample --config <sampler.yaml>
```

Sampler config supports:

- `base_url`
- `model`
- `api_key` or `api_key_env`
- `output_path`
- `replay_output_dir`
- `scenarios`
- `temperature`
- `timeout_seconds`
- `dry_run_responses`

`dry_run_responses` makes the command runnable without a live API while preserving the same transcript/replay path.

## New Example

Added:

```text
examples/eair_sampler_dry_run.yaml
```

This example writes:

```text
outputs/eair_sampler_cli_dry_run/sampled_transcripts.jsonl
outputs/eair_sampler_cli_dry_run/replay/
```

## Tests

Added TDD test:

```text
test_eair_sampler_cli_runs_configured_dry_run_and_replay
```

Observed failure before implementation: CLI reported `No such command 'eair-sample'`.

## Dry-Run Result

Ran:

```text
python -m formaltrust_platform eair-sample --config examples/eair_sampler_dry_run.yaml
```

Replay summary:

| metric | value |
|---|---:|
| transcripts | 2 |
| parse errors | 0 |
| candidate unsafe | 1 |
| final unsafe | 0 |
| gate allow | 1 |
| gate replace | 1 |

## Supported Claim

EAIR-Bench now has a reproducible command-line protocol for model sampling and deterministic replay evaluation.

## Claim Boundary

The example uses `dry_run_responses`, not a live provider. It verifies CLI/config protocol, artifact generation, and replay compatibility.

## Next Iteration

Add a small documented live-run checklist and a sample real-provider config template that uses `api_key_env` rather than inline keys.
