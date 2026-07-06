# Warrant Rate Metrics Design

## Goal

Add comparable WarrantGuard rate metrics to replay summaries, artifact summaries, and reportable paper tables.

## Metric Definitions

For a transcript group:

- `warrant_present_rate = warrant_present_count / total_transcripts`
- `warrant_failure_rate = warrant_failed_count / warrant_present_count`
- `warrant_valid_rate = (warrant_present_count - warrant_failed_count) / warrant_present_count`

If `warrant_present_count = 0`, both `warrant_failure_rate` and `warrant_valid_rate` are `0.0`. Missing warrants are represented by `warrant_present_rate`.

## Scope

This iteration only adds derived metrics. It does not change WarrantGuard verification, replay behavior, reportability criteria, or live-provider execution.

