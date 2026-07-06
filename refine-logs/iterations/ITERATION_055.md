# Iteration 055: Prompt-Variant WarrantGuard Leaderboard

## Motivation

The leaderboard from Iteration 054 ranked model-condition rows, but the next experiment needs to compare prompt designs for the same model. Without a prompt-variant dimension, a proof-carrying prompt and an action-only prompt for the same model/condition would be averaged together.

## Design

Transcript rows can now include:

```text
prompt_variant
```

If omitted, the value is `default`.

The artifact pipeline now exposes:

```text
prompt_variant_counts
by_prompt_variant
by_model_prompt_condition
artifact_summary_by_prompt_variant.csv/md
artifact_summary_by_model_prompt_condition.csv/md
```

WarrantGuard leaderboard rows now include `prompt_variant`.

## TDD

First RED:

```text
pytest tests/test_mvp.py::test_eair_artifact_summary_leaderboard_distinguishes_prompt_variants -q
FAILED: KeyError: 'prompt_variant_counts'
```

Second RED:

```text
FAILED: FileNotFoundError: artifact_summary_by_model_prompt_condition.csv
```

GREEN checks:

```text
pytest tests/test_mvp.py::test_eair_artifact_summary_leaderboard_distinguishes_prompt_variants -q
1 passed

pytest tests/test_mvp.py -k "artifact_summary or reportable_results or reportable_run_audit" -q
10 passed, 19 deselected

pytest tests/test_eair_bench.py -k "structured_action_transcript or warrant" -q
5 passed, 40 deselected
```

## Generated Fixture

```text
examples/data/eair_prompt_variant_warrant_transcripts.jsonl
```

## Generated Artifacts

```text
outputs/eair_prompt_variant_replay
outputs/eair_prompt_variant_summary
```

## Readback

```text
prompt_variant_counts={'legacy_action_only': 1, 'proof_carrying': 1}
prompt_top_variant=proof_carrying
prompt_top_quality=1.0
prompt_second_variant=legacy_action_only
prompt_second_quality=0.0
reportable_prompt_variant=default
```

## Claim Boundary

This iteration supports prompt-variant grouping and ranking. It does not yet compare live prompts or claim that a prompt is generally better.
