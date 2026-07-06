# Prompt-Variant WarrantGuard Leaderboard Design

## Goal

Support multi-prompt proof-carrying action experiments by preserving `prompt_variant` through transcript replay, artifact summaries, and WarrantGuard leaderboards.

## Design

Transcript rows may include:

```json
{"prompt_variant": "proof_carrying"}
```

If omitted, the value is `default`.

The replay and summary pipeline now records:

- transcript-level `prompt_variant`
- summary-level `prompt_variant_counts`
- `by_prompt_variant`
- `by_model_prompt_condition`
- leaderboard rows with `prompt_variant`

## Output Files

Artifact summaries write:

- `artifact_summary_by_prompt_variant.csv`
- `artifact_summary_by_prompt_variant.md`
- `artifact_summary_by_model_prompt_condition.csv`
- `artifact_summary_by_model_prompt_condition.md`

WarrantGuard leaderboard CSV/Markdown/JSON includes `prompt_variant` after `model`.

## Claim Boundary

This is a grouping and reporting-layer change. It does not claim one prompt is better until populated by live or controlled replay experiments.
