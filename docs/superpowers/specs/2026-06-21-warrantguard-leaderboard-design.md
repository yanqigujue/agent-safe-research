# WarrantGuard Leaderboard Design

## Goal

Turn `warrant_quality_score` from a metric column into a directly sortable leaderboard for model-condition comparisons.

## Scope

This is a reporting-layer change. It does not alter:

- WarrantGuard verification
- hard gates
- evidence sufficiency rules
- reportability audit criteria
- model sampling

## Leaderboard Rows

Each row contains:

- `rank`
- `model`
- `prompt_variant`
- `condition`
- `total_transcripts`
- `warrant_quality_score`
- `warrant_present_rate`
- `warrant_valid_rate`
- `warrant_failure_rate`
- `warrant_present_count`
- `warrant_failed_count`
- `warrant_error_category_counts_json`

## Sorting

Rows are sorted by:

1. `warrant_quality_score` descending
2. `warrant_present_rate` descending
3. `warrant_valid_rate` descending
4. `warrant_failure_rate` ascending
5. `total_transcripts` descending
6. `model` ascending
7. `prompt_variant` ascending
8. `condition` ascending

## Output Artifacts

Artifact-summary outputs:

- `artifact_summary_warrant_leaderboard.json`
- `artifact_summary_warrant_leaderboard.csv`
- `artifact_summary_warrant_leaderboard.md`

Reportable-export outputs:

- `reportable_warrant_leaderboard.json`
- `reportable_warrant_leaderboard.csv`
- `reportable_warrant_leaderboard.md`

Both JSON payloads also embed the leaderboard as `warrant_leaderboard`.

## Claim Boundary

The leaderboard ranks artifact or reportable-run rows that already exist. It is not a new safety metric and does not claim live-provider performance unless the upstream reportability audit passes on live provider transcripts.
