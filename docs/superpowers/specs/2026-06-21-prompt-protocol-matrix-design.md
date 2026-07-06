# Prompt-Protocol Matrix Design

Date: 2026-06-21

## Problem

The multi-prompt sampler proved that one scenario can be sampled under several prompt protocols. The next experimental unit needs to compare those protocols across multiple EAIR-Bench conditions and produce summary artifacts in one command.

## Design

Extend sampler configs so `summary_output_dir` triggers artifact summarization after replay.

The command becomes:

```text
eair-sample config
  -> sampled_transcripts.jsonl
  -> replay artifact
  -> coverage-gated artifact summary
  -> prompt-condition matrix
  -> WarrantGuard leaderboard
```

The deterministic matrix fixture covers:

- clean sufficient evidence;
- legitimate policy evidence update;
- parameter-level hijack.

The fixture compares:

- `legacy_action_only`;
- `proof_carrying`;
- `proof_carrying_strict`.

## Expected Interpretation

The proof-carrying variants should improve warrant presence on clean and legitimate cases, but they should not pass parameter hijack merely because a warrant object exists. WarrantGuard should still reject warrants backed by hijack evidence or hard-gate violations.

## Outputs

```text
examples/eair_prompt_protocol_matrix_dry_run.yaml
outputs/eair_prompt_protocol_matrix_dry_run/
```

