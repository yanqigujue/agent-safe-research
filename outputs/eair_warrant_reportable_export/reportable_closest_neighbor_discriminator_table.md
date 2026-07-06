# EAIR Reportable Closest-Neighbor Discriminator Table

Closest-neighbor discriminator rows are derived from reportable reviewer-rejection protected-field rows; they state WarrantGuard's discriminator against nearby problem formulations, not empirical failure claims about prior systems.

| reviewer_rejection | closest_neighbor | count | total_transcripts | warrant_quality_score | conditions | protected_fields | warrant_obligations | WarrantGuard discriminator | claim_boundary |
|---|---|---:|---:|---:|---|---|---|---|---|
| benchmark_overfit_source_diversity | synthetic benchmark overfit critique | 3 | 3 | 0.0 | ["policy_update::near_duplicate_single_source_policy_support"] | ["decision", "risk_report", "tool"] | ["source_diverse_support"] | source-diversity failures separated from clean sufficient-evidence controls | reportable_discriminator_not_prior_work_failure |
| source_attribution_only | RAGForensics / source attribution | 3 | 3 | 0.0 | ["policy_update::near_duplicate_single_source_policy_support"] | ["decision", "risk_report", "tool"] | ["source_diverse_support"] | attributed evidence still needs sufficiency, freshness, source diversity, and low conflict | reportable_discriminator_not_prior_work_failure |
