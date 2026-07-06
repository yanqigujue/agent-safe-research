# Protocol-Legitimacy Aggregate Design

## Problem

Iteration 061 produced condition-level protocol-legitimacy rows, but the paper also needs a compact prompt-ablation view. The aggregate must show whether a prompt protocol merely increases format adherence or actually improves evidence/action legitimacy.

## Design

Reuse `eair-export-protocol-legitimacy-table` and emit an additional artifact family:

```text
protocol_legitimacy_by_prompt_variant.json
protocol_legitimacy_by_prompt_variant.csv
protocol_legitimacy_by_prompt_variant.md
```

The aggregate groups the condition-level table by `prompt_variant`.

Fields:

- `prompt_variant`
- `row_count`
- `total_transcripts`
- `prompt_adherence_total`
- `prompt_adherence_compliant_count`
- `prompt_adherence_noncompliant_count`
- `prompt_adherence_rate`
- `warrant_quality_score`
- `adherence_legitimacy_gap`
- `high_gap_count`
- `warrant_error_category_counts_json`

`warrant_quality_score` is transcript-weighted across rows. `adherence_legitimacy_gap` is `prompt_adherence_rate - warrant_quality_score`.

## Claim Boundary

The aggregate is descriptive and paper-facing. It does not replace the per-condition table, because failure analysis still needs the condition-level rows.
