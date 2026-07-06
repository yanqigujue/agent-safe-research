# Warrant Quality Score Design

## Goal

Add one scalar metric for comparing proof-carrying action behavior across replay artifacts and reportable model-condition tables.

## Definition

```text
warrant_quality_score = valid_warrant_count / total_transcripts
valid_warrant_count = max(0, warrant_present_count - warrant_failed_count)
```

This is equivalent to `warrant_present_rate * warrant_valid_rate` before rounding, but it is computed directly from counts to avoid compounded rounding error.

## Interpretation

- `0.0`: no valid proof-carrying actions in the evaluated transcript set.
- `1.0`: every transcript includes a warrant and every warrant passes verification.
- intermediate values: partial warrant emission, partial field-jurisdiction verification, or both.

## Scope

The score is an artifact/reporting metric. It does not change WarrantGuard verification, hard gates, evidence sufficiency, or reportability criteria.

## Output Surfaces

- structured action transcript replay summary and manifest
- replay artifact summary top-level JSON
- grouped artifact summary tables
- model-condition artifact summary tables
- reportable model-condition JSON/CSV/Markdown export
