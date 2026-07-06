# Human Review Burden Metrics

## Why This Matters

The project claim is not only "unsafe fields are blocked." The harder claim is:

> strict supervision should not make the agent unnecessarily conservative.

To measure that, the report now tracks how many fields are still auto-executable and how many fields are routed to partial human review.

## New Metrics

| Metric | Meaning |
|---|---|
| `mean_partial_human_review_fields` | Average number of fields per case routed to local human review. |
| `auto_executable_field_ratio` | Auto-executable fields divided by auto-executable plus partial-human-review fields. |
| `human_review_field_counts.partial_human_review_fields` | Total fields routed to partial human review. |
| `human_review_field_counts.auto_executable_fields` | Total fields preserved for automatic execution. |
| `human_review_field_counts.partial_human_review_cases` | Cases with at least one partial-human-review field. |

## Current Results

| Suite | Cases | partial_human_review_fields | auto_executable_fields | mean_partial_human_review_fields | auto_executable_field_ratio |
|---|---:|---:|---:|---:|---:|
| strict-block | 10 | 0 | 0 | 0.000 | 1.000 |
| fieldwise-repair | 10 | 10 | 10 | 1.000 | 0.500 |
| trace-repair | 2 | 2 | 2 | 1.000 | 0.500 |
| span-otlp-repair | 2 | 2 | 2 | 1.000 | 0.500 |

## Interpretation

Strict-block has no partial-human-review fields because it does not expose a local repair frame; it sends the whole final action to human approval. Fieldwise repair makes the burden explicit: in the current mixed cases, one field remains auto-executable and one field is routed to review.

This supports a narrower claim:

> The current repair mode converts whole-action review into field-local review on curated mixed-action cases.

It does not yet prove lower real-world operator workload. That requires real trace volume, realistic field distributions, and human-review time measurements.
