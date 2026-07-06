# Protocol Metric Consistency Gate Design

## Problem

The alignment gate rejects protocol rows that do not belong to a reportable summary, but a same-key row could still carry altered metric values. That would let a reportable export cite a protocol table whose numbers do not match the audited artifact summary.

## Design

For each aligned protocol row, compare selected fields against the matching summary metrics:

- `total_transcripts`
- `candidate_unsafe_count`
- `final_unsafe_count`
- `warrant_present_rate`
- `warrant_valid_rate`
- `warrant_failure_rate`
- `warrant_quality_score`
- `warrant_error_category_counts_json`
- `gate_counts_json`
- `influence_counts_json`

Any mismatch blocks the reportable export.

## Boundary

The gate checks consistency with the summary artifact. It does not independently recompute WarrantGuard metrics from transcripts.
