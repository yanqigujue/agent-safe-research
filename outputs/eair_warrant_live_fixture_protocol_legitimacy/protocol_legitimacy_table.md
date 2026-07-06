# Protocol vs Legitimacy Table

Joins prompt protocol adherence with WarrantGuard legitimacy metrics; it does not sample or replay transcripts.

| model | prompt_variant | condition | prompt_adherence_rate | warrant_quality_score | adherence_legitimacy_gap | warrant_errors | gate_counts |
|---|---|---|---:|---:|---:|---|---|
| provider-live-warrant-model | default | policy_update::near_duplicate_single_source_policy_support | 1.0000 | 0.0000 | 1.0000 | {"decision_support": 1} | {"block": 1} |
