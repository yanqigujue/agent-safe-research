# Warrant Taxonomy Summary Design

## Goal

Make WarrantGuard replay failures analyzable by category, model, and benchmark condition.

## Approved Direction

This is a direct continuation of the approved WarrantGuard direction. The system already records raw `warrant_errors`; this iteration converts those raw strings into stable categories for experiment tables.

## Taxonomy

The first taxonomy is intentionally small:

| Category | Raw errors |
|---|---|
| `decision_support` | `decision_warrant_missing`, `decision_warrant_insufficient` |
| `approval` | `approval_warrant_missing` |
| `risk_metadata` | `risk_level_warrant_missing`, `risk_report_warrant_missing` |
| `parameter` | `parameter_warrant_missing:<name>` |
| `hard_gate` | `hard_gate_violation` |
| `counter_evidence` | `counter_warrant_not_clear`, `counter_warrant_present` |
| `unknown` | any unrecognized error or warning |

Warnings and errors use the same category mapping so counter-warrant warnings can be aggregated.

## Result Contract

Transcript replay rows add:

- `warrant_error_categories`

Transcript replay summaries add:

- `warrant_error_category_counts`

Artifact summaries add:

- top-level `warrant_present_count`
- top-level `warrant_failed_count`
- top-level `warrant_error_category_counts`
- per-manifest row warrant counts
- per-model, per-condition, and per-model-condition warrant counts and category counts

## Reporting

CSV and Markdown outputs should expose warrant taxonomy columns in:

- `artifact_summary.csv`
- `artifact_summary.md`
- `artifact_summary_by_model.csv`
- `artifact_summary_by_condition.csv`
- `artifact_summary_by_model_condition.csv`
- corresponding Markdown tables

## Non-Goals

This iteration does not change verifier semantics. It only summarizes existing warrant outcomes.

