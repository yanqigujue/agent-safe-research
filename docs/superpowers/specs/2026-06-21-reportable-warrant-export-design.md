# Reportable Warrant Export Design

## Goal

Make WarrantGuard taxonomy metrics available in reportable paper-facing model-condition tables.

## Scope

This iteration extends `eair-export-reportable-results`. It does not change reportability criteria, replay semantics, or WarrantGuard verification.

## Data Flow

1. `eair-replay` records transcript-level warrant diagnostics.
2. `eair-summarize-artifacts` aggregates warrant diagnostics by model, condition, and model-condition pair.
3. `eair-audit-reportable-run` checks whether the artifact bundle is reportable.
4. `eair-export-reportable-results` exports paper-facing tables.

This iteration adds warrant columns at step 4:

- `warrant_present_count`
- `warrant_failed_count`
- `warrant_error_category_counts_json`

## Acceptance

The exported JSON, CSV, and Markdown table must include warrant taxonomy fields when the summary contains them. Existing exports without warrants should keep working with zero or empty values.

