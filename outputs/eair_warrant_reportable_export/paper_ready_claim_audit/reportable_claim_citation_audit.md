# EAIR Reportable Claim Citation Audit

| field | value |
|---|---|
| passed | true |
| require_reviewed | true |
| human_reviewed | true |
| review_status | reviewed |
| review_manifest_payload_sha256_matches | true |
| claim_count | 15 |
| passed_claim_count | 15 |
| failed_claim_count | 0 |

## Claims

| claim_id | json_path | expected | actual | artifact_sha256_matches | passed |
|---|---|---|---|---:|---:|
| warrant_quality_rank_1 | warrant_leaderboard.0.warrant_quality_score | 0.0 | 0.0 | true | true |
| protocol_legitimacy_gap_1 | protocol_legitimacy_by_prompt_variant.0.adherence_legitimacy_gap | 1.0 | 1.0 | true | true |
| protected_field_warrant_quality_1 | protected_field_rows.0.warrant_quality_score | 0.0 | 0.0 | true | true |
| protected_field_warrant_quality_2 | protected_field_rows.1.warrant_quality_score | 0.0 | 0.0 | true | true |
| protected_field_warrant_quality_3 | protected_field_rows.2.warrant_quality_score | 0.0 | 0.0 | true | true |
| reviewer_rejection_protected_field_warrant_quality_1 | reviewer_rejection_protected_field_rows.0.warrant_quality_score | 0.0 | 0.0 | true | true |
| reviewer_rejection_protected_field_warrant_quality_2 | reviewer_rejection_protected_field_rows.1.warrant_quality_score | 0.0 | 0.0 | true | true |
| reviewer_rejection_protected_field_warrant_quality_3 | reviewer_rejection_protected_field_rows.2.warrant_quality_score | 0.0 | 0.0 | true | true |
| reviewer_rejection_protected_field_warrant_quality_4 | reviewer_rejection_protected_field_rows.3.warrant_quality_score | 0.0 | 0.0 | true | true |
| reviewer_rejection_protected_field_warrant_quality_5 | reviewer_rejection_protected_field_rows.4.warrant_quality_score | 0.0 | 0.0 | true | true |
| reviewer_rejection_protected_field_warrant_quality_6 | reviewer_rejection_protected_field_rows.5.warrant_quality_score | 0.0 | 0.0 | true | true |
| influence_contrast_warrant_quality_1 | influence_contrast_rows.0.warrant_quality_score | 0.0 | 0.0 | true | true |
| closest_neighbor_discriminator_count_1 | closest_neighbor_discriminator_rows.0.reviewer_rejection_count | 3 | 3 | true | true |
| closest_neighbor_discriminator_count_2 | closest_neighbor_discriminator_rows.1.reviewer_rejection_count | 3 | 3 | true | true |
| reportable_export_integrity_passed | passed | true | true | true | true |

## Errors

- none
